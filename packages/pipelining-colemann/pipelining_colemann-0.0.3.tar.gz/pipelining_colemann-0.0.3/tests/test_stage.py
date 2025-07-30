from typing import Any
import pytest

from pipelining.core.stage import Stage
from tests.conftest import DummyStage


def test_stage_is_abstract() -> None:
    with pytest.raises(TypeError):
        Stage("test")  # type: ignore


def test_bad_subclass() -> None:
    class PartialStage(Stage):
        pass

    with pytest.raises(TypeError):
        PartialStage()  # type: ignore


def test_stage_run_method() -> None:
    dummy_stage = DummyStage("test", lambda c: c.update({"ran": True}))

    context: dict[str, Any] = {}
    dummy_stage.run(context)

    assert context["ran"] is True
