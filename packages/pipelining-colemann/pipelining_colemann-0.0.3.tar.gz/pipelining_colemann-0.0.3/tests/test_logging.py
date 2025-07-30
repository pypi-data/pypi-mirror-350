import logging
from pytest import LogCaptureFixture
import pytest
from rich.logging import RichHandler

from pipelining.core.pipeline import Pipeline
from pipelining.util.logger import configure_logging
from tests.conftest import LogStage


def test_configure_logging_adds_rich_handler() -> None:
    """
    configure_logging should add a RichHandler to the root logger,
    and be idempotent (not add duplicates on repeated calls).
    """
    root = logging.getLogger()

    # Clear existing handlers
    root.handlers.clear()

    # First call: should add one RichHandler
    configure_logging(level=logging.INFO)
    handlers = [h for h in root.handlers if isinstance(h, RichHandler)]
    assert len(handlers) == 1, "Expected one RichHandler after first configure"

    # Second call: still only one RichHandler
    configure_logging(level=logging.DEBUG)
    handlers2 = [h for h in root.handlers if isinstance(h, RichHandler)]
    assert len(handlers2) == 1, "Expected configure_logging to be idempotent"


@pytest.mark.parametrize(
    "expected_messages",
    [
        [
            "Starting root",
            "Running stage: LogStage",
            "Hello World",
            "Stage LogStage completed successfully!",
            "root completed successfully!",
        ]
    ],
)
def test_pipeline_and_stage_logging(
    expected_messages: list[str], caplog: LogCaptureFixture
) -> None:
    """
    Pipeline should inject child loggers and emit logs with correct names and levels.
    """
    pipeline = Pipeline([LogStage("LogStage", "Hello World")], name="root")
    pipeline.run()

    messages = caplog.messages

    assert expected_messages == messages, (
        "Expected messages do not match actual messages"
    )
