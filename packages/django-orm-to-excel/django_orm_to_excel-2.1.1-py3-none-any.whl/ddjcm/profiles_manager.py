from pathlib import Path

from ddjcm.code_collector import CodeCollector
from ddjcm.config import Config
from ddjcm.application import App
from ddjcm.code_writer import CodeWriter
from ddjcm.url_manager import UrlManager
from ddjcm.form_generator import FormGenerator
from ddjcm.view_generator import ViewGenerator
from ddjcm.model_generator import ModelGenerator
from ddjcm.templates_manager import TemplatesManager
from ddjcm.code_generator import FromImport, TemplatedCodeGenerator


class ProfilesManager:
    def __init__(self, roles: dict[str, str], code_collector: CodeCollector, config: Config):
        self.roles = roles
        self.config = config
        self.code_collector = code_collector
        self.url_manager = UrlManager("profiles", self.code_collector, config)

    def create_app(self):
        return App("profiles", self.config).create()

    def create_model(self):
        profile_model = ModelGenerator(
            "Profile",
            config=self.config,
            verbose_name="профиль",
            verbose_name_plural="профили"
        ) \
            .add_field("user", "OneToOneField", {
                    "to": '"auth.User"',
                    "verbose_name": '"Пользователь"',
                    "null": "False",
                    "on_delete": "models.CASCADE"
                }) \
            .add_field("name", "CharField", {
                    "verbose_name": '"Имя"',
                    "max_length": "256",
                    "blank": "False",
                    "null": "False"
                }) \
            .add_field("last_name", "CharField", {
                    "verbose_name": '"Фамилия"',
                    "max_length": "256",
                    "blank": "False",
                    "null": "False"
                }) \
            .add_field("phone_number", "CharField", {
                    "verbose_name": '"Номер телефона"',
                    "max_length": "11",
                    "blank": "False",
                    "null": "False"
                }) \
            .add_field("role", "CharField", {
                    "verbose_name": '"Роль"',
                    "max_length": "256",
                    "choices": "ProfileRole.choices",
                    "default": "ProfileRole." + list(self.roles.keys())[0].upper()
                }) \
            .add_text_enum("ProfileRole", self.roles)

        CodeWriter(Path("profiles") / "models.py", self.config).write(profile_model.get_result())

    def create_forms(self):
        imports = FromImport(module="django", objects=["forms"])

        register_form = FormGenerator("ProfileRegisterForm", self.config) \
            .add_field("username", "Никнейм", "CharField", {}) \
            .add_field("name", "Имя", "CharField", {}) \
            .add_field("last_name", "Фамилия", "CharField", {}) \
            .add_field("phone_number", "Номер телефона", "CharField", {}) \
            .add_field("password", "Пароль", "CharField", {"widget": "forms.PasswordInput"})

        login_form = FormGenerator("ProfileLoginForm", self.config) \
            .add_field("username", "Никнейм", "CharField", {}) \
            .add_field("password", "Пароль", "CharField", {"widget": "forms.PasswordInput"})

        forms = "\n\n".join(map(lambda form: form.get_result(), [
            register_form,
            login_form
        ]))

        result = imports + "\n\n" + forms

        CodeWriter(Path("profiles") / "forms.py", self.config).write(result)

    def create_views(self):
        vg = ViewGenerator(self.config)
        profile_register_view = vg.get_input_view(form_model="ProfileRegisterForm", html_page="register.html")
        profile_login_view = vg.get_input_view(form_model="ProfileLoginForm", html_page="login.html")

        import_forms = FromImport(module="profiles.forms", objects=["ProfileRegisterForm", "ProfileLoginForm"])

        tcg = TemplatedCodeGenerator()
        profileregister_processing = tcg.get_builder("profileregister_processing.j2")()
        profilelogin_processing = tcg.get_builder("profilelogin_processing.j2")()

        result = "\n".join([
            import_forms,
            profileregister_processing,
            profile_register_view,
            profilelogin_processing,
            profile_login_view,
        ])

        for role in self.roles.keys():
            self.url_manager.register_url(f"register_{role}", "profileregister_view")

        self.url_manager.register_url("login", "profilelogin_view")

        tm = TemplatesManager("profiles", self.config)
        html_templates_path = Path("..") / "ddjcm" / Path("ddjcm") / "html_templates"
        tm.write("register.html", (html_templates_path / "register.html").read_text(encoding=self.config.encoding))
        tm.write("login.html", (html_templates_path / "login.html").read_text(encoding=self.config.encoding))

        CodeWriter(Path("profiles") / "views.py", self.config).write(result)

    def save_urls(self):
        self.url_manager.save_urls()
