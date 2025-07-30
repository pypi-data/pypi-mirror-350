from pathlib import Path
from typing import List


class Uploader:
    """Plugin upload action class.

    * Organize, upload, setup task, generate ground truths for the uploaded data.
    """

    def __init__(self, run, path: Path, *args, **kwargs):
        """Initialize the plugin upload action class.

        Args:
            run: Plugin run object.
            path: pathlib object by upload target destination path.
        """
        self.run = run
        self.path = path

    def handle_upload_files(self) -> List:
        """Handle upload files.

        * Organize data according to collection file specification structure.
        * Structure files according to the file specification of the target collection.

        Returns:
            List: List of dictionaries containing 'files' and 'meta'.

        Examples:
            [
              {
          "files": {
              'image_1': image_1_pathlib_object,
              'image_2': image_2_pathlib_object,
              'meta_1': meta_1_pathlib_object,
          },
          "meta": {
            "key": "value"
          }
              }
            ]
        """
        return []
