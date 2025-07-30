import argparse

from ddjcm.code_collector import CodeCollector
from ddjcm.config import Config
from ddjcm.entities import Entity
from ddjcm.project import set_templates_directory
from ddjcm.profiles_manager import ProfilesManager
from ddjcm.subsystem_manager import SubsystemManager
from ddjcm.manifest_processor import ManifestProcessor
from ddjcm.templates_manager import save_tags, save_templates


class CompactHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def __init__(self, *args, **kwargs):
        kwargs["width"] = 100
        kwargs["max_help_position"] = 30
        super().__init__(*args, **kwargs)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)
        return ", ".join(action.option_strings)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="DDJCM",
        description="It is 1C in Django world",
        epilog="Good luck!",
        formatter_class=CompactHelpFormatter
    )

    argparser.add_argument(
        "--manifest",
        help="path to manifest file",
        default="manifest.py"
    )
    argparser.add_argument(
        "--create-app-command",
        help="command to create an app",
        default="python3 manage.py startapp {app_name}"
    )
    argparser.add_argument(
        "--encoding",
        help="encoding for opening and writing files",
        default="utf-8"
    )
    argparser.add_argument(
        "--guard-start-comment",
        help="acomment to mark beginning of generated code",
        default="# <<<\n"
    )
    argparser.add_argument(
        "--guard-end-comment",
        help="acomment to mark end of generated code",
        default="\n# >>>"
    )

    args = argparser.parse_args()

    config = Config(
        create_app_command=args.create_app_command,
        encoding=args.encoding,
        guard_start_comment=args.guard_start_comment,
        guard_end_comment=args.guard_end_comment
    )

    set_templates_directory(config)
    save_templates(config)

    manifest_processor = ManifestProcessor(args.manifest.split(".")[0])

    for subsystem in manifest_processor.get_subsystems():
        save_tags(subsystem, config)

    code_collector = CodeCollector(config)

    profiles_manager = ProfilesManager(roles=manifest_processor.get_roles(), code_collector=code_collector, config=config)

    profiles_manager.create_app()
    profiles_manager.create_model()
    profiles_manager.create_forms()
    profiles_manager.create_views()
    profiles_manager.save_urls()

    subsystem_manager = SubsystemManager(manifest_processor.get_subsystems(), code_collector, config)
    subsystem_manager.create_apps()
    subsystem_manager.create_dashboard(manifest_processor.get_roles())

    entity: Entity
    for name, entity in manifest_processor.get_entities().items():
        entity.set_name(name)
        entity.set_config(config)
        entity.set_roles(manifest_processor.get_roles())
        entity.set_code_collector(code_collector)

        entity.create_model()

        entity.save_forms()
        entity.save_views()
        entity.register_urls()

    subsystem_manager.create_entities_lists(manifest_processor.get_entities(), manifest_processor.get_roles())

    code_collector.write()
