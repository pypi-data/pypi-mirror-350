import logging
import warnings
from rich.logging import RichHandler
from rich.traceback import install
from tqdm import TqdmExperimentalWarning

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)


def configure_logging(level: int = logging.INFO) -> None:
    """
    Set up RichHandler on the root logger for pretty, coloured output.

    Parameters
    ----------
    level : int, optional
        Minimum log level (default: INFO).
    """

    # avoid adding multiple handlers if called more than once
    root = logging.getLogger()

    if any(isinstance(h, RichHandler) for h in root.handlers):
        return

    install(show_locals=True)

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        handlers=[
            RichHandler(show_time=True, show_level=True, show_path=False, markup=True)
        ],
    )
