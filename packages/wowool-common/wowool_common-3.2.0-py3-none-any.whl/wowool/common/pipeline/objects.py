from dataclasses import dataclass, field
from typing import Any


@dataclass
class UUID:
    name: str
    options: dict[str, Any] = field(default_factory=dict)

    def to_json(self):
        return {"name": self.name, "options": self.options}


def createUUID(uid: str | UUID | dict) -> UUID:
    if isinstance(uid, str):
        return UUID(name=uid)
    elif isinstance(uid, UUID):
        return uid
    elif isinstance(uid, dict):
        if "options" not in uid:
            uid["options"] = {}
        return UUID(name=uid["name"], options=uid["options"])
    else:
        raise ValueError(f"Invalid UID: {uid}")


@dataclass
class ComponentInfo:
    options: dict[str, Any]
    type: str
    name: str
    uid: str
    filename: str | None = None
    app: dict[str, str] | None = None
    original: str | None = None

    def to_json(self):
        retval = {"type": self.type, "uid": self.uid}
        if self.options:
            retval["options"] = self.options
        if self.filename:
            retval["filename"] = self.filename
        if self.app:
            retval["app"] = self.app
        return retval
