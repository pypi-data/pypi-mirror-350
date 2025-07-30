from pathlib import Path

from ddjcm.config import Config


class CodeWriter:
    def __init__(self, path: Path, config: Config):
        self.config = config

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()

        self.path = path
        self.content = path.read_text(encoding=self.config.encoding)

    def write(self, code: str):
        if self.is_guard_end_comment_before_guard_start_comment():
            raise RuntimeError(
                "Комментарий начала не может быть расположен после комментария окончания ("
                + str(self.path) + ")"
            )

        if not self.has_guard_start_comment():
            code =  self.content \
                    + "\n" \
                    + self.config.guard_start_comment \
                    + code \
                    + self.config.guard_end_comment
        else:
            content_before = self.content.split(self.config.guard_start_comment)[0].strip()
            content_after = ""

            if self.has_guard_end_comment():
                content_after = self.content.split(self.config.guard_end_comment)[-1]

            content_after = content_after.strip()

            code = content_before \
                    + "\n" \
                    + self.config.guard_start_comment \
                    + code \
                    + self.config.guard_end_comment \
                    + "\n" \
                    + content_after

        self.path.write_text(code, encoding=self.config.encoding)

    def has_guard_start_comment(self) -> bool:
        return self.config.guard_start_comment in self.content

    def has_guard_end_comment(self) -> bool:
        return self.config.guard_end_comment in self.content

    def is_guard_end_comment_before_guard_start_comment(self) -> bool:
        return (
            self.content.find(self.config.guard_start_comment) > self.content.find(self.config.guard_end_comment)
            and self.content.find(self.config.guard_end_comment) > -1
        )
