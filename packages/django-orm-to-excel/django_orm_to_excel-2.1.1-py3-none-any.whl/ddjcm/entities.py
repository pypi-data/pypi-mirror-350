import copy
import json
from pathlib import Path
import typing as t
from abc import ABC, abstractmethod

from ddjcm.code_collector import CodeCollector
from ddjcm.code_writer import CodeWriter
from ddjcm.config import Config
from ddjcm.form_generator import FormGenerator
from ddjcm.permissions import All, Only, Permission
from ddjcm.code_generator import Call, Class, FromImport, Newline, TemplatedCodeGenerator, Variable
from ddjcm.url_manager import UrlManager
from ddjcm.view_generator import ViewGenerator


class Null:
    """ Sentinel """


class Field(ABC):
    def __init__(
            self,
            verbose: str,
            validator: t.Callable | None = None,
            default: t.Any | Null = Null,
            required: bool = False,
            permission: Permission = Permission(view=All(), edit=All())
    ):
        self.name = ""
        self.verbose = verbose
        self.default = default
        self.required = required
        self.permission = permission

        self._imports = []
        self._needs = []
        self.additional_form_options = {}

    def set_name(self, name: str):
        self.name = name

    def need(self, code: str, is_import: bool = False):
        if is_import:
            self._imports.append(code)
        else:
            self._needs.append(code)

    @abstractmethod
    def get_field_name(self):
        raise NotImplementedError

    @abstractmethod
    def get_form_field_name(self):
        raise NotImplementedError

    def get_default_value(self):
        return f"{self.default}"

    def get_options(self):
        options = {
            "verbose_name": f'"{self.verbose}"',
            "blank": not self.required,
            "null": not self.required
        }

        if self.default != Null:
            options.update({"default": self.get_default_value()})

        return options

    def get_form_options(self):
        return {
            "label": f'"{self.verbose}"',
            **self.additional_form_options
        }

    def get_model_field(self) -> str:
        options = self.get_options()

        return Variable(
            name=self.name,
            value="models." + Call(object_name=self.get_field_name(), kwargs=options)
        )

    def get_form_field(self) -> str:
        options = self.get_form_options()

        return Variable(
            name=self.name,
            value="forms." + Call(
                object_name=self.get_form_field_name(),
                kwargs=options
            )
        )


class String(Field):
    def get_field_name(self):
        return "CharField"

    def get_form_field_name(self):
        return self.get_field_name()

    def get_options(self):
        options = super().get_options()
        options["max_length"] = 256
        return options

    def get_default_value(self):
        return f'"{self.default}"'


class Integer(Field):
    def get_field_name(self):
        return "IntegerField"

    def get_form_field_name(self):
        return self.get_field_name()

class Float(Field):
    def get_field_name(self):
        return "FloatField"

    def get_form_field_name(self):
        return self.get_field_name()

class Date(Field):
    def __init__(
            self,
            verbose: str,
            validator: t.Callable | None = None,
            default: t.Any | Null = Null,
            auto_now: bool = False,
            auto_now_add: bool = False,
            required: bool = False,
            permission: Permission = Permission(view=All(), edit=All())
    ):
        super().__init__(verbose, validator, default, required, permission)

        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

    def get_field_name(self):
        return "DateField"

    def get_form_field_name(self):
        return self.get_field_name()

    def get_default_value(self):
        if self.default == "today":
            return "date.today()"

        self.need(FromImport(module="datetime", objects=["date"]), is_import=True)
        return "date({})".format(", ".join(map(lambda x: x.strip("0"), self.default.split("-"))))

    def get_options(self):
        options = super().get_options()

        if self.auto_now:
            options["auto_now"] = True

        if self.auto_now_add:
            options["auto_now_add"] = True

        return options

    def get_form_options(self):
        options = super().get_form_options()
        options["widget"] = "forms.DateInput(attrs={\"type\": \"date\"})"
        return options

    def get_form_field(self) -> str:
        options = self.get_form_options()

        return Variable(
            name=self.name,
            value="forms." + Call(
                object_name=self.get_form_field_name(),
                kwargs=options
            )
        )


class Time(Date):
    def get_field_name(self):
        return "TimeField"

    def get_form_options(self):
        options = super().get_form_options()
        options["widget"] = "forms.TimeInput(attrs={\"type\": \"time\"})"
        return options

    def get_default_value(self):
        if self.default == "now":
            return "time.now()"

        self.need(FromImport(module="datetime", objects=["time"]), is_import=True)
        return "time({})".format(", ".join(map(lambda x: x.strip("0"), self.default.split(":"))))


