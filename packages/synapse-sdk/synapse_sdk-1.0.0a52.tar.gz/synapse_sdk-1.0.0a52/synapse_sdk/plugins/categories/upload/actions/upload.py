import json
from datetime import datetime
from enum import Enum
from typing import Annotated, Dict, List

from pydantic import AfterValidator, BaseModel, field_validator
from pydantic_core import PydanticCustomError

from synapse_sdk.clients.exceptions import ClientError
from synapse_sdk.clients.utils import get_batched_list
from synapse_sdk.clients.validators.collections import FileSpecificationValidator
from synapse_sdk.i18n import gettext as _
from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod
from synapse_sdk.plugins.models import Run
from synapse_sdk.shared.enums import Context
from synapse_sdk.utils.pydantic.validators import non_blank
from synapse_sdk.utils.storage import get_pathlib


class UploadStatus(str, Enum):
    SUCCESS = 'success'
    FAILED = 'failed'


class UploadRun(Run):
    class DataFileLog(BaseModel):
        """Data file log model."""

        data_file_info: str | None
        status: UploadStatus
        created: str

    class DataUnitLog(BaseModel):
        """Data unit log model."""

        data_unit_id: int | None
        status: UploadStatus
        created: str

    class TaskLog(BaseModel):
        """Task log model."""

        task_id: int | None
        status: UploadStatus
        created: str

    def log_data_file(self, data_file_info: dict, status: UploadStatus):
        """Upload data_file log.

        Args:
            data_file_info (dict): The json info of the data file.
            checksum (str): The checksum of the data file.
            status (DataUnitStatus): The status of the data unit.
        """
        now = datetime.now().isoformat()
        self.log(
            'upload_data_file',
            self.DataFileLog(data_file_info=json.dumps(data_file_info), status=status.value, created=now).model_dump(),
        )

    def log_data_unit(self, data_unit_id: int, status: UploadStatus):
        """Upload data_unit log.

        Args:
            data_unit_id (int): The ID of the data unit.
            status (DataUnitStatus): The status of the data unit.
        """
        now = datetime.now().isoformat()
        self.log(
            'upload_data_unit',
            self.DataUnitLog(data_unit_id=data_unit_id, status=status.value, created=now).model_dump(),
        )

    def log_task(self, task_id: int, status: UploadStatus):
        """Upload task log.

        Args:
            task_id (int): The ID of the task.
            status (UploadStatus): The status of the task.
        """
        now = datetime.now().isoformat()
        self.log('upload_task', self.TaskLog(task_id=task_id, status=status.value, created=now).model_dump())


class UploadParams(BaseModel):
    """Upload action parameters.

    Args:
        name (str): The name of the action.
        description (str | None): The description of the action.
        checkpoint (int | None): The checkpoint of the action.
        path (str): The path of the action.
        storage (int): The storage of the action.
        collection (int): The collection of the action.
        project (int | None): The project of the action.
        is_generate_tasks (bool): The flag to generate tasks.
        is_generate_ground_truths (bool): The flag to generate ground truths
    """

    name: Annotated[str, AfterValidator(non_blank)]
    description: str | None
    path: str
    storage: int
    collection: int
    project: int | None

    @field_validator('storage', mode='before')
    @classmethod
    def check_storage_exists(cls, value: str, info) -> str:
        """Validate synapse-backend storage exists.

        TODO: Need to define validation method naming convention.
        TODO: Need to make validation method reusable.
        """
        action = info.context['action']
        client = action.client
        try:
            client.get_storage(value)
        except ClientError:
            raise PydanticCustomError('client_error', _('Error occurred while checking storage exists.'))
        return value

    @field_validator('collection', mode='before')
    @classmethod
    def check_collection_exists(cls, value: str, info) -> str:
        """Validate synapse-backend collection exists."""
        action = info.context['action']
        client = action.client
        try:
            client.get_dataset(value)
        except ClientError:
            raise PydanticCustomError('client_error', _('Error occurred while checking collection exists.'))
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
            raise PydanticCustomError('client_error', _('Error occurred while checking project exists.'))
        return value


