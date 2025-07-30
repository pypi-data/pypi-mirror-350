from multiprocessing import Pool
from pathlib import Path
from typing import Dict, Optional

from tqdm import tqdm

from synapse_sdk.clients.base import BaseClient
from synapse_sdk.clients.utils import get_batched_list


class DatasetClientMixin(BaseClient):
    def list_dataset(self):
        path = 'datasets/'
        return self._list(path)

    def get_dataset(self, dataset_id):
        """Get dataset from synapse-backend.

        Args:
            dataset_id: The dataset id to get.
        """
        path = f'datasets/{dataset_id}/?expand=file_specifications'
        return self._get(path)

    def create_data_file(self, file_path: Path):
        """Create data file to synapse-backend.

        Args:
            file_path: The file pathlib object to upload.
        """
        path = 'data_files/'
        return self._post(path, files={'file': file_path})

    def create_data_units(self, data):
        """Create data units to synapse-backend.

        Args:
            data: The data bindings to upload from create_data_file interface.
        """
        path = 'data_units/'
        return self._post(path, data=data)

    def upload_dataset(
        self,
        dataset_id: int,
        dataset: Dict,
        project_id: Optional[int] = None,
        batch_size: int = 1000,
        process_pool: int = 10,
    ):
        """Upload dataset to synapse-backend.

        Args:
            dataset_id: The dataset id to upload the data to.
            dataset: The dataset to upload.
                * structure:
                    - files: The files to upload. (key: file name, value: file pathlib object)
                    - meta: The meta data to upload.
            project_id: The project id to upload the data to.
            batch_size: The batch size to upload the data.
            process_pool: The process pool to upload the data.
        """
        # TODO validate dataset with schema

        params = [(data, dataset_id) for data in dataset]

        with Pool(processes=process_pool) as pool:
            dataset = pool.starmap(self.upload_data_file, tqdm(params))

        batches = get_batched_list(dataset, batch_size)

        for batch in tqdm(batches):
            data_units = self.create_data_units(batch)

            if project_id:
                tasks_data = []
                for data, data_unit in zip(batch, data_units):
                    task_data = {'project': project_id, 'data_unit': data_unit['id']}
                    # TODO: Additional logic needed here if task data storage is required during import.

                    tasks_data.append(task_data)

                self.create_tasks(tasks_data)

    def upload_data_file(self, data: Dict, dataset_id: int) -> Dict:
        """Upload files to synapse-backend.

        Args:
            data: The data to upload.
                * structure:
                    - files: The files to upload. (key: file name, value: file pathlib object)
                    - meta: The meta data to upload.
            dataset_id: The dataset id to upload the data to.

        Returns:
            Dict: The result of the upload.
        """
        for name, path in data['files'].items():
            data_file = self.create_data_file(path)
            data['dataset'] = dataset_id
            data['files'][name] = {'checksum': data_file['checksum'], 'path': str(path)}
        return data
