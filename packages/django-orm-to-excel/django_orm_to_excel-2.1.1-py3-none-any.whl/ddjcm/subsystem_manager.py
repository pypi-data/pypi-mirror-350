from pathlib import Path
import typing as t

from ddjcm.application import App
from ddjcm.code_collector import CodeCollector
from ddjcm.code_writer import CodeWriter
from ddjcm.config import Config
from ddjcm.entities import Entity
from ddjcm.project import get_project_name
from ddjcm.templates_manager import TemplatesManager
from ddjcm.url_manager import UrlManager
from ddjcm.view_generator import ViewGenerator


class SubsystemManager:
    def __init__(self, subsystems: dict[str, dict[str, t.Any]], code_collector: CodeCollector, config: Config):
        self.subsystems = subsystems
        self.code_collector = code_collector
        self.config = config

        self.vg = ViewGenerator(self.config)

    def create_apps(self):
        for subsystem in self.subsystems.keys():
            app = App(subsystem, self.config)
            app.create()

    def create_dashboard(self, roles: list[str]):
        items = {
            role: [
                dict(slug=subsystem_name, name=subsystem["name"])
                for subsystem_name, subsystem in self.subsystems.items()
                if subsystem["permission"].can_view(role)
            ]
            for role in roles
        }

        view = self.vg.get_dashboard_view(subsystem="", model_name="main", title="Главная", items=items, import_render=True)

        url_manager = UrlManager(get_project_name(), self.code_collector, self.config)

        url_manager.register_url(f"subsystems", "main_dashboard_view")
        url_manager.save_urls(append=True)

        self.code_collector.collect(get_project_name(), "views.py", view)
        CodeWriter(Path(get_project_name()) / "views.py", self.config).write(view)

    def create_entities_lists(self, entities: dict[str, Entity], roles: list[str]):
        for subsystem_name, subsystem in self.subsystems.items():
            owned_entities = list(filter(lambda e: e.subsystem == subsystem_name, entities.values()))

            items = {}

            for own_entity in owned_entities:
                for role in roles:
                    items.setdefault(role, [])
                    items[role] += [
                        dict(slug=list_name, name=list_["name"])
                        for list_name, list_ in own_entity.lists.items()
                        if list_["permission"].can_view(role)
                    ]

            view = self.vg.get_dashboard_view(subsystem_name, subsystem_name, title=subsystem["name"], items=items)

            url_manager = UrlManager(subsystem_name, self.code_collector, self.config)

            url_manager.register_url(f"", f"{subsystem_name}_dashboard_view")
            url_manager.save_urls(append=True)

            self.code_collector.collect(subsystem_name, "views.py", view)
            # CodeWriter(Path(subsystem_name) / "views.py", self.config).write(view)
