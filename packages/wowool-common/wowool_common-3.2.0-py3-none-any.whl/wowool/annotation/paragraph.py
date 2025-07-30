from __future__ import annotations
from wowool.annotation.annotation import Annotation
from wowool.annotation.sentence import Sentence
from wowool.annotation.token import Token
from typing import Callable, List, cast, Iterator, Self
from wowool.document.analysis.analysis import Analysis


class Paragraph(Annotation):
    """
    :class:`Paragraph` is a class that contains all the information of a
    """

    FilterType = Callable[[Self], bool]

    def __init__(self, begin_offset: int, end_offset: int):
        """
        Initialize a :class:`Paragraph` instance

        :param begin_offset: Begin offset of the paragraph
        :type begin_offset: ``int``
        :param end_offset: End offset of the paragraph
        :type end_offset: ``int``
        :return: An initialized paragraph
        :rtype: :class:`paragraph`
        """
        self._attributes = {}
        super(Paragraph, self).__init__(begin_offset, end_offset)
        self._sentence_annotations = None
        self._dict = None
        self._canonical = None
        self._text = None

    def _get_text(self):
        """
        :return: A string representation of the concept
        :rtype: ``str``
        """
        retval = ""
        prev_tk = None
        for tk in [a for a in self.annotations if a.is_token]:
            if prev_tk and prev_tk.end_offset != tk.begin_offset:
                retval += " "
            retval += tk.literal
            prev_tk = tk
        return retval.strip()

    @property
    def sentences(self) -> None | List[Sentence]:
        """
        :return: a list of the sentence annotations in the paragraph
        :rtype: ``list[Sentence]``
        """
        return self._sentence_annotations

    @property
    def text(self):
        """
        :return: A string representation of the concept
        :rtype: ``str``
        """
        if self._text is None:
            self._text = self._get_text()
        return self._text

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __getstate__(self):
        return self.__dict__

    def keys(self):
        """
        This function is used to convert a concept object to a dictionary

        .. code-block:: python

            { **concept }


        :return: a list of the keys of the concept.
        :rtype: list(str)


        """
        if not self._dict:
            self._dict = self.to_json()
        return self._dict.keys()

    def __repr__(self) -> str:
        retval = "P:" + Annotation.__repr__(self)
        return retval

    @staticmethod
    def same_paragraph(original_text: str, prev: Sentence, next: Sentence) -> bool:
        annotation = prev.annotations[-1]

        if prev.is_header:
            return True

        prev_last_token = cast(Token, annotation) if annotation.is_token else None
        if prev_last_token and prev_last_token.has_pos("Punct-Line"):
            return True
        if (next.begin_offset - prev.end_offset) >= 2:
            doc_text = original_text[prev.end_offset : next.begin_offset]
            if "\r" in doc_text:
                doc_text = doc_text.replace("\r", "")
            pos = doc_text.find("\n")
            if pos == -1:
                return True
            elif (pos := doc_text.find("\n", pos + 1)) == -1:
                return True
            else:
                return False

        return True

    @staticmethod
    def _document_iter(doc: Analysis, original_text: str) -> Iterator[Paragraph]:

        paragraph = Paragraph(0, 0)
        for sentence in doc:
            if paragraph._sentence_annotations is None:
                paragraph._sentence_annotations = [sentence]
                paragraph._begin_offset = sentence.begin_offset
            else:
                if Paragraph.same_paragraph(original_text, paragraph._sentence_annotations[-1], sentence):
                    paragraph._sentence_annotations.append(sentence)
                else:
                    paragraph._end_offset = paragraph._sentence_annotations[-1].end_offset
                    yield paragraph
                    paragraph = Paragraph(sentence.begin_offset, 0)
                    paragraph._sentence_annotations = [sentence]
        if paragraph._sentence_annotations:
            paragraph._end_offset = paragraph._sentence_annotations[-1].end_offset
            yield paragraph

    @staticmethod
    def iter(object, original_text=None, align: bool = True) -> Iterator[Paragraph]:
        """
        Iterate over the concepts in a document, an analysis, a sentence or a concept. For example:

        .. code-block:: python

            document = analyzer("Hello from Antwerp, said John Smith.")
            for paragraph in Paragraph.iter(document):
                print(paragraph)

        :param object: Object to iterate
        :type object: :class:`Analysis <wowool.analysis.Analysis>`

        :return: A generator expression yielding paragraphs
        :rtype: :class:`Entity <wowool.annotation.paragraph.Paragraph>`
        """
        from wowool.document.analysis.document import AnalysisDocument
        from wowool.document.analysis.analysis import Analysis

        if original_text is None and isinstance(object, AnalysisDocument):
            original_text = object.text

        if isinstance(object, AnalysisDocument) and object.analysis:
            yield from Paragraph._document_iter(object.analysis, original_text)
        elif isinstance(object, Analysis):
            yield from Paragraph._document_iter(object, original_text)
        else:
            raise TypeError(f"Expected Document, Analysis, but got '{type(object)}'")
