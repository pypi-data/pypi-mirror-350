from ddjcm.config import Config
from ddjcm.code_generator import (
    Call,
    Class,
    GetAttr,
    Variable,
    TemplatedCodeGenerator,
) 


class FormGenerator:
    def __init__(self, model_name: str, config: Config):
        self.model_name = model_name
        self.tcg = TemplatedCodeGenerator()
        self.fields = []

    def add_field(self, field_name: str, label: str, field_type: str, settings: dict[str, str]):
        settings["label"] = f'"{label}"'

        self.fields.append(
            Variable(
                name=field_name,
                value=Call(
                    object_name=GetAttr(object_name="forms", attr_name=field_type),
                    kwargs=settings,
                ),
            ),
        )

        return self

    def add_raw_field(self, raw_field: str):
        self.fields.append(raw_field)
        return self

    def get_result(self):
        body = self.fields

        return Class(
            name=self.model_name,
            parents=[GetAttr(object_name="forms", attr_name="Form")],
            body=body
        )
