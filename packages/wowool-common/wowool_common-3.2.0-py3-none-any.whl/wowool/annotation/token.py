from __future__ import annotations
from wowool.annotation.annotation import Annotation, ErrorAnnotationNotFound
from typing import List, MutableSet, Union, cast, Generator


from typing import NewType

Entity = NewType("Entity", Annotation)
TokenType = NewType("TokenType", Annotation)


class Token(Annotation):
    """
    :class:`Token` is a class that contains all the information of a token
    """

    __slots__ = ["literal", "morphology", "properties"]

    def __init__(self, begin_offset: int, end_offset: int, literal: str):
        """
        Initialize a :class:`Token` instance

        :param begin_offset: Begin offset of the token
        :type begin_offset: ``int``
        :param end_offset: End offset of the token
        :type end_offset: ``int``
        :param literal: Literal string from the input document
        :type literal: ``str``

        :return: An initialized token
        :rtype: :class:`Token`
        """
        super(Token, self).__init__(begin_offset, end_offset)
        self.literal: str = literal
        self.morphology: List[MorphData] = []
        self.properties: MutableSet[str] = set()

        #  :param properties: the properties of the token.
        #  :type properties: set()
        #  :param morphology: the morphologic data information of the token.
        #  :type morphology: MorphData

    def rich(self):
        """
        :return: The rich string representation of the token
        :rtype: ``str``
        """
        retval = "<literal>T</literal>:" + Annotation.__repr__(self) + ": <literal>" + self.literal + "</literal>"
        if self.properties:
            retval += ",{"
            for idx, prop in enumerate(sorted(self.properties)):
                if idx != 0:
                    retval += ", "
                retval += "+" + prop
            retval += "}"

        if self.morphology:
            retval += ","
            for morph_info in self.morphology:
                retval += morph_info.rich()

        return retval

    def __repr__(self):
        retval = "T:" + Annotation.__repr__(self) + ": " + self.literal
        if self.properties:
            retval += ",{"
            for idx, prop in enumerate(sorted(self.properties)):
                if idx != 0:
                    retval += ", "
                retval += "+" + prop
            retval += "}"

        if self.morphology:
            retval += ","
            for morph_info in self.morphology:
                retval += str(morph_info)

        return retval

    @property
    def stem(self) -> str:
        """
        :return: The first stem of the token or an empty string if absent
        :type: ``str``
        """
        for morph_info in self.morphology:
            return morph_info.stem
        return ""

    @property
    def pos(self) -> str:
        """
        :return: The first part-of-speech of the token or an empty string if absent
        :type: ``str``
        """
        for morph_info in self.morphology:
            return morph_info.pos
        return ""

    def has_property(self, prop: str) -> bool:
        """
        :param prop: Property name. For example ``"NF"``
        :type prop: ``str``

        :return: Whether a given property is set on the token
        :rtype: ``bool``
        """
        return prop in self.properties

    def has_pos(self, pos: str) -> bool:
        """
        :param pos: Part-of-speech. For example ``"Nn"``
        :type pos: ``str``

        :return: Whether a given part-of-speech is set on the token
        :rtype: ``bool``
        """
        for morph_info in self.morphology:
            if morph_info.pos.startswith(pos):
                return True
        return False

    def get_morphology(self, pos: str):
        """
        :param pos: Part-of-speech. For example ``"Nn"``
        :type pos: ``str``

        :return: Whether a given part-of-speech is set on the token
        :rtype: ``bool``
        """
        for morph_info in self.morphology:
            if morph_info.pos.startswith(pos):
                return morph_info

    def __len__(self) -> int:
        """
        :returns: The length of the token in the input document in bytes. This takes into account unicode characters
        :type: ``int``
        """
        return self.end_offset - self.begin_offset

    def __bool__(self) -> bool:
        return self._begin_offset != -1

    @staticmethod
    def _document_iter(document) -> Generator[Token, None, None]:
        for sentence in document:
            for annotation in sentence:
                if annotation.is_token:
                    yield cast(Token, annotation)

    @staticmethod
    def _concept_iter(concept) -> Generator[Token, None, None]:
        for annotation in concept.annotations:
            if annotation.is_token:
                yield cast(Token, annotation)

    @staticmethod
    def iter(object) -> Generator[Token, None, None]:
        """
        Iterate over the concepts in a document, an analysis, a sentence or a concept. For example:

        .. code-block:: python

            document = analyzer("Hello from Antwerp, said John Smith.")
            for token in Token.iter(document):
                print(token)

        :param object: Object to iterate
        :type object: :class:`Analysis <wowool.analysis.Analysis>`, :class:`Sentence <wowool.annotation.sentence.Sentence>` or :class:`Entity <wowool.annotation.entity.Entity>`

        :return: A generator expression yielding tokens
        :rtype: :class:`Token <wowool.annotation.token.Token>`
        """
        from wowool.document.analysis.document import AnalysisDocument
        from wowool.document.analysis.analysis import Analysis
        from wowool.annotation import Sentence, Entity

        if isinstance(object, AnalysisDocument) and object.analysis:
            yield from Token._document_iter(object.analysis)
        elif isinstance(object, Analysis):
            yield from Token._document_iter(object)
        elif isinstance(object, Sentence):
            for annotation in object:
                if isinstance(annotation, Token):
                    yield cast(Token, annotation)
        elif isinstance(object, Entity):
            yield from Token._concept_iter(object)
        else:
            raise TypeError(f"Expected Document, Analysis, Sentence, or Entity but got '{type(object)}'")

    @staticmethod
    def next(sentence, object) -> Token:
        """returns the next Token"""
        index = object.index + 1
        sentence_length = len(sentence)
        while index < sentence_length:
            if sentence[index].is_token:
                return cast(Token, sentence[index])
            else:
                index += 1
        raise ErrorAnnotationNotFound

    @staticmethod
    def prev(sentence, object: Union[Entity, Token]) -> Token:
        """returns the prev Token"""
        index = object.index - 1
        while index >= 0:
            if sentence[index].is_token:
                return cast(Token, sentence[index])
            else:
                index -= 1
        raise ErrorAnnotationNotFound


class MorphData:
    """
    :class:`MorphData` is a class that contains the morphological data. For example:

    .. code-block:: python

        for md in token.morphology:
            print( md.pos , md.stem )

    :param pos: Part-of-speech
    :type pos: ``str``
    :param stem: Stem
    :type stem: ``str``
    """

    def __init__(self):
        self.pos: str = "None"
        self.stem: str = ""

    def rich(self) -> str:
        """
        :return: The rich string representation of the morphological data
        :rtype: ``str``
        """
        retval = "['<stem>" + self.stem + "</stem>':" + self.pos + "]"
        if hasattr(self, "morphology"):
            self.morphology: List[MorphData]
            for md in self.morphology:
                retval += md.rich()
        return retval

    def __repr__(self) -> str:
        retval = f"[{self.stem}:{self.pos}"
        if hasattr(self, "morphology"):
            retval += ",["
            self.morphology: List[MorphData]
            for md in self.morphology:
                retval += str(md)
            retval += "]"
        retval += "]"
        return retval

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __getstate__(self):
        return self.__dict__


TokenNone = Token(-1, -1, "")
