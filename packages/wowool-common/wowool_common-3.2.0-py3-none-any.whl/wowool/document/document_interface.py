from typing import Protocol, runtime_checkable, Any

MT_PLAINTEXT = "text/plain"
MT_ANALYSIS_JSON = "application/vnd.wowool.document-analysis"
MT_STRING = "application/vnd.wowool.string"


@runtime_checkable
class DocumentInterface(Protocol):
    """
    :class:`DocumentInterface` is an interface utility to handle data input.
    """

    @property
    def id(self) -> str:
        pass

    @property
    def mime_type(self) -> str:
        pass

    @property
    def encoding(self) -> str:
        pass

    @property
    def data(self) -> Any:
        pass

    @property
    def metadata(self) -> dict[str, Any]:
        pass
