class TaskPreAnnotation:
    def __init__(self, run, *args, **kwargs):
        """Initialize the plugin task pre annotation action class.

        Args:
            run: Plugin run object.
        """
        self.run = run

    def handle_annotate_data_from_files(self):
        pass

    def handle_annotate_data_with_inference(self):
        pass
