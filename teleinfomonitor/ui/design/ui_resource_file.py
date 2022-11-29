from pathlib import Path


class UiResourceFile:

    def __init__(self, file_name: str):
        super(UiResourceFile, self).__init__()
        self.path = Path(__file__).parent / file_name

    def __str__(self):
        return str(self.path)
