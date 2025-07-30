from dataclasses import dataclass


@dataclass
class Topic:
    name: str
    relevancy: float


def convert_topics(jo_topics: list):
    return [Topic(**t) for t in jo_topics] if jo_topics else []
