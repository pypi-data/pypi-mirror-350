from pathlib import Path

from ddjcm.config import Config


def get_project_name() -> str:
    return Path.cwd().name


def set_templates_directory(config: Config):
    settings_path = Path(get_project_name()) / "settings.py"

    settings_content = settings_path.read_text(encoding=config.encoding)
    settings_lines = settings_content.split("\n")

    new_lines = []

    for line in settings_lines:
        if "'DIRS': []" in line:
            new_lines.append("        'DIRS': [BASE_DIR / 'templates'],")
        else:
            new_lines.append(line)

    settings_path.write_text("\n".join(new_lines), encoding=config.encoding)
