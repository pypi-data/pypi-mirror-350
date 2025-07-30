from __future__ import annotations

from enum import Enum


class EntityKinds(Enum):
    """
    Entity kinds.
    """

    FUNCTION_HUGGINGFACESERVE = "huggingfaceserve"
    TASK_HUGGINGFACESERVE_SERVE = "huggingfaceserve+serve"
    RUN_HUGGINGFACESERVE = "huggingfaceserve+run"

    FUNCTION_MLFLOWSERVE = "mlflowserve"
    TASK_MLFLOWSERVE_SERVE = "mlflowserve+serve"
    RUN_MLFLOWSERVE = "mlflowserve+run"

    FUNCTION_SKLEARNSERVE = "sklearnserve"
    TASK_SKLEARNSERVE_SERVE = "sklearnserve+serve"
    RUN_SKLEARNSERVE = "sklearnserve+run"

    FUNCTION_KUBEAISERVE = "kubeaiserve"
    TASK_KUBEAISERVE_SERVE = "kubeaiserve+serve"
    RUN_KUBEAISERVE = "kubeaiserve+run"


class TaskActions(Enum):
    """
    Task actions.
    """

    SERVE = "serve"
