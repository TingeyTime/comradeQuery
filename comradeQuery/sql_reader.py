class SQLReader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.content = ""

    def read_file(self) -> str:
        with open(self.file_path, 'r') as f:
            self.content = f.read()

        return self.content