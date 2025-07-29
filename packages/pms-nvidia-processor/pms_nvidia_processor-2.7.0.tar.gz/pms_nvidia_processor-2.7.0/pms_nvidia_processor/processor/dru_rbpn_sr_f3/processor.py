from ..base.dependency import *
from ..base.processor import *
from ...utility import patcher, normalizer, batch, caster
from .config import *
from .context import *


def _pre_processing(
    batch_input_images: list[np.ndarray],
    input_buffer: np.ndarray,
) -> None:
    b = len(batch_input_images)
    for batch_idx in range(b):
        image = batch_input_images[batch_idx]
        h, w, c = image.shape
        for channel_idx in range(c):
            input_buffer[batch_idx, channel_idx, :h, :w] = image[:, :, channel_idx]


def _post_processing(
    output_buffer: np.ndarray,  # BxCxHxW
    output_image: np.ndarray,  # BxHxWxC
) -> None:

    b, h, w, c = output_image.shape
    for i in range(3):
        np.copyto(src=output_buffer[:b, i, :h, :w], dst=output_image[:, :, :, i])


@register
class DRURBPNSRF3Processor(NVIDIAProcessorBase[EngineIOData, EngineIOData]):

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

        self.config = DRURBPNSRF3Config
        self.normalizer = normalizer.NormalizerFactory.create_multi(normalization)

    async def inference(
        self,
        batch_input_data: list[np.ndarray],
        batch_output_data: np.ndarray,
    ):
        session = self.session
        _pre_processing(
            batch_input_images=batch_input_data,
            input_buffer=self.input_buffer,
        )
        session.run()
        _post_processing(
            output_buffer=self.output_buffer,
            output_image=batch_output_data,
        )

    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        max_batch_size = self.io_shapes["input"][0][0]
        # 여기서 patching
        input_vector = self.caster.cast(input_data.frame)
        [
            self.normalizer.normalize(input_vector[:, :, i * 3 : (i + 1) * 3], 2)
            for i in range(self.config.NUMBER_OF_FRAMES)
        ]
        context = DRURBPNSRF3Context(input_vector, self.patcher)

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

        input_image: np.ndarray = input_data.frame  # type: ignore
        padded_input_image = patcher.pad_vector(
            input_image,
            overlap_length=patcher_config.input_overlab_length,
        )
        output_image: np.ndarray = np.zeros(
            (
                input_image.shape[0] * self.config.UPSCALE_RATIO,
                input_image.shape[1] * self.config.UPSCALE_RATIO,
                self.config.NUMBER_OF_OUTPUT_CHANNELS,
            )
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
            "input": (
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
        self.input_buffer = self.session._input_bindings[0].host_buffer.reshape(
            self.io_shapes["input"][0]
        )
        self.input_buffer.fill(1.0 / 255.0)
        self.output_buffer = self.session._output_bindings[0].host_buffer.reshape(
            *self.io_shapes["output"][0]
        )

        return True

    def _get_live(self) -> bool:
        return True

    def _get_concurrency(self) -> int:
        return self._concurrency
