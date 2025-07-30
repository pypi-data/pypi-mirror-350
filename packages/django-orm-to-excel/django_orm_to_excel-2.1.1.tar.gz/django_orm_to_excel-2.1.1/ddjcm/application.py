import os
from pathlib import Path

from ddjcm.config import Config
from ddjcm.project import get_project_name


class App:
    def __init__(self, app_name: str, config: Config):
        self.app_name = app_name
        self.config = config

    def create(self):
        if not self._is_exists():
            os.system(self.config.create_app_command.format(app_name=self.app_name))

        self._register()
        self._register_urls()

    def _register(self):
        settings_path = Path(get_project_name()) / "settings.py"

        settings_content = settings_path.read_text(encoding=self.config.encoding)
        settings_lines = settings_content.split("\n")

        installed_apps_start = settings_lines.index("INSTALLED_APPS = [") + 1
        installed_apps_end = installed_apps_start + settings_lines[installed_apps_start:].index("]")

        for line in settings_lines[installed_apps_start:installed_apps_end]:
            if f"'{self.app_name}'" in line:
                break
        else:
            settings_lines.insert(installed_apps_end, f"    '{self.app_name}',")

        settings_path.write_text("\n".join(settings_lines), encoding=self.config.encoding)

    def _register_urls(self):
        global_urls_path = Path(get_project_name()) / "urls.py"

        global_urls_content = global_urls_path.read_text(encoding=self.config.encoding)
        global_urls_lines = global_urls_content.split("\n")

        urlpatterns_start = global_urls_lines.index("urlpatterns = [") + 1
        urlpatterns_end = urlpatterns_start + global_urls_lines[urlpatterns_start:].index("]")

        registered_url = f"path('{self.app_name}/', include('{self.app_name}.urls')),"
        for line in global_urls_lines[urlpatterns_start:urlpatterns_end]:
            if registered_url in line:
                break
        else:
            global_urls_lines.insert(urlpatterns_end, f"    {registered_url}")

        if "from django.conf.urls import include" not in global_urls_lines:
            global_urls_lines = ["from django.conf.urls import include"] + global_urls_lines

        global_urls_path.write_text("\n".join(global_urls_lines), encoding=self.config.encoding)

    def _is_exists(self) -> bool:
        return Path(self.app_name).is_dir() and self._is_dir_app(Path(self.app_name))

    def _is_dir_app(self, path: Path) -> bool:
        return (path / "admin.py").is_file()
