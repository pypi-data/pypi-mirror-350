import os
import tempfile as tf
import pms_tensorrt as trt
import pms_model_manager as pmm
from ..processor.dpir.config import DPIRConfig
from ..processor.dru_asm_sr_f3.config import DRUASMSRF3Config
from ..processor.dru_rbpn_deinter_f3_gloss.config import (
    DRURBPNDEINTERF3GLOSSConfig,
)
from ..processor.dru_rbpn_deinter_pc_f2.config import (
    DRURBPNDEINTERPCF2Config,
)
from ..processor.dru_rbpn_sr_f3.config import DRURBPNSRF3Config
from ..processor.dru_rbpn_sr_f5.config import DRURBPNSRF5Config
from ..processor.color_resnet.config import (
    ColorResnetPostConfig,
    ColorResnetPreConfig,
)
from ..processor.fisf.config import FISFConfig
from ..processor.gg.config import GGConfig
from ..processor.col_en.config import ColEnConfig
from ..processor.cdru_f2.config import CDRUF2Config

__MODEL_CONFIG_MAP = {
    "DPIR": DPIRConfig,
    "DRU-RBPN-SR-F3": DRURBPNSRF3Config,
    "DRU-RBPN-SR-F5": DRURBPNSRF5Config,
    "DRU-ASM-SR-F3": DRUASMSRF3Config,
    "DRU-RBPN-DEINTER-F3-GLOSS": DRURBPNDEINTERF3GLOSSConfig,
    "DRU-RBPN-DEINTER-PC-F2": DRURBPNDEINTERPCF2Config,
    "FISF": FISFConfig,
    "COLOR-RESNET-PRE": ColorResnetPreConfig,
    "COLOR-RESNET-POST": ColorResnetPostConfig,
    "GG": GGConfig,
    "COL-EN": ColEnConfig,
    "CDRU-F2": CDRUF2Config,
}


def create_build_params(
    model_name: str,
    device: int = 0,
    downlaod_model_alias="newest",
):  # -> dict[str, Any]:
    import pms_tensorrt as trt

    assert (
        model_name in __MODEL_CONFIG_MAP
    ), f"ERROR!, model_name={model_name} is not in the list. {__MODEL_CONFIG_MAP.keys()}"
    params: dict = {
        "model_name": model_name,
        "device": device,
        "downlaod_model_alias": downlaod_model_alias,
    }
    config = __MODEL_CONFIG_MAP[model_name]
    if config is FISFConfig:
        params.update(
            {
                "build_config_flags": [],
                "shape_profile": {
                    "input0": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                    },
                    "input1": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                    },
                    "output": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                    },
                },
            }
        )
    elif config is ColorResnetPreConfig:
        params.update(
            {
                "build_config_flags": [],
                "shape_profile": {
                    "input": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_SHAPE_INPUT,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_SHAPE_INPUT,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_SHAPE_INPUT,
                        ],
                    },
                    "output": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_SHAPE_OUTPUT,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_SHAPE_OUTPUT,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_SHAPE_OUTPUT,
                        ],
                    },
                },
            }
        )
    elif config is ColorResnetPostConfig:
        params.update(
            {
                "build_config_flags": [],
                "shape_profile": {
                    "input": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                    },
                    "model_output": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_SHAPE_MODEL_OUTPUT,
                        ],
                        "opt_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_SHAPE_MODEL_OUTPUT,
                        ],
                        "max_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_SHAPE_MODEL_OUTPUT,
                        ],
                    },
                    "output": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                    },
                },
            }
        )
    elif config is GGConfig:
        params.update(
            {
                "build_config_flags": [],
                "shape_profile": {
                    "input_image": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                    },
                    "grain_level": {
                        "min_shape": [config.MIN_BATCH_SIZE, 1, 1, 1],
                        "opt_shape": [config.OPT_BATCH_SIZE, 1, 1, 1],
                        "max_shape": [config.MAX_BATCH_SIZE, 1, 1, 1],
                    },
                    "grain_noise": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                    },
                    "output": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                    },
                },
            }
        )
    else:
        params.update(
            {
                "build_config_flags": [
                    trt.TRTBuilderFlag.FP16,
                ],
                "shape_profile": {
                    "input": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.input_shape,
                        ],
                    },
                    "output": {
                        "min_shape": [
                            config.MIN_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                        "opt_shape": [
                            config.OPT_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                        "max_shape": [
                            config.MAX_BATCH_SIZE,
                            *config.TRT_CONFIG.output_shape,
                        ],
                    },
                },
            }
        )
    return params


def build_and_upload_plan(
    model_name: str,
    shape_profile: dict[str, dict[str, list[int]]],
    build_config_flags: list[trt.TRTBuilderFlag],
    device: int = 0,
    onnx_model_file_name="model.onnx",
    plan_model_file_name="model.plan",
    downlaod_model_alias="newest",
):
    download_model_name = f"{model_name}#onnx"
    device_name = "nvidia-" + "-".join(
        s for s in trt.get_device_list()[0].split(":")[1].lower().split(" ")[2:-1]
    )
    if device_name.endswith("-d"):
        device_name = device_name[:-2]
    upload_model_name = f"{model_name}#{device_name}"
    upload_model_alias = "newest"

    number_of_devices = trt.get_device_count()
    assert number_of_devices > 0, "There is no NVIDIA GPUs."
    assert number_of_devices > device, f"device {device} is not exist."
    assert device > -1, f"device_id {device} is not exist."
    os.environ["CUDA_VISIBLE_DEVICES"] = str(device)

    upload_tag = {
        f"{io_name}.{shape_name}": str(shape_profile[io_name][shape_name])
        for io_name in shape_profile
        for shape_name in shape_profile[io_name]
    }
    for flag in build_config_flags:
        upload_tag.update({flag.name: ""})
    print(upload_tag)
    with tf.TemporaryDirectory() as temp_dir:
        print(f"Temporary Directory is {temp_dir}")
        model_manager = pmm.ModelManager(temp_dir)
        model_manager.download(
            model_name=download_model_name, alias=downlaod_model_alias
        )
        meta_data = pmm.MLFlowModel.load_metadata(
            model_manager.get_metadata_path(
                model_name=download_model_name, alias=downlaod_model_alias
            )
        )
        upload_tag["source_version"] = str(meta_data["version"])
        upload_tag["source_aliases"] = str(meta_data["aliases"])
        upload_tag["source_run_id"] = str(meta_data["run_id"])
        model_onnx_dir = model_manager.get_local_model_dir(
            model_name=download_model_name,
            alias=downlaod_model_alias,
        )
        model_plan_dir = model_manager.get_local_model_dir(
            model_name=upload_model_name,
            alias=upload_model_alias,
        )
        os.makedirs(model_plan_dir, exist_ok=False)
        onnx_model_path = os.path.join(model_onnx_dir, onnx_model_file_name)
        plan_model_path = os.path.join(model_plan_dir, plan_model_file_name)
        builder = trt.EngineBuilder()
        builder.build_from_onnx(
            onnx_path=onnx_model_path,
            plan_path=plan_model_path,
            config_flags=build_config_flags,
            shape_profiles=[
                trt.ShapeProfile(name=io_name, **shape_profile[io_name])
                for io_name in shape_profile
            ],
        )
        os.system(f"ls {os.path.dirname(plan_model_path)}")
        model_manager.upload(
            model_name=upload_model_name,
            model_dir=model_plan_dir,
            aliases=[upload_model_alias],
            tag=upload_tag,
        )
