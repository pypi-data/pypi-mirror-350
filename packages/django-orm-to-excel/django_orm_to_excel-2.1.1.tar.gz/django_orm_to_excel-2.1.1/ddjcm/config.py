from dataclasses import dataclass


@dataclass
class Config:
    create_app_command: str
    encoding: str
    guard_start_comment: str
    guard_end_comment: str
