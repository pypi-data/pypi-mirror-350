from __future__ import annotations

from digitalhub_runtime_modelserve.entities.run.modelserve_run.spec import (
    RunSpecModelserveRun,
    RunValidatorModelserveRun,
)


class RunSpecMlflowserveRun(RunSpecModelserveRun):
    """RunSpecMlflowserveRun specifications."""


class RunValidatorMlflowserveRun(RunValidatorModelserveRun):
    """RunValidatorMlflowserveRun validator."""
