from dataclasses import dataclass
from wowool.document.analysis.apps.topics import convert_topics, Topic
from wowool.document.analysis.apps.themes import convert_themes, Theme


@dataclass
class Chunk:
    sentences: list
    begin_offset: int
    end_offset: int
    outline: list | None
    topics: list[Topic] | None
    themes: list[Theme] | None


def convert_chunks(jo_chunks: list):
    chunks = []
    for c in jo_chunks["chunks"]:
        chunk = Chunk(c["sc"], c.get("bo"), c.get("eo"), c.get("outline"), convert_topics(c.get("topics")), convert_themes(c.get("themes")))
        chunks.append(chunk)

    return chunks
