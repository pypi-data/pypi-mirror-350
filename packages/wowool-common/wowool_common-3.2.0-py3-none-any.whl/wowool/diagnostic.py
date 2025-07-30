from enum import IntEnum
import logging
import typing


class DiagnosticType(IntEnum):
    """
    :class:`DiagnosticType` is an enumeration type that holds the diagnostic types supported by default. The included levels map to the levels provided by the logging library

    .. note:: This enumeration type can be extended or replaced with any other integer type
    """

    Debug = logging.DEBUG
    Info = logging.INFO
    Warning = logging.WARNING
    Error = logging.ERROR
    Critical = logging.CRITICAL
    Notset = logging.NOTSET

    @classmethod
    def names(cls) -> typing.List[str]:
        """
        :return: The diagnostic names, sorted by level value (``int``)
        :rtype: A ``list`` of ``str``
        """
        names = [name for name in dir(DiagnosticType) if not name.startswith("_") and name[0].isupper()]
        return sorted(names, key=lambda name: int(getattr(DiagnosticType, name)))

    @classmethod
    def all(cls):
        """
        :return: All type enumerations
        :rtype: A ``list`` of ``int``
        """
        return [getattr(DiagnosticType, name) for name in cls.names()]

    @classmethod
    def count(cls) -> int:
        """
        :return: The number of types
        :rtype: ``int``
        """
        return len(cls.names())


_levelToName = {
    logging.CRITICAL: "[red bold]CRITICAL[/red bold]",
    logging.ERROR: "[red]ERROR[/red]",
    logging.WARNING: "[yellow]WARNING[/yellow]",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
    logging.NOTSET: "NOTSET",
}


def _getLevelName(level):
    if level in _levelToName:
        return _levelToName[level]
    return ""


class Diagnostic:
    """
    :class:`Diagnostic` is a class that holds all relevant diagnostical information

    .. note:: The ``type`` parameter can be any integer type. For convenience sake, :class:`DiagnosticType` is used by default, but you can provide your own typing scheme
    """

    @staticmethod
    def from_json(json: dict):
        return Diagnostic(
            id=json["id"],
            message=json["message"],
            type=json["type"],
            line=json["line"] if "line" in json else None,
            offset=json["offset"] if "offset" in json else None,
        )

    def __init__(
        self,
        id: typing.Union[str, int],
        message: str,
        type: typing.SupportsInt,
        line: typing.Union[int, None] = None,
        offset: typing.Union[int, None] = None,
    ):
        """
        Initialize a :class:`Diagnostic` instance

        :param id: Unique identifier
        :type id: ``str`` or ``int``
        :param message: Message
        :type message: ``str``
        :param line: Line number (optional)
        :type line: ``int``
        :param offset: Offset (optional)
        :type offset: ``int``
        """
        super(Diagnostic, self).__init__()
        self.id = id
        self.message = message
        self.type = type
        self.line = line
        self.offset = offset

    def to_json(self):
        """
        :return: A dictionary representing a JSON object of the diagnostic
        :rtype: ``dict``
        """
        obj = dict(id=self.id, message=self.message, type=self.type)
        if self.line is not None:
            obj["line"] = self.line
        if self.offset is not None:
            obj["offset"] = self.offset
        return obj

    def to_exception(self):
        return DiagnosticException(self)

    def rich(self):
        """
        :return: The rich string representation of the token
        :rtype: ``str``
        """
        if self.line:
            return f"<default>{self.id}</default>:{self.line}:{_getLevelName(self.type)}:{self.message}"
        else:
            return f"<default>{self.id}</default>:{_getLevelName(self.type)}:{self.message}"

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    def __str__(self):
        return f"<Diagnostic: id={self.id}, type={self.type}, message={self.message}>"


class DiagnosticException(Exception):
    def __init__(self, diagnostic: Diagnostic):
        super(DiagnosticException, self).__init__(self, diagnostic.message)
        self.diagnostic = diagnostic

    def __str__(self):
        return self.diagnostic.message


class Diagnostics:
    """
    :class:`Diagnostics` is a convenience class that provides some commonly used functionality and acts as a facade
    """

    @staticmethod
    def from_json(json: list):
        items = [Diagnostic.from_json(item) for item in json]
        return Diagnostics(items=items)

    def __init__(self, items: typing.List[Diagnostic] = None):
        """
        Initialize a :class:`Diagnostics` instance

        :params items: Diagnostics. Defaults to an empty list
        :type items: A ``list`` of :class:`Diagnostic`
        """
        super(Diagnostics, self).__init__()
        self.items = items if items else []

    def add(self, diagnostic: Diagnostic):
        """
        Add a diagnostic

        :param diagnostic: Diagnostic
        :type diagnostic: :class:`Diagnostic`
        """
        self.items.append(diagnostic)

    def extend(self, diagnostics):
        """
        Extend with given diagnostics

        :param diagnostic: Diagnostics
        :type diagnostic: :class:`Diagnostics`
        """
        for diagnostic in diagnostics:
            self.add(diagnostic)

    def filter(self, type: typing.SupportsInt):
        """
        Filter on a given diagnostic type

        :param type: Diagnostic type
        :type type: :class:`DiagnosticType` or ``int``

        :return: A generator expression yielding diagnostics of the matching type
        :rtype: :class:`Diagnostic`
        """
        if type == DiagnosticType.Notset:
            return self.items
        return filter(lambda item: type == item.type, self.items)

    def has(self, type: typing.SupportsInt) -> bool:
        """
        :return: Whether a diagnostic with the given type is present
        :rtype: ``bool``
        """
        for _ in self.filter(type):
            return True
        return False

    def __len__(self) -> int:
        """
        :return: The number of diagnostics
        :rtype: ``int``
        """
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def raise_when(self, type: typing.SupportsInt):
        """
        Raises an exception when a diagnostic exceeds the level of the given type

        :raises DiagnosticException: Only in presence of a diagnostic level that exceeds the given type
        """
        for diagnostic in self.items:
            if int(diagnostic.type) >= int(type):
                exception = diagnostic.to_exception()
                assert isinstance(exception, DiagnosticException), "Diagnostic did not return an exception"
                raise exception

    def is_greater_or_equal_than(self, type: typing.SupportsInt):
        """
        :returns: Whether a diagnostic is greater or equal than the given diagnostic type
        :rtype: ``bool``
        """
        for diagnostic in self.items:
            if int(diagnostic.type) >= int(type):
                return True

    def to_json(self):
        return [diagnostic.to_json() for diagnostic in self.items]

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    def __str__(self):
        return f"<Diagnostics: {len(self)} items>"

    def __getitem__(self, index):
        return self.items[index]
