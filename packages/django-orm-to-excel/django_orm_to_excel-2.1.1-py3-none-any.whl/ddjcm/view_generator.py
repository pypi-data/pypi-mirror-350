import typing as t

from ddjcm.config import Config
from ddjcm.code_generator import TemplatedCodeGenerator


class ViewGenerator:
    def __init__(self, config: Config):
        self.tcg = TemplatedCodeGenerator()

    def get_dashboard_view(
            self,
            subsystem: str,
            model_name: str,
            title: str,
            items: dict[str, dict[t.Union[t.Literal["slug"], t.Literal["name"]], str]],
            import_render: bool = False
    ):
        DashboardView = self.tcg.get_builder("dashboard_view.j2")

        return DashboardView(subsystem=subsystem, model_name=model_name, title=title, items=items, import_render=import_render)

    def get_input_view(self, form_model: str, html_page: str, title: str = "", initial_fields: list | None = None, model_name: str = "", prefill: str | None = None):
        InputView = self.tcg.get_builder("input_view.j2")

        return InputView(form_model=form_model, title=title, html_page=html_page, initial_fields=initial_fields or [], model_name=model_name, prefill=prefill)

    def get_info_view(self, model: str, available_fields: dict[str, list[str]], html_page: str, links: dict[str, str]):
        InfoView = self.tcg.get_builder("info_view.j2")

        return InfoView(model=model, available_fields=available_fields, html_page=html_page, links=links)

    def get_list_view(self, list_name: str, model: str, queryset: str, heads: list[str], title: str, subsystem: str, links: dict[str, str]):
        ListView = self.tcg.get_builder("list_view.j2")

        return ListView(list_name=list_name, model=model, queryset=queryset, heads=heads, title=title, subsystem=subsystem, links=links)

    def get_download_view(self, report_name: str, model_name: str, queryset: str, fields: list[str]):
        DownloadView = self.tcg.get_builder("download.j2")

        return DownloadView(report_name=report_name, model_name=model_name, queryset=queryset, fields=fields)
