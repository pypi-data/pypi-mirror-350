from pms_nvidia_processor.processor.color_resnet.context import ColorResnetPostContext
from .config import *
from ..base.dependency import *
from ..base.processor import *
from ...utility import patcher, normalizer, batch, caster


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


def _post_processing_patch(
    output_buffer: np.ndarray,  # BxCxHxW
    output_image: np.ndarray,  # BxHxWxC
) -> None:
    b, h, w, c = output_image.shape
    pred = output_buffer[:b, :, :h, :w]
    for i in range(3):
        np.copyto(src=pred[:, i, :, :], dst=output_image[:, :, :, i])


def _post_processing_merged(
    output_image: np.ndarray,
    scale_min: np.ndarray,
    scale_max: np.ndarray,
):
    np.subtract(output_image, scale_min, out=output_image)
    np.divide(output_image, scale_max - scale_min, out=output_image)


def _get_scale_factor(output_image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    def _rgb2grayscale(rgb: np.ndarray):
        return (
            0.299 * rgb[..., :, :, 0:1]
            + 0.587 * rgb[..., :, :, 1:2]
            + 0.114 * rgb[..., :, :, 2:3]
        )

    scale_max = (
        np.amax(
            _rgb2grayscale(output_image),
            # axis=(-3, -2, -1),
            axis=(-2, -1, -3),
            keepdims=True,
        )
        + 0.0015
    )
    scale_min = (
        np.amin(
            _rgb2grayscale(output_image),
            # axis=(-3, -2, -1),
            axis=(-2, -1, -3),
            keepdims=True,
        )
        - 0.0015
    )
    return scale_min, scale_max


@register
class COLORRESNETPOSTProcessor(NVIDIAProcessorBase[EngineIOData, EngineIOData]):

    def __init__(
        self,
        concurrency: int,
        index: int,
        model_path: str,
        filter_coefficient: np.ndarray,
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
        self.filter_coefficient = filter_coefficient
        self.config = ColorResnetPostConfig
        self.is_scale_factor_calculated = False
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
        _post_processing_patch(
            output_buffer=self.output_buffer,
            output_image=batch_output_data,
        )

    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        max_batch_size = 1
        # 여기서 patching
        input_vector = self.caster.cast(input_data.frame)
        self.normalizer.normalize(input_vector, 2)
        context = ColorResnetPostContext(input_vector, self.patcher)

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

        if not self.is_scale_factor_calculated:
            self.scale_min, self.scale_max = _get_scale_factor(context.output_vector)
            self.is_scale_factor_calculated = True
        _post_processing_merged(
            output_image=context.output_vector,
            scale_min=self.scale_min,
            scale_max=self.scale_max,
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
        output_image: np.ndarray = np.zeros(input_image.shape, np.float32)
        self.patcher = patcher.Patcher(
            **patcher_config.build_patcher_params(
                input_vector=padded_input_image,
                output_vector=output_image,
            )
        )
        n_patches = len(self.patcher.slice(input_vector=padded_input_image))

        # set io shape
        # self.batch_size = min(n_patches + 1, self.config.MAX_BATCH_SIZE - 1)
        self.batch_size = self.config.MAX_BATCH_SIZE
        self.io_shapes = {
            "input": (
                [self.batch_size, *trt_config.input_shape],
                np.float32,
            ),
            "model_output": (
                [1, *self.config.TRT_SHAPE_MODEL_OUTPUT],
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
        self.filter_coefficient_buffer = self.session._input_bindings[
            1
        ].host_buffer.reshape(self.io_shapes["model_output"][0])
        self.output_buffer = self.session._output_bindings[0].host_buffer.reshape(
            self.io_shapes["output"][0]
        )
        self.filter_coefficient_buffer[:] = self.filter_coefficient[:]
        self.session.run()
        return True

    def _get_live(self) -> bool:
        return True

    def _get_concurrency(self) -> int:
        return self._concurrency
