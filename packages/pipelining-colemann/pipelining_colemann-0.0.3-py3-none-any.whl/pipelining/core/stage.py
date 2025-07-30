from abc import ABC, abstractmethod
from logging import Logger, getLogger
from typing import Any


class Stage(ABC):
    """
    Base class for a single pipeline stage.

    Subclasses must implement the `run` method. Before execution,
    the Pipeline will inject a per-stage logger into the `logger`
    attribute.

    Parameters
    ----------
    name : str
        A name for the stage.

    Attributes
    ----------
    logger : logging.Logger
        Logger instance for this stage, injected by the Pipeline.
    name : str
        Name of the stage, used for logging and identification.
    """

    def __init__(self, name: str) -> None:
        self.logger: Logger = getLogger("undefined")
        self.name = name

    @abstractmethod
    def run(self, context: dict[str, Any]) -> None:
        """
        Run the stage's logic.

        Parameters
        ----------
        context : dict
            Shared context dictionary that carries data between stages.

        Raises
        ------
        Exception
            Any exception raised here will be caught and re-raised by the Pipeline
            after logging.
        """
