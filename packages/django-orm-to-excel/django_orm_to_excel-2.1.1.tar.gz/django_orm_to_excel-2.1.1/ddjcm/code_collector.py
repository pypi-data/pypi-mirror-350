from pathlib import Path

from ddjcm.code_writer import CodeWriter
from ddjcm.config import Config


class CodeCollector:
    def __init__(self, config: Config):
        self.code = {}
        self.config = config

    def collect(self, subsystem_name: str, file: str, code: str):
        self.code.setdefault(subsystem_name, {})
        self.code[subsystem_name].setdefault(file, [])

        self.code[subsystem_name][file].append(code)

    def write(self):
        for subsystem_name, files in self.code.items():
            for file_name, content in files.items():
                CodeWriter(Path(subsystem_name) / file_name, self.config).write("\n\n".join(content))
