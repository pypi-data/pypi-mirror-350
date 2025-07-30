from typing import Iterator, Self


class BasicAnnotation:
    """
    :class:`BasicAnnotation` is the base class for all annotations
    """

    __slott__ = ["begin_offset", "end_offset"]

    def __init__(self, begin_offset: int, end_offset: int):
        """
        Initialize an :class:`BasicAnnotation` instance

        :param begin_offset: Begin offset of the annotation
        :type begin_offset: ``int``
        :param end_offset: End offset of the annotation
        :type end_offset: ``int``

        :rtype: :class:`BasicAnnotation`
        """
        self._begin_offset: int = begin_offset
        self._end_offset: int = end_offset

    def __repr__(self):
        return "({:>3},{:>3})".format(self.begin_offset, self.end_offset)

    @property
    def begin_offset(self) -> int:
        """
        :return: The begin offset of the annotation
        :type: ``int``
        """
        return self._begin_offset

    @property
    def end_offset(self) -> int:
        """
        :return: The end offset of the annotation
        :type: ``int``
        """
        return self._end_offset

    @property
    def is_concept(self) -> bool:
        """
        Deprecated, use :meth:`is_entity` instead
        :return: Whether the annotation is a :class:`Entity`
        :rtype: ``bool``
        """
        return self.is_entity

    @property
    def is_entity(self) -> bool:
        """
        :return: Whether the annotation is a :class:`Entity`
        :rtype: ``bool``
        """
        from wowool.annotation.entity import Entity

        return isinstance(self, Entity)

    @property
    def is_sentence(self) -> bool:
        """
        :return: Whether the annotation is a :class:`Sentence`
        :rtype: ``bool``
        """
        from wowool.annotation.sentence import Sentence

        return isinstance(self, Sentence)

    @property
    def is_token(self) -> bool:
        """
        :return: Whether the annotation is a :class:`Token`
        :rtype: ``bool``
        """
        from wowool.annotation.token import Token

        return isinstance(self, Token)

    @property
    def is_paragraph(self) -> bool:
        """
        :return: Whether the annotation is a :class:`Paragraph`
        :rtype: ``bool``
        """
        from wowool.annotation.paragraph import Paragraph

        return isinstance(self, Paragraph)


class Annotation(BasicAnnotation):
    """
    :class:`Annotation` is the base class for all annotations
    """

    __slott__ = ["begin_offset", "end_offset"]

    def __init__(self, begin_offset: int, end_offset: int):
        """
        Initialize an :class:`Annotation` instance

        :param begin_offset: Begin offset of the annotation
        :type begin_offset: ``int``
        :param end_offset: End offset of the annotation
        :type end_offset: ``int``

        :rtype: :class:`Annotation`
        """
        super(Annotation, self).__init__(begin_offset, end_offset)
        self._annotation_idx = None

    @property
    def index(self) -> int:
        assert self._annotation_idx is not None
        return self._annotation_idx

    @staticmethod
    def _document_iter(doc) -> Iterator[Self]:
        for sentence in doc:
            for annotation in sentence:
                yield annotation

    @staticmethod
    def _sentence_iter(sentence) -> Iterator[Self]:
        for annotation in sentence:
            yield annotation

    @staticmethod
    def iter(object) -> Iterator[Self]:
        """
        Iterate over the concepts in a document, an analysis, a sentence or a concept. For example:

        .. code-block:: python

            document = analyzer("Hello from Antwerp, said John Smith.")
            for concept in Entity.iter(document, lambda concept : concept.uri == "NP"):
                print(concept)

        :param object: Object to iterate
        :type object: :class:`Analysis <wowool.analysis.Analysis>`, :class:`Sentence <wowool.annotation.sentence.Sentence>` or :class:`Entity <wowool.annotation.entity.Entity>`
        :param filter: Predicate function to filter the concepts, callable that accepts a concept and returns True if the concept is considered a match
        :type filter: Callable accepting a :class:`Entity` and returning a ``bool``

        :return: A generator expression yielding concepts
        :rtype: :class:`Entity <wowool.annotation.entity.Entity>`
        """
        from wowool.document.analysis.document import AnalysisDocument
        from wowool.document.analysis.analysis import Analysis
        from wowool.annotation import Sentence

        if isinstance(object, AnalysisDocument) and object.analysis:
            yield from Annotation._document_iter(object.analysis)
        elif isinstance(object, Analysis):
            yield from Annotation._document_iter(object)
        elif isinstance(object, Sentence):
            yield from Annotation._sentence_iter(object)
        else:
            raise TypeError(f"Expected Document, Analysis, Sentence, but got '{type(object)}'")


class ErrorAnnotationNotFound(ValueError):
    pass