class DateTime(Date):
    def get_field_name(self):
        return "DateTimeField"

    def get_form_options(self):
        options = super().get_form_options()
        options["widget"] = "forms.DateTimeInput(attrs={\"type\": \"datetime-local\"})"
        return options

    def get_default_value(self):
        if self.default == "now":
            return "datetime.now()"

        date, time = self.default.split()

        self.need(FromImport(module="datetime", objects=["datetime"]), is_import=True)
        return "datetime({}, {})".format(
            ", ".join(map(lambda x: x.strip("0"), date.split("-"))),
            ", ".join(map(lambda x: x.strip("0"), time.split(":")))
        )


class Foreign(Field):
    def __init__(
            self,
            verbose: str,
            to: str,
            on_delete: str,
            queryset: str,
            validator: t.Callable | None = None,
            default: t.Any | Null = Null,
            required: bool = False,
            permission: Permission = Permission(view=All(), edit=All())
    ):
        super().__init__(verbose, validator, default, required, permission)

        self.to = to
        self.on_delete = on_delete
        self.queryset = queryset

    def get_field_name(self):
        return "ForeignKey"

    def get_form_field_name(self):
        return "ModelChoiceField"

    def get_options(self):
        options = super().get_options()

        if self.on_delete == "protect":
            options["on_delete"] = "models.PROTECT"
        elif self.on_delete == "cascade":
            options["on_delete"] = "models.CASCADE"

        return options

    def get_form_options(self):
        options = super().get_form_options()
        options["queryset"] = self.queryset
        return options

    def get_model_field(self) -> str:
        options = self.get_options()

        return Variable(
            name=self.name,
            value="models." + Call(
                object_name=self.get_field_name(),
                args=[f'"{self.to}"'],
                kwargs=options
            )
        )

    def get_form_field(self) -> str:
        self.need(FromImport(module=".models", objects=[self.to.split(".")[1]]), is_import=True)
        options = self.get_form_options()

        return Variable(
            name=self.name,
            value="forms." + Call(
                object_name=self.get_form_field_name(),
                kwargs=options
            )
        )



class Enum(String):
    def __init__(
            self,
            verbose: str,
            choices: dict[str, str],
            validator: t.Callable | None = None,
            default: t.Any | Null = Null,
            required: bool = False,
            permission: Permission = Permission(view=All(), edit=All())
    ):
        super().__init__(verbose, validator, default, required, permission)

        self.choices = choices

    def get_default_value(self):
        return self.enum_model_name + "." + self.default.upper()

    def get_options(self):

        self.enum_model_name = self.name.title() + "Choices"
        enum_model = Class(
            name=self.enum_model_name,
            parents=["models.TextChoices"],
            body=[
                Variable(name=choice.upper(), value=f'"{choice}", "{verbose}"')
                for choice, verbose in self.choices.items()
            ]
        )

        self.need(enum_model)

        options = super().get_options()
        options["choices"] = self.enum_model_name + ".choices"

        return options

    def get_form_options(self):
        options = super().get_form_options()
        options["choices"] = list(self.choices.items())
        return options

    def get_form_field_name(self):
        return "ChoiceField"

    def get_form_field(self) -> str:
        options = self.get_form_options()

        return Variable(
            name=self.name,
            value="forms." + Call(
                object_name=self.get_form_field_name(),
                kwargs=options
            )
        )


