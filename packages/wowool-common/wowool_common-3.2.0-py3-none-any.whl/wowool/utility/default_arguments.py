from typing import Optional, Union
from pathlib import Path
from wowool.utility.path import expand_path
from wowool.document import Document


def default_cleanup(text):
    """
    Default cleanup function for the CLI.
    :param doc: Document to be cleaned up
    :type doc: :class:`Document`
    """
    return "".join(i for i in text if 31 < ord(i) < 127 or ord(i) == 0xD or ord(i) == 0xA)


def make_document_collection(
    text: Optional[Union[list, str]] = None,
    file: Optional[Union[Path, str]] = None,
    cleanup: Optional[bool] = None,
    encoding="utf-8",
    pattern="**/*.txt",
    **kwargs,
):
    stripped = None
    if cleanup:
        stripped = default_cleanup

    if file:
        options = {}
        options["encoding"] = encoding
        if cleanup:
            options["cleanup"] = stripped
        fn = expand_path(file)

        return Document.glob(fn, stripped=stripped)
    if text:
        doc_collection = []
        if isinstance(text, str):
            doc_collection.append(Document.create(text))
        elif isinstance(text, list):
            for text_ in text:
                doc_collection.append(Document.create(text_))

    return doc_collection
