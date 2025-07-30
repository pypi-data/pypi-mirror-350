from io import StringIO
from wowool.annotation.annotation import BasicAnnotation
from wowool.annotation.token import Token
from wowool.annotation.entity import Entity
from typing import Callable, Iterator, Self


def _filter_pass_thru_concept(concept: Entity) -> bool:
    return concept.uri != "Sentence"


def _filter_pass_thru(sentence) -> bool:
    return True


class Sentence(BasicAnnotation):
    """
    :class:`Sentence` is a class that contains all the :class:`Tokens <wowool.annotation.token.Token>` and :class:`Concepts <wowool.annotation.entity.Entity>` of a sentence
    """

    FilterType = Callable[[Self], bool]

    def __init__(self, begin_offset: int, end_offset: int) -> None:
        """
        Initialize a :class:`Sentence` instance

        :param begin_offset: Begin offset of the sentence
        :type begin_offset: ``int``
        :param end_offset: End offset of the sentence
        :type end_offset: ``int``

        :return: An initialized sentence
        :rtype: :class:`Sentence`
        """
        super(Sentence, self).__init__(begin_offset, end_offset)
        self.annotations = []
        self.text_ = None
        self.attributes = {}
        self.tokens_: list[Token] | None = None

    def rich(self) -> str:
        """
        :return: The rich string representation of the sentence
        :rtype: ``str``
        """
        output = StringIO()
        output.write("S:" + BasicAnnotation.__repr__(self))
        if self.is_header:
            output.write(" @( header='true' )")
        output.write("\n")
        for annotation in self.annotations:
            output.write(" ")
            output.write(annotation.rich())
            output.write("\n")
        contents = output.getvalue()
        output.close()
        return contents

    def __repr__(self) -> str:
        output = StringIO()
        output.write("S:" + BasicAnnotation.__repr__(self))
        if self.is_header:
            output.write(" @( header='true' )")
        output.write("\n")
        for annotation in self.annotations:
            output.write(" ")
            output.write(str(annotation))
            output.write("\n")
        contents = output.getvalue()
        output.close()
        return contents

    def __iter__(self):
        """
        A :class:`Sentence` instance is iterable, yielding :class:`Annotation <wowool.annotation.annotation.Annotation>` objects. For example:

        .. code-block:: python

            for annotation in sentence:
                print(annotation)

        :rtype: :class:`Annotation <wowool.annotation.annotation.Annotation>`
        """
        return iter(self.annotations)

    def __len__(self) -> int:
        return len(self.annotations)

    @property
    def tokens(self) -> list[Token]:
        if self.tokens_ is None:
            self.tokens_ = [a for a in self.annotations if a.is_token]
        return self.tokens_

    @property
    def entities(self):
        yield from Entity.iter(self)

    def __getattr__(self, uri: str):
        """
        Find the first instance of the concept with the given URI in the sentence

        For example:

        .. code-block:: python

            # Find the first person in the current sentence
            person = sentence.Person

        :param uri: URI, or name, of the concept
        :type  uri: ``str``

        :returns: The first matching instance of the given concept
        :type: :class:`Entity <wowool.annotation.entity.Entity>`

        """
        return self.find_first(uri)

    def find_first(self, uri: str):
        """
        Find the first instance of the concept with the given URI in the sentence

        For example:

        .. code-block:: python

            # Find a child concept in the current sentence
            person = concept.find_first('Person'))

        :param uri: URI, or name, of the concept
        :type  uri: ``str``

        :returns: The first matching instance of the given concept
        :type: :class:`Entity <wowool.annotation.entity.Entity>`
        """
        concept = Entity(self.begin_offset, self.end_offset, "Sentence")
        concept._sentence_annotations = self.annotations
        concept._annotation_idx = 0
        return concept.find_first(uri)

    def find(self, uri: str):
        """
        Find all instances of the concept the with the given URI in the sentence

        For example:

        .. code-block:: python

            # List all persons in the sentence
            for person in concept.find('Person')):
                print(person)

        :param uri: URI, or name, of the concept
        :type uri: ``str``

        :returns: The matching instances of the given concept
        :rtype: A ``list`` of :class:`Entity`
        """
        concept = Entity(self.begin_offset, self.end_offset, "Sentence")
        concept._sentence_annotations = self.annotations
        concept._annotation_idx = 0
        return concept.find(uri)

    def __getitem__(self, value):
        return self.annotations[value] if value < len(self.annotations) else None

    @property
    def text(self):
        """
        :return: A string representation of the sentence
        :rtype: ``str``
        """
        retval = ""
        prev_tk = None
        for tk in [a for a in self.annotations if a.is_token]:
            if prev_tk:
                if prev_tk.end_offset != tk.begin_offset:
                    retval += " "
            retval += tk.literal
            prev_tk = tk
        return retval.strip()

    @property
    def stems(self):
        """
        :return: A string representation of the sentence with the stems
        :rtype: ``str``
        """
        if self.text_ is None:
            retval = ""
            prev_tk = None
            for tk in [a for a in self.annotations if a.is_token]:
                if prev_tk:
                    if prev_tk.end_offset != tk.begin_offset:
                        retval += " "
                retval += tk.stem
                prev_tk = tk
            self.text_ = retval.strip()
        return self.text_

    @property
    def is_header(self) -> bool:
        """
        :return: True if the sentence is a header
        :rtype: ``bool``
        """
        return self.attributes.get("header", []) == ["true"]

    def concepts(self, filter=_filter_pass_thru_concept):
        """
        Access the concepts in the analysis of the document

        :param filter: Optional filter to select or discard concepts
        :type filter: Functor accepting a :class:`Entity <wowool.annotation.entity.Entity>` and returning a ``bool``

        :return: A generator expression yielding the concepts in the processed document
        :rtype: :class:`Concepts <wowool.annotation.entity.Entity>`
        """
        yield from Entity.iter(self, filter)

    @staticmethod
    def _document_iter(doc, filter: FilterType = _filter_pass_thru) -> Iterator[Entity]:
        for sentence in doc:
            for annotation in sentence:
                if annotation.is_concept and filter(annotation):
                    yield annotation

    @staticmethod
    def _paragraph_iter(paragraph, filter: FilterType = _filter_pass_thru) -> Iterator[Entity]:
        for sentence in paragraph.sentences:
            yield sentence

    @staticmethod
    def iter(object, filter: FilterType = _filter_pass_thru, align: bool = True) -> Iterator[Self]:
        """
        Iterate over the concepts in a document, an analysis, a sentence or a concept. For example:

        .. code-block:: python

            document = analyzer("Hello from Antwerp, said John Smith.")
            for concept in Sentence.iter(document, lambda concept : concept.uri == "NP"):
                print(concept)

        :param object: Object to iterate
        :type object: :class:`Analysis <wowool.analysis.Analysis>`, :class:`Sentence <wowool.annotation.sentence.Sentence>` or :class:`Sentence <wowool.annotation.concept.Sentence>`
        :param filter: Predicate function to filter the concepts, callable that accepts a concept and returns True if the concept is considered a match
        :type filter: Callable accepting a :class:`Sentence` and returning a ``bool``

        :return: A generator expression yielding concepts
        :rtype: :class:`Sentence <wowool.annotation.concept.Sentence>`
        """
        from wowool.document.analysis.document import AnalysisDocument
        from wowool.document.analysis.analysis import Analysis
        from wowool.annotation.paragraph import Paragraph

        if isinstance(object, AnalysisDocument) and object.analysis:
            yield from Sentence._document_iter(object.analysis, filter)
        elif isinstance(object, Analysis):
            yield from Sentence._document_iter(object, filter)
        elif isinstance(object, Paragraph):
            yield from Sentence._paragraph_iter(object, filter)
        else:
            raise TypeError(f"Expected Document, Analysis, Sentence, or Entity but got '{type(object)}'")
