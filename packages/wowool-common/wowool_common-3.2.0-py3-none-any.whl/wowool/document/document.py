from wowool.document.document_interface import DocumentInterface
from wowool.document.factory import Factory, _resolve__pass_thru
from pathlib import Path
from wowool.document.defines import WJ_ID, WJ_DATA, WJ_MIME_TYPE, WJ_METADATA
from typing import Generator, Any


class Document(DocumentInterface):
    """
    :class:`DocumentInterface` is an interface utility to handle data input.
    """

    def __init__(self, data: str | bytes, id: Path | str | None = None, mime_type: str = "", metadata: dict = {}, encoding="utf8"):
        self.input_provider = Factory.create(
            id=id,
            data=data,
            mime_type=mime_type,
            encoding=encoding,
            metadata=metadata,
        )
        self._metadata = metadata

    @property
    def id(self) -> str:
        """
        :return: Unique document identifier
        :rtype: ``str``
        """
        return self.input_provider.id

    @property
    def mime_type(self) -> str:
        """
        :return: Document type
        :rtype: ``str``
        """
        return self.input_provider.mime_type

    @property
    def encoding(self) -> str:
        """
        :return: Document encoding
        :rtype: ``str`` or ``bytes``
        """
        return self.input_provider.encoding

    @property
    def data(self) -> str | bytes:
        """
        :return: Document content
        :rtype: ``str`` or ``bytes``
        """
        return self.input_provider.data

    @property
    def metadata(self) -> dict:
        """
        :return: Document content
        :rtype: ``str`` or ``bytes``
        """
        return self._metadata

    @staticmethod
    def deserialize(document: dict) -> DocumentInterface:
        """
        Deserialize a document from JSON format.

        :param document: JSON representation of the document.
        :return: Document object.
        :rtype: ``Document``
        """
        from wowool.document.serialize import deserialize

        return deserialize(document)

    @staticmethod
    def from_json(
        document: dict,
    ) -> DocumentInterface:
        return Factory.from_json(
            id=document[WJ_ID], data=document[WJ_DATA], provider_type=document[WJ_MIME_TYPE], metadata=document.get(WJ_METADATA, {})
        )

    @staticmethod
    def create(
        data: str | bytes | None = None,
        id: Path | str | None = None,
        mime_type: str = "",
        encoding="utf8",
        binary: bool = False,
        **kwargs,
    ) -> DocumentInterface:
        """
        Create a document from the given data.

        :param data: Document content.
        :param id: Unique document identifier.
        :param mime_type: Document type.
        :param encoding: Document encoding.
        :param raw: If True, the data is treated as raw bytes.
        :param kwargs: Additional keyword arguments.
        :return: Document object.
        :rtype: ``Document``"""
        return Factory.create(
            id=id,
            data=data,
            mime_type=mime_type,
            encoding=encoding,
            binary=binary,
            **kwargs,
        )

    @staticmethod
    def from_file(
        file: Path | str | None = None,
        data: str | bytes | None = None,
        mime_type: str = "",
        encoding="utf-8",
        **kwargs,
    ) -> DocumentInterface:
        """Create a document from the given file.

        :param file: Path to the file.
        :param data: Document content.
        :param mime_type: Document type.
        :param encoding: Document encoding.
        :param kwargs: Additional keyword arguments.
        :return: Document object.
        :rtype: ``Document``
        :raises ValueError: If the file is not found.
        :raises TypeError: If the file is not a string or Path object.
        :raises IOError: If there is an error reading the file.
        """
        return Factory.create(
            id=file,
            data=data,
            mime_type=mime_type,
            encoding=encoding,
            **kwargs,
        )

    @staticmethod
    def glob(
        folder: Path | str,
        pattern: str = "**/*.txt",
        mime_type: str = "",
        resolve=_resolve__pass_thru,
        binary: bool = False,
        **kwargs,
    ) -> Generator[DocumentInterface, Any, None]:
        """
        Create a document from the given folder.
        This method will search for files matching the given pattern in the specified folder.

        :param folder: Path to the folder.
        :param pattern: Pattern to match files.
        :param mime_type: Document type.
        :param resolve: Function to resolve the data.
        :param raw: If True, the data is treated as raw bytes.
        :param kwargs: Additional keyword arguments.
        :return: Generator of Document objects.
        :rtype: ``Generator``
        :raises ValueError: If the folder is not found."""
        yield from Factory.glob(folder, pattern=pattern, mime_type=mime_type, resolve=resolve, binary=binary, **kwargs)
