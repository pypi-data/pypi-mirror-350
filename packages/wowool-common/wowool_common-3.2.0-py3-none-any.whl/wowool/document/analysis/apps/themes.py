from dataclasses import dataclass


@dataclass
class Theme:
    name: str
    relevancy: float


def convert_themes(jo_themes: list):
    return [Theme(**t) for t in jo_themes] if jo_themes else []
