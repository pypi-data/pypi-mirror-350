from logging import INFO, getLogger
from typing import Any, Iterable

from tqdm.rich import tqdm

from pipelining.core.stage import Stage
from pipelining.util.logger import configure_logging


class Pipeline:
    """
    Orchestrates execution of an ordered list of pipeline stages.

    A single “root” logger is created for the pipeline (named by `name`),
    and each stage receives a child logger before it runs. All stages share
    a common context dict.

    Parameters
    ----------
    stages : list[Stage]
        A list of stages to be executed
    name : str, optional
        A name for the pipeline, by default "Pipeline"
    log_level : int, optional
        The logging level for the pipeline, by default INFO

    Attributes
    ----------
    stages : list of Stage
        The sequence of stage instances to execute.
    logger : logging.Logger
        Root logger for the entire pipeline, configured by the application.
    name : str
        Name of the pipeline, used for logging and identification.
    """

    def __init__(
        self, stages: Iterable[Stage], name: str = "Pipeline", log_level: int = INFO
    ) -> None:
        """
        Initialize the Pipeline with a list of stages and a logger.

        Parameters
        ----------
        stages : Iterable[Stage]
            A list of stages to be executed
        name : str, optional
            A name for the pipeline, by default "Pipeline"
        log_level : int, optional
            The logging level for the pipeline, by default INFO
        """
        configure_logging(log_level)

        self.logger = getLogger(name)
        self.stages: list[Stage] = list(stages)
        self.name = name

    def run(
        self, context: dict[str, Any] | None = None, use_tqdm: bool = False
    ) -> dict[str, Any]:
        """
        Execute all stages in sequence.

        This will:
        1. Initialise or reuse the provided context dict.
        2. Store the pipeline's root logger in `context['logger']`.
        3. For each stage, inject a child logger (`pipeline_name.StageClass`)
            into `stage.logger`, call `stage.run(context)`, and log status.

        Parameters
        ----------
        context : dict, optional
            Initial shared context for stages (default is a new empty dict).

        Returns
        -------
        dict
            The context dict after all stages have run.

        Raises
        ------
        Exception
            Re-raises any exception from a stage after logging it.
        """
        context = context or {}
        context["logger"] = self.logger

        self.logger.info(f"Starting {self.name}")

        if use_tqdm:
            with tqdm(
                self.stages, desc="Pipeline Progress", unit="stage"
            ) as progress_bar:
                for stage in progress_bar:
                    self._run_stage(stage, context)
        else:
            for stage in self.stages:
                self._run_stage(stage, context)

        self.logger.info(f"{self.name} completed successfully!")
        return context

    def _run_stage(self, stage: Stage, context: dict[str, Any]) -> None:
        """
        Run a single stage with the provided context.

        Parameters
        ----------
        stage : Stage
            The stage to run.
        context : dict
            The context to pass to the stage.
        """
        stage_name = stage.__class__.__name__
        stage.logger = self.logger.getChild(stage_name)

        self.logger.info(f"Running stage: {stage_name}")

        try:
            stage.run(context)
        except Exception as e:
            self.logger.error(f"Error in stage {stage_name}: {e}")
            raise

        self.logger.info(f"Stage {stage_name} completed successfully!")
