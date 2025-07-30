from pathlib import Path

from ddjcm.code_collector import CodeCollector
from ddjcm.config import Config
from ddjcm.code_writer import CodeWriter
from ddjcm.code_generator import TemplatedCodeGenerator


class UrlManager:
    def __init__(self, app_name: str, code_collector: CodeCollector, config: Config):
        self.app_name = app_name
        self.code_collector = code_collector
        self.config = config

        self.urls = {}

    def register_url(self, url: str, view: str):
        self.urls[url] = view

    def save_urls(self, append: bool = False):
        # cw = CodeWriter(Path(self.app_name) / "urls.py", self.config)
        tcg = TemplatedCodeGenerator()

        Urls = tcg.get_builder("urls.j2")
        urls = Urls(app_name=self.app_name, urls=self.urls, append=append)

        # cw.write(urls)
        self.code_collector.collect(self.app_name, "urls.py", urls)
