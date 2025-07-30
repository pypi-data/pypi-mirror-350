from __future__ import annotations

from digitalhub.entities._base.runtime_entity.builder import RuntimeEntityBuilder
from digitalhub.entities.task._base.utils import build_task_actions

from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds, TaskActions


class RuntimeEntityBuilderMlflowserve(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_MLFLOWSERVE.value
    TASKS_KINDS = build_task_actions(
        [
            (
                EntityKinds.TASK_MLFLOWSERVE_SERVE.value,
                TaskActions.SERVE.value,
            ),
        ]
    )
    RUN_KIND = EntityKinds.RUN_MLFLOWSERVE.value


class RuntimeEntityBuilderSklearnserve(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_SKLEARNSERVE.value
    TASKS_KINDS = build_task_actions(
        [
            (
                EntityKinds.TASK_SKLEARNSERVE_SERVE.value,
                TaskActions.SERVE.value,
            ),
        ]
    )
    RUN_KIND = EntityKinds.RUN_SKLEARNSERVE.value


class RuntimeEntityBuilderHuggingfaceserve(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_HUGGINGFACESERVE.value
    TASKS_KINDS = build_task_actions(
        [
            (
                EntityKinds.TASK_HUGGINGFACESERVE_SERVE.value,
                TaskActions.SERVE.value,
            ),
        ]
    )
    RUN_KIND = EntityKinds.RUN_HUGGINGFACESERVE.value


class RuntimeEntityBuilderKubeaiserve(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_KUBEAISERVE.value
    TASKS_KINDS = build_task_actions(
        [
            (
                EntityKinds.TASK_KUBEAISERVE_SERVE.value,
                TaskActions.SERVE.value,
            ),
        ]
    )
    RUN_KIND = EntityKinds.RUN_KUBEAISERVE.value