class Entity:
    def __init__(
            self,
            verbose: str,
            verboses: str,
            subsystem: str,
            fields: dict[str, Field],
            lists: dict[str, dict[str, t.Any]] | None = None,
            prefill_actor: str | None = None,
            prefill_create: str | None = None,
            prefill_create_title: str = "Создать связанную сущность",
            reports: dict[str, dict[str, t.Any]] | None = None
    ):
        self.name = ""
        self.verbose = verbose
        self.verboses = verboses
        self.subsystem = subsystem
        self.fields = fields
        self.lists = lists or {}
        self.prefill_actor = prefill_actor
        self.prefill_create = prefill_create
        self.prefill_create_title = prefill_create_title
        self.reports = reports or {}

    def set_name(self, name: str):
        self.name = name

    def set_roles(self, roles: list[str]):
        self.roles = roles

    def set_config(self, config: Config):
        self.config = config

    def set_code_collector(self, code_collector: CodeCollector):
        self.code_collector = code_collector

    def create_model(self):
        model = self.get_model()

        self.code_collector.collect(self.subsystem, "models.py", model)
        CodeWriter(Path(self.subsystem) / "models.py", self.config).write(model)

    def get_model(self) -> str:
        if not self.name:
            raise RuntimeError("Field 'name' must be setted")

        fields = []
        fields_imports = set()
        fields_needs = set()

        for field_name, field in self.fields.items():
            field.set_name(field_name)
            fields.append(field.get_model_field())

            for need in field._needs:
                fields_needs.add(need)

            for import_ in field._imports:
                fields_imports.add(import_)

        needs = "".join(fields_imports) + "\n" + "".join(fields_needs)

        model = Class(
            name=self.name.title(),
            parents=["models.Model"],
            body=[
                "\n".join(fields) + "\n\n" +
                Class(
                    name="Meta",
                    parents=[],
                    body=[
                        Variable(name="verbose_name", value=f'"{self.verbose}"'),
                        Variable(name="verbose_name_plural", value=f'"{self.verboses}"'),
                    ]
                )
            ]
        )

        return needs + "\n" + model

    def get_info_view(self) -> str:
        vg = ViewGenerator(None)
        imports = FromImport(module=f"{self.subsystem}.models", objects=[self.name.title()])
        available_fields = {
            role: list(dict(filter(lambda field: field[1].permission.can_view(role), list(self.fields.items()))).keys())
            for role in self.roles
        }

        links = {
            "Редактировать": f"/{self.subsystem}/edit_{self.name}/?id="
        }

        if self.prefill_create:
            app, list_ = self.prefill_create.split(".")
            links[self.prefill_create_title] = f"/{app}/create_{list_}/?prefill_id="

        filtered_links = {
            role: dict(filter(lambda item: any(field.permission.can_edit(role) for field in self.fields.values()), links.items()))
            for role in self.roles
        }

        return "\n".join([
            imports,
            vg.get_info_view(model=self.name.title(), available_fields=available_fields, html_page="info.html", links=filtered_links)
        ])

    def get_list_views(self) -> str:
        vg = ViewGenerator(None)

        views = []

        for list_name, list_ in self.lists.items():
            links = {
                list_["create_title"]: f"/{self.subsystem}/create_{list_name}",
            }

            all_links = {
                role: dict(filter(lambda item: list_["permission"].can_edit(role), links.items()))
                for role in self.roles
            }

            for role in self.roles:
                for report_name, report in list_["reports"].items():
                    if report["permission"].can_view(role):
                        all_links[role][report["verbose"]] = f"/{self.subsystem}/report_{list_name}_{report_name}"

            views.append(vg.get_list_view(
                list_name=list_name,
                model=self.name.title(),
                queryset=list_["queryset"],
                heads=list_["fields"],
                title=list_["name"],
                subsystem=self.subsystem,
                links=all_links
            ))

        return "\n\n".join(views)

    def get_create_views(self):
        vg = ViewGenerator(self.config)

        forms_names = []
        create_views = []

        for list_name, list_ in self.lists.items():
            form_name = f'{" ".join(list_name.split("_")).title().replace(" ", "")}CreateForm'
            forms_names.append(form_name)

            tcg = TemplatedCodeGenerator()
            create_processing = tcg.get_builder("create_processing.j2")(
                list_name=list_name.replace("_", ""),
                model_name=self.name.title(),
                subsystem_name=self.subsystem,
                entity_name=self.name,
                fields=list_["create"]
            )

            create_views.append(create_processing)
            create_views.append(
                vg.get_input_view(
                    form_model=form_name,
                    title=list_["create_title"],
                    html_page="create.html",
                    prefill=self.prefill_actor.split(".")[1] if self.prefill_actor else None
                )
            )

        import_forms = ""
        if forms_names:
            import_forms = FromImport(module=f"{self.subsystem}.forms", objects=forms_names)

        import_models = ""
        if self.prefill_actor:
            app, model = self.prefill_actor.split(".")
            import_models = FromImport(module=f"{app}.models", objects=[model])

        return "\n".join([
            import_models,
            import_forms,
            *create_views
        ])

    def get_edit_view(self):
        vg = ViewGenerator(self.config)

        form_name = f'{self.name.title()}EditForm'
        edit_views = []

        tcg = TemplatedCodeGenerator()
        edit_processing = tcg.get_builder("edit_processing.j2")(
            entity_name=self.name,
            model_name=self.name.title(),
            subsystem_name=self.subsystem,
            fields={
                role: list(
                    map(
                        lambda field_pair: field_pair[0],
                        filter(lambda field_pair: field_pair[1].permission.can_edit(role), self.fields.items())
                    )
                )
                for role in self.roles
            }
        )

        edit_views.append(edit_processing)
        edit_views.append(
            vg.get_input_view(
                form_model=form_name,
                title=self.verbose.title(),
                html_page="edit.html",
                initial_fields=list(self.fields.keys()),
                model_name=self.name.title()
            )
        )

        import_forms = (form_name and FromImport(module=f"{self.subsystem}.forms", objects=[form_name])) or ""

        return "\n".join([
            import_forms,
            *edit_views
        ])

    def get_report_views(self) -> str:
        vg = ViewGenerator(None)

        imports = FromImport(module=f"{self.subsystem}.models", objects=[self.name.title()])
        reports_views = []

        for list_name, list_ in self.lists.items():
            for report_name, report in list_["reports"].items():
                reports_views.append(
                    vg.get_download_view(
                        report_name=f"{list_name}_{report_name}",
                        model_name=self.name.title(),
                        queryset=report["queryset"],
                        fields=report["fields"]
                    )
                )

        return "\n".join([
            imports,
            "\n\n".join(reports_views)
        ])

    def get_create_form(self):
        imports = [FromImport(module="django", objects=["forms"])]
        forms = []

        for list_name, list_ in self.lists.items():
            form_name = f'{" ".join(list_name.split("_")).title().replace(" ", "")}CreateForm'

            form = FormGenerator(form_name, self.config)

            for field_name in list_["create"]:
                form.add_raw_field(self.fields[field_name].get_form_field())

            forms.append(form.get_result())

        for field in self.fields.values():
            for import_ in field._imports:
                imports.append(import_)

        return "\n\n".join([
            *imports ,
            *forms
        ])

    def get_edit_form(self):
        imports = [FromImport(module="django", objects=["forms"])]

        form_name = f'{self.name.title()}EditForm'
        form = FormGenerator(form_name, self.config)

        for field_name in self.fields:
            copied_field = copy.deepcopy(self.fields[field_name])
            copied_field.additional_form_options["required"] = False
            form.add_raw_field(copied_field.get_form_field())

        form_edit_permission_method = "def get_fields(self, request):\n    role = request.user.profile.role\n    "

        for role in self.roles:
            form_edit_permission_method += 'if role == "' + role.upper() + '":\n        return ' + str(list(
                map(
                    lambda field_pair: field_pair[0],
                    filter(lambda field_pair: field_pair[1].permission.can_edit(role), self.fields.items())
                )
            )) + "\n    "

        form_edit_permission_method += "return []"

        form.add_raw_field(form_edit_permission_method)

        for field in self.fields.values():
            for import_ in field._imports:
                imports.append(import_)

        return "\n\n".join([
            *imports ,
            form.get_result()
        ])

    def save_views(self):
        info_view = self.get_info_view()
        list_views = self.get_list_views()
        create_views = self.get_create_views()
        edit_view = self.get_edit_view()
        report_views = self.get_report_views()

        self.code_collector.collect(self.subsystem, "views.py", "\n\n".join([
            info_view,
            list_views,
            create_views,
            edit_view,
            report_views,
        ]))

    def save_forms(self):
        create_form = self.get_create_form()
        edit_form = self.get_edit_form()

        self.code_collector.collect(self.subsystem, "forms.py", "\n\n".join([
            create_form,
            edit_form
        ]))

    def register_urls(self):
        url_manager = UrlManager(self.subsystem, self.code_collector, self.config)

        url_manager.register_url(self.name, f"{self.name}_info_view")
        url_manager.register_url(f"edit_{self.name}", f"{self.name}edit_view")

        for list_name in self.lists:
            url_manager.register_url(f"create_{list_name}", f"{list_name.lower().replace('_', '')}create_view")

        for list_ in self.lists:
            url_manager.register_url(list_, f"{list_}_list_view")

        for list_name, list_ in self.lists.items():
            for report in list_["reports"]:
                url_manager.register_url(f"report_{list_name}_{report}", f"{list_name}_{report}_download_view")

        url_manager.save_urls(append=True)
