from .processor.dpir.processor import DPIRProcessor
from .processor.dru_rbpn_sr_f3.processor import DRURBPNSRF3Processor
from .processor.dru_rbpn_sr_f5.processor import DRURBPNSRF5Processor
from .processor.dru_asm_sr_f3.processor import DRUASMSRF3Processor
from .processor.dru_rbpn_deinter_f3_gloss.processor import (
    DRURBPNDEINTERF3GLOSSProcessor,
)
from .processor.dru_rbpn_deinter_pc_f2.processor import DRURBPNDEINTERPCF2Processor
from .processor.fisf.processor import FISFProcessor
from .processor.color_resnet.processor_pre import COLORRESNETPREProcessor
from .processor.color_resnet.processor_post import COLORRESNETPOSTProcessor
from .processor.gg.processor import GGProcessor
from .processor.col_en.processor import COLENProcessor
from .processor.cdru_f2.processor import CDRUF2Processor


__all__: list[str] = [
    "DPIRProcessor",
    "DRURBPNSRF3Processor",
    "DRURBPNSRF5Processor",
    "DRUASMSRF3Processor",
    "DRURBPNDEINTERF3GLOSSProcessor",
    "DRURBPNDEINTERPCF2Processor",
    "FISFProcessor",
    "COLORRESNETPREProcessor",
    "COLORRESNETPOSTProcessor",
    "GGProcessor",
    "COLENProcessor",
    "CDRUF2Processor",
]

__version__ = "2.7.0"
