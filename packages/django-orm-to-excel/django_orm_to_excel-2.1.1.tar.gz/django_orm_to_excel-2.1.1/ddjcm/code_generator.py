import jinja2 as j2


class CodeUnit:
    def __init__(self, env: j2.Environment, template_name: str):
        self.template = env.get_template(template_name)

    def __call__(self, **kwargs) -> str:
        return self.template.render(**kwargs)


def nested(body: list[str]) -> str:
    res = "\n    ".join("\n".join(body).split("\n"))
    return res


class TemplatedCodeGenerator:
    def __init__(self):
        self.env = j2.Environment(
            loader = j2.FileSystemLoader("../ddjcm/ddjcm/ddjcm_templates"),
        )
        self.env.filters["nested"] = nested

    def get_builder(self, template_name: str) -> CodeUnit:
        return CodeUnit(self.env, template_name)


__tcg = TemplatedCodeGenerator()

Call = __tcg.get_builder("call.j2")
Class = __tcg.get_builder("class.j2")
Import = __tcg.get_builder("import.j2")
Ellipse = __tcg.get_builder("ellipse.j2")
GetAttr = __tcg.get_builder("getattr.j2")
Newline = __tcg.get_builder("newline.j2")
Variable = __tcg.get_builder("variable.j2")
FromImport = __tcg.get_builder("from_import.j2")
