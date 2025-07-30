from typing import Any, Callable
from pipelining.core.stage import Stage


class DummyStage(Stage):
    """
    A dummy stage for testing purposes.

    This stage does not perform any actual processing but serves as a
    placeholder in the pipeline. It can be used to test the pipeline's
    execution flow without implementing real logic.

    Parameters
    ----------
    name : str
        The name of the stage.
    """

    def __init__(self, name: str, action: Callable) -> None:
        super().__init__(name)
        self.name = name
        self.action = action

    def run(self, context: dict[str, Any]) -> None:
        context.setdefault("order", []).append(self.name)

        if callable(self.action):
            self.action(context)


class LogStage(Stage):
    """
    A logging stage for testing purposes.

    This stage does not perform any actual processing but serves as a
    placeholder in the pipeline. It can be used to test the pipeline's
    execution flow without implementing real logic.

    Parameters
    ----------
    name : str
        The name of the stage.
    """

    def __init__(self, name: str, message: str) -> None:
        super().__init__(name)
        self.name = name
        self.message = message

    def run(self, _: dict) -> None:
        self.logger.info(self.message)
