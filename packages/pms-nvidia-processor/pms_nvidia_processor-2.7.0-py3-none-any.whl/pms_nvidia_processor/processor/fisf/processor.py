from .config import *
from .context import *
from ..base.dependency import *
from ..base.processor import *
from ...utility import patcher, normalizer, batch, caster


def _pre_processing(
    batch_input_images: list[np.ndarray],
    input_buffer0: np.ndarray,
    input_buffer1: np.ndarray,
) -> None:
    b = len(batch_input_images)
    for batch_idx in range(b):
        image = batch_input_images[batch_idx]
        h, w, c = image.shape
        for channel_idx in range(3):
            input_buffer0[batch_idx, channel_idx, :h, :w] = image[:, :, channel_idx]
            input_buffer1[batch_idx, channel_idx, :h, :w] = image[:, :, channel_idx + 3]


def _post_processing(
    output_buffer: np.ndarray,  # BxCxHxW
    output_image: np.ndarray,  # BxHxWxC
) -> None:
    b, h, w, c = output_image.shape
    x = output_buffer[:b, :, :h, :w]
    for i in range(3):
        np.copyto(src=x[:b, i, :, :], dst=output_image[:, :, :, i])


class FISFProcessorBase(NVIDIAProcessorBase[EngineIOData, EngineIOData]):

    def __init__(
        self,
        concurrency: int,
        index: int,
        model_path: str,
        device: Literal["auto"] | int = "auto",
        normalization: str = "color-basic",
    ):
        # super
        super().__init__(
            concurrency=concurrency,
            index=index,
            model_path=model_path,
            device=device,
        )

        self.config = FISFConfig
        self.normalizer = normalizer.NormalizerFactory.create_multi(normalization)

    async def inference(
        self, batch_input_data: list[np.ndarray], batch_output_data: np.ndarray
    ):
        session = self.session

        _pre_processing(
            batch_input_images=batch_input_data,
            input_buffer0=self.input_buffer0,
            input_buffer1=self.input_buffer1,
        )

        session.run()
        _post_processing(
            output_buffer=self.output_buffer,
            output_image=batch_output_data,
        )

    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        max_batch_size = self.io_shapes["input0"][0][0]
        # 여기서 patching
        input_vector = self.caster.cast(
            input_data.frame
        )  # must be h x w x 6(a pair of frames)
        [
            self.normalizer.normalize(input_vector[:, :, i * 3 : (i + 1) * 3], 2)
            for i in range(2)
        ]
        context = FISFContext(input_vector, self.patcher)
        # batch inference
        for batch_input_patches, batch_output_patches in zip(
            batch.BatchTool.batch_list(context.input_patches, max_batch_size),
            batch.BatchTool.batch_vector(context.output_patches, max_batch_size),
        ):
            await self.inference(
                batch_input_data=batch_input_patches,
                batch_output_data=batch_output_patches,
            )

        self.patcher.merge(
            output_vector=context.output_vector,
            patches=context.output_patches,
        )

        self.normalizer.denormalize(context.output_vector, 2)
        return EngineIOData(
            frame_id=input_data.frame_id,
            frame=self.caster.uncast(context.output_vector),
        )

    def _ready_processor(self) -> bool:
        return True

    def _bind_io(self, input_data: EngineIOData):
        self.caster = caster.Caster(input_data.frame)

        patcher_config = self.config.PATCHER_CONFIG
        trt_config = self.config.TRT_CONFIG

        input_image_set: np.ndarray = input_data.frame  # type: ignore
        padded_input_image = patcher.pad_vector(
            input_image_set,
            overlap_length=patcher_config.input_overlab_length,
        )
        output_image: np.ndarray = np.zeros(
            (
                input_image_set.shape[0] * self.config.UPSCALE_RATIO,
                input_image_set.shape[1] * self.config.UPSCALE_RATIO,
                self.config.NUMBER_OF_OUTPUT_CHANNELS,
            ),
            np.uint8,
        )
        self.patcher = patcher.Patcher(
            **patcher_config.build_patcher_params(
                input_vector=padded_input_image,
                output_vector=output_image,
            )
        )
        n_patches = len(self.patcher.slice(input_vector=padded_input_image))

        # set io shape
        self.batch_size = min(n_patches, self.config.MAX_BATCH_SIZE)
        self.io_shapes = {
            "input0": (
                [self.batch_size, *trt_config.input_shape],
                np.float32,
            ),
            "input1": (
                [self.batch_size, *trt_config.input_shape],
                np.float32,
            ),
            "output": (
                [self.batch_size, *trt_config.output_shape],
                np.float32,
            ),
        }

        # init trt engine
        self.initialize_trt_session(
            required_batch_size=self.batch_size,
            io_shape=self.io_shapes,
        )

        # set io buffer
        self.input_buffer0 = self.session._input_bindings[0].host_buffer.reshape(
            self.io_shapes["input0"][0]
        )
        self.input_buffer1 = self.session._input_bindings[1].host_buffer.reshape(
            self.io_shapes["input1"][0]
        )
        self.output_buffer = self.session._output_bindings[0].host_buffer.reshape(
            self.io_shapes["output"][0]
        )

        return True

    def _get_live(self) -> bool:
        return True

    def _get_concurrency(self) -> int:
        return self._concurrency


@register
class FISFProcessor(FISFProcessorBase):
    def __init__(
        self,
        concurrency: int,
        index: int,
        model_path: str,
        scale_factor: int,
        device: int | Literal["auto"] = "auto",
    ):
        super().__init__(concurrency, index, model_path, device)
        assert (
            scale_factor % 2 == 0
        ), f"ERROR, The scale_factor must be a power of 2. (value={scale_factor})"
        self.scale_factor = scale_factor
        self.num_iterations = int(np.log2(scale_factor))

    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        frames = [
            input_data.frame[:, :, 0:3],
            input_data.frame[:, :, 3:6],
        ]  # The shape must be h x w x 6
        for _ in range(self.num_iterations):
            new_frames = []
            for i in range(len(frames) - 1):
                partial_input_data = EngineIOData(
                    frame_id=input_data.frame_id,
                    frame=np.concatenate([frames[i + 0], frames[i + 1]], axis=-1),
                )
                partial_output_data = await super()._run(partial_input_data)
                new_frames.append(partial_output_data.frame)

            # Create a new list that interleaves existing frames and new frames
            frames = [
                frame for pair in zip(frames[:-1], new_frames) for frame in pair
            ] + [frames[-1]]
        result = np.concatenate(frames, axis=-1)
        return EngineIOData(frame_id=input_data.frame_id, frame=result)
