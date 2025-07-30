import importlib


class ManifestProcessor:
    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path
        self._module = importlib.import_module(self.manifest_path)

        self.system = self._module.system

    def get_roles(self):
        return self.system.roles

    def get_subsystems(self):
        return self.system.subsystems

    def get_entities(self):
        return self.system.entities
