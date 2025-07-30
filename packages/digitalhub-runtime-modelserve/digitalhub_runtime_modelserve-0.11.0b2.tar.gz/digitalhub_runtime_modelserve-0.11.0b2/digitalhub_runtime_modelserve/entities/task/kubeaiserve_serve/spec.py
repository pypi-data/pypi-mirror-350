from __future__ import annotations

from digitalhub_runtime_modelserve.entities.task.modelserve_serve.spec import (
    TaskSpecModelserveServe,
    TaskValidatorModelserveServe,
)


class TaskSpecKubeaiserveServe(TaskSpecModelserveServe):
    """
    TaskSpecKubeaiserveServe specifications.
    """


class TaskValidatorKubeaiserveServe(TaskValidatorModelserveServe):
    """
    TaskValidatorKubeaiserveServe validator.
    """
