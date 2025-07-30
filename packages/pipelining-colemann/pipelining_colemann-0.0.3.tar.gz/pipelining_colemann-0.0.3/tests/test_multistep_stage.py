import time
from typing import Any, Callable

import pytest
from pipelining.core.multistep_stage import MultiStepStage


# Dummy step function that writes to context
def make_step(name: str, delay: float = 0.1) -> Callable:
    def step(context):
        time.sleep(delay)
        context[name] = f"{name}_done"

    return step


def test_sequential_execution() -> None:
    context: dict[str, Any] = {}
    steps = [make_step("a"), make_step("b"), make_step("c")]
    stage = MultiStepStage(name="TestSequential", steps=steps)

    stage.run(context)

    assert context == {"a": "a_done", "b": "b_done", "c": "c_done"}


def test_parallel_execution() -> None:
    context: dict[str, Any] = {}
    steps = [make_step("x"), make_step("y"), make_step("z")]
    stage = MultiStepStage(name="TestParallel", steps=steps, parallel=True)

    stage.run(context)

    assert set(context.keys()) == {"x", "y", "z"}
    assert all(value.endswith("_done") for value in context.values())


@pytest.mark.parametrize("parallel", [True, False])
def test_step_exception_raised(parallel: bool) -> None:
    def bad_step(_):
        raise ValueError("Boom!")

    stage = MultiStepStage("TestError", [bad_step], parallel=parallel)

    with pytest.raises(ValueError, match="Boom!"):
        stage.run(context={})
