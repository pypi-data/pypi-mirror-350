from typing import Any
import pytest
from pipelining.core.pipeline import Pipeline
from tests.conftest import DummyStage


@pytest.mark.parametrize("with_tqdm", [True, False])
def test_pipeline_runs_all_stages_in_order(with_tqdm: bool) -> None:
    s1 = DummyStage("s1", lambda c: c.update({"s1": True}))
    s2 = DummyStage("s2", lambda c: c.update({"s2": True}))
    pipeline = Pipeline([s1, s2], name="TestPipeline")

    result = pipeline.run(use_tqdm=with_tqdm)

    assert result["s1"] is True
    assert result["s2"] is True


def test_pipeline_raises_on_stage_failure() -> None:
    def fail_action(context: dict[str, Any]) -> None:
        raise Exception("Stage failed")

    s1 = DummyStage("s1", fail_action)
    pipeline = Pipeline([s1], name="TestPipeline")

    with pytest.raises(Exception, match="Stage failed"):
        pipeline.run()
