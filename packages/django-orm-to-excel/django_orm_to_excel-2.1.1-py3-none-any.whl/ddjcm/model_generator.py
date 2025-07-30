from ddjcm.config import Config
from ddjcm.code_generator import (
    TemplatedCodeGenerator,
    Call,
    Class,
    GetAttr,
    Newline,
    Variable
)


class ModelGenerator:
    def __init__(
            self,
            model_name: str,
            config: Config,
            verbose_name: str | None = None,
            verbose_name_plural: str | None = None,
    ):
        self.model_name = model_name

        self.verbose_name = verbose_name
        if not verbose_name_plural:
            verbose_name_plural = verbose_name
        self.verbose_name_plural = verbose_name_plural

        self.tcg = TemplatedCodeGenerator()

        self.fields = []
        self.enums = []

    def add_field(self, field_name: str, field_type: str, settings: dict[str, str]):
        self.fields.append(
            Variable(
                name=field_name,
                value=Call(
                    object_name=GetAttr(object_name="models", attr_name=field_type),
                    kwargs=settings,
                ),
            ),
        )

        return self

    def add_text_enum(self, name: str, options: dict[str, str]):
        self.enums.append(
            Class(
                name=name,
                parents=["models.TextChoices"],
                body=[
                    Variable(
                        name=value.upper(),
                        value=f'"{value.upper()}", "{verbose}"'
                    )
                    for value, verbose in options.items()
                ]
            )
        )

        return self

    def get_result(self):
        body = self.fields

        if self.verbose_name:
            meta_body = [
                Variable(name="verbose_name", value=f'"{self.verbose_name}"'),
                Variable(name="verbose_name_plural", value=f'"{self.verbose_name_plural}"'),
            ]

            meta_class = Class(
                name="Meta",
                parents=[],
                body=meta_body
            )

            body += [Newline(), meta_class]

        result = "\n\n".join(self.enums) + "\n\n" + Class(
            name=self.model_name,
            parents=[GetAttr(object_name="models", attr_name="Model")],
            body=body
        )

        return result
