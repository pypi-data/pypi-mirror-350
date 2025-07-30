from pathlib import Path

from ddjcm.config import Config
from ddjcm.project import get_project_name


class TemplatesManager:
    def __init__(self, app_name: str, config: Config):
        self.app_name = app_name
        self.config = config

    def write(self, template_name: str, code: str):
        path = Path(self.app_name) / "templates" / template_name
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()

        path.write_text(code, encoding=self.config.encoding)

    def write_tags(self, tags: str):
        path = Path(self.app_name) / "templatetags" / "helpers.py"
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()

        tags = "from django import template\n\nregister = template.Library()\n\n" + tags

        path.write_text(tags, encoding=self.config.encoding)
        path = Path(self.app_name) / "templatetags" / "__init__.py"
        path.touch()


def save_templates(config: Config):
    templates = TemplatesManager("", config)
    templates.write("base.html", """
        <!DOCTYPE html>
        <html data-theme="light">
        <head>
            <meta charset="utf-8" />
            <title>""" + get_project_name() + """</title>
            <!-- <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css"> -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/yegor256/tacit@gh-pages/tacit-css-1.9.0.min.css"/>
        </head>
        <body>
            <h1>{% block header %}{% endblock header %}</h1>
            <div>{% block content %}{% endblock content %}</div>
        </body>
        </html>
    """)

    html_templates_path = Path("..") / "ddjcm" / Path("ddjcm") / "html_templates"
    templates.write("dashboard.html", (html_templates_path / "dashboard.html").read_text(encoding=config.encoding))
    templates.write("list.html", (html_templates_path / "list.html").read_text(encoding=config.encoding))
    templates.write("info.html", (html_templates_path / "info.html").read_text(encoding=config.encoding))
    templates.write("create.html", (html_templates_path / "create.html").read_text(encoding=config.encoding))
    templates.write("edit.html", (html_templates_path / "edit.html").read_text(encoding=config.encoding))


def save_tags(app: str, config: Config):
    templates = TemplatesManager(app, config)

    tags = []

    tags.append("""@register.filter\ndef get_item(obj, value):\n    return obj[value]""")
    tags.append("""@register.filter\ndef get_label_tag(obj, value):\n    return obj[value].label_tag()""")

    templates.write_tags("\n\n".join(tags))

