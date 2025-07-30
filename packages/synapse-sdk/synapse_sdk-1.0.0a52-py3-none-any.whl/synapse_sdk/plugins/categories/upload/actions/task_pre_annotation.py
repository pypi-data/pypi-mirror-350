from enum import Enum
from typing import Annotated

from pydantic import AfterValidator, BaseModel, field_validator
from pydantic_core import PydanticCustomError

from synapse_sdk.clients.exceptions import ClientError
from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod
from synapse_sdk.plugins.models import Run
from synapse_sdk.utils.pydantic.validators import non_blank


class TaskDataAnnotationType(str, Enum):
    FILE = 'file'
    INFERENCE = 'inference'


class TaskPreAnnotationRun(Run):
    pass


class TaskPreAnnotationParams(BaseModel):
    """TaskPreAnnotation action parameters.

    Args:
        name (str): The name of the action.
        description (str | None): The description of the action.
        project (int): The project ID.
        data_collection (int): The data collection ID.
        task_data_annotation_type (TaskDataAnnotationType): The type of task data annotation.
    """

    name: Annotated[str, AfterValidator(non_blank)]
    description: str | None
    project: int
    data_collection: int
    task_data_annotation_type: TaskDataAnnotationType

    @field_validator('data_collection', mode='before')
    @classmethod
    def check_data_collection_exists(cls, value: str, info) -> str:
        """Validate synapse-backend collection exists."""
        action = info.context['action']
        client = action.client
        try:
            client.get_dataset(value)
        except ClientError:
            raise PydanticCustomError('client_error', 'Error occurred while checking data collection exists.')
        return value

    @field_validator('project', mode='before')
    @classmethod
    def check_project_exists(cls, value: str, info) -> str:
        """Validate synapse-backend project exists."""
        if not value:
            return value

        action = info.context['action']
        client = action.client
        try:
            client.get_project(value)
        except ClientError:
            raise PydanticCustomError('client_error', 'Error occurred while checking project exists.')
        return value


@register_action
class TaskPreAnnotationAction(Action):
    """TaskPreAnnotation action class.

    * Annotate data to tasks.
    """

    name = 'task_pre_annotation'
    category = PluginCategory.UPLOAD
    method = RunMethod.JOB
    run_class = TaskPreAnnotationRun
    progress_categories = {
        'generate_tasks': {
            'proportion': 10,
        },
        'annotate_task_data': {
            'proportion': 90,
        },
    }

    def start(self):
        """Start task_pre_annotation action.

        * Generate tasks.
        * Annotate data to tasks.
        """
        task_pre_annotation = self.get_task_pre_annotation()
        task_pre_annotation.handle_annotate_data_from_files()
        return {}

    def get_task_pre_annotation(self):
        """Get task pre annotation entrypoint."""
        return self.entrypoint()