@register_action
class UploadAction(Action):
    """Upload action class.

    Attrs:
        name (str): The name of the action.
        category (PluginCategory): The category of the action.
        method (RunMethod): The method to run of the action.

    Progress Categories:
        analyze_collection: The progress category for the analyze collection process.
        data_file_upload: The progress category for the upload process.
        generate_data_units: The progress category for the generate data units process.
    """

    name = 'upload'
    category = PluginCategory.UPLOAD
    method = RunMethod.JOB
    run_class = UploadRun
    progress_categories = {
        'analyze_collection': {
            'proportion': 10,
        },
        'upload_data_files': {
            'proportion': 50,
        },
        'generate_data_units': {
            'proportion': 40,
        },
    }

    def get_uploader(self, path):
        """Get uploader from entrypoint."""
        return self.entrypoint(self.run, path)

    def start(self) -> Dict:
        """Start upload process.

        Returns:
            Dict: The result of the upload process.
        """
        # Setup path object with path and storage.
        storage = self.client.get_storage(self.params['storage'])
        pathlib_cwd = get_pathlib(storage, self.params['path'])

        # Initialize uploader.
        uploader = self.get_uploader(pathlib_cwd)

        # Analyze Collection file specifications to determine the data structure for upload.
        file_specification_template = self._analyze_collection()

        # Setup result dict.
        result = {}

        # Organize data according to Collection file specification structure.
        organized_files = uploader.handle_upload_files()
        if not self._validate_organized_files(file_specification_template, organized_files):
            self.run.log_message('Validate organized files failed.')
            self.run.end_log()
            return result

        # Upload files to synapse-backend.
        organized_files_count = len(organized_files)
        if not organized_files_count:
            self.run.log_message('Files not found on the path.', context=Context.WARNING.value)
            self.run.end_log()
            return result
        uploaded_files = self._upload_files(organized_files, organized_files_count)
        result['uploaded_files_count'] = len(uploaded_files)

        # Generate data units for the uploaded data.
        upload_result_count = len(uploaded_files)
        if not upload_result_count:
            self.run.log_message('No files were uploaded.', context=Context.WARNING.value)
            self.run.end_log()
            return result
        generated_data_units = self._generate_data_units(uploaded_files, upload_result_count)
        result['generated_data_units_count'] = len(generated_data_units)

        self.run.end_log()
        return result

    def _analyze_collection(self) -> Dict:
        """Analyze Synapse Collection Specifications.

        Returns:
            Dict: The file specifications of the collection.
        """

        # Initialize progress
        self.run.set_progress(0, 1, category='analyze_collection')

        client = self.run.client
        collection_id = self.params['collection']
        collection = client.get_dataset(collection_id)

        # Finish progress
        self.run.set_progress(1, 1, category='analyze_collection')

        return collection['file_specifications']

    def _validate_organized_files(self, file_specification_template: Dict, organized_files: List) -> bool:
        """Validate organized files from Uploader."""
        validator = FileSpecificationValidator(file_specification_template, organized_files)
        return validator.validate()

    def _upload_files(self, organized_files, organized_files_count: int) -> List:
        """Upload files to synapse-backend.

        Returns:
            Dict: The result of the upload.
        """
        # Initialize progress
        self.run.set_progress(0, organized_files_count, category='upload_data_files')
        self.run.log_message('Uploading data files...')

        client = self.run.client
        collection_id = self.params['collection']
        upload_result = []
        organized_files_count = len(organized_files)
        current_progress = 0
        for organized_file in organized_files:
            uploaded_data_file = client.upload_data_file(organized_file, collection_id)
            self.run.log_data_file(organized_file, UploadStatus.SUCCESS)
            upload_result.append(uploaded_data_file)
            self.run.set_progress(current_progress, organized_files_count, category='upload_data_files')
            current_progress += 1

        # Finish progress
        self.run.set_progress(organized_files_count, organized_files_count, category='upload_data_files')
        self.run.log_message('Upload data files completed.')

        return upload_result

    def _generate_data_units(self, uploaded_files: List, upload_result_count: int) -> List:
        """Generate data units for the uploaded data.

        TODO: make batch size configurable.

        Returns:
            Dict: The result of the generate data units process.
        """
        # Initialize progress
        self.run.set_progress(0, upload_result_count, category='generate_data_units')

        client = self.run.client

        generated_data_units = []
        current_progress = 0
        batches = get_batched_list(uploaded_files, 100)
        batches_count = len(batches)
        for batch in batches:
            created_data_units = client.create_data_units(batch)
            generated_data_units.append(created_data_units)
            self.run.set_progress(current_progress, batches_count, category='generate_data_units')
            current_progress += 1
            for created_data_unit in created_data_units:
                self.run.log_data_unit(created_data_unit['id'], UploadStatus.SUCCESS)

        # Finish progress
        self.run.set_progress(upload_result_count, upload_result_count, category='generate_data_units')

        return sum(generated_data_units, [])
