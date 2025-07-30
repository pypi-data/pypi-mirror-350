from __future__ import annotations
from wowool.annotation.annotation import Annotation, ErrorAnnotationNotFound
from wowool.annotation.token import Token
from typing import Callable, Union, List, cast, Generator, Iterator, Self


def _align(idx, collection) -> int:
    bo = collection[idx].begin_offset
    eo = collection[idx].end_offset
    rvidx = idx - 1
    while rvidx >= 0:
        if bo == collection[rvidx].begin_offset and eo == collection[rvidx].end_offset:
            rvidx -= 1
        else:
            return rvidx + 1
    return idx


def _filter_pass_thru(concept) -> bool:
    return True


class Entity(Annotation):
    """
    :class:`Entity` is a class that contains all the information of a concept
    """

    FilterType = Callable[[Self], bool]

    def __init__(self, begin_offset: int, end_offset: int, uri: str):
        """
        Initialize a :class:`Entity` instance

        :param begin_offset: Begin offset of the concept
        :type begin_offset: ``int``
        :param end_offset: End offset of the concept
        :type end_offset: ``int``
        :param uri: URI, or name, of the concept
        :type uri: ``str``

        :return: An initialized concept
        :rtype: :class:`Entity`
        """
        self._attributes = {}
        super(Entity, self).__init__(begin_offset, end_offset)
        self._uri = uri
        self._sentence_annotations = None
        self._annotations = None
        self._literals = None
        self._stems = None
        self._tokens = None
        self._dict = None
        self._canonical = None
        self._text = None

    @property
    def uri(self) -> str:
        """
        :return: The URI, or name, of the concept
        :type: ``str``
        """
        return self._uri

    @property
    def literal(self) -> str:
        """
        :return: The literal representation of the concept
        :rtype: ``str``
        """
        return self.text

    @property
    def literals(self) -> List[str]:
        """
        :return: The literals of the concept
        :rtype: A ``list`` of ``str``
        """
        if not self._literals:
            self._literals = [token.literal for token in self.tokens]
        return self._literals

    @property
    def stem(self) -> str:
        """
        :return: The stem representation of the concept
        :type: ``str``
        """
        return " ".join(self.stems)

    def has_canonical(self) -> bool:
        if "canonical" in self._attributes:
            return True
        elif "icanonical" in self._attributes:
            return True
        return False

    def _get_canonical(self) -> str:
        if "canonical" in self._attributes:
            return self._attributes["canonical"][0]
        elif "icanonical" in self._attributes:
            return self._attributes["icanonical"][0]
        elif self._has_guesses() or self._has_props():
            return self.literal
        return self.stem if self.stem else self.literal

    @property
    def canonical(self) -> str:
        """
        :return: The stem representation of the concept
        :type: ``str``
        """
        if self._canonical is None:
            self._canonical = self._get_canonical()
        return self._canonical

    @property
    def attributes(self):
        return self._attributes

    @property
    def stems(self) -> List[str]:
        """
        :return: The stems of the concept
        :rtype: A ``list`` of ``str``
        """
        if not self._stems:
            self._stems = [token.stem for token in self.tokens]
        return self._stems

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
    def text(self):
        """
        :return: A string representation of the concept
        :rtype: ``str``
        """
        if self._text is None:
            self._text = self._get_text()
        return self._text

    @property
    def tokens(self) -> List[Token]:
        """
        :return: The tokens of the concept
        :rtype: A ``list`` of ``str``
        """
        if not self._tokens:
            assert self._sentence_annotations is not None
            self._tokens = [
                annotation
                for annotation in self._sentence_annotations[self._annotation_idx :]
                if annotation.is_token and annotation.begin_offset < self.end_offset
            ]
        return self._tokens

    @property
    def annotations(self) -> List[Annotation]:
        """
        :return: The tokens of the concept
        :rtype: A ``list`` of ``str``
        """
        if not self._annotations:
            assert self._sentence_annotations is not None
            self._annotations = [
                annotation for annotation in self._sentence_annotations[self._annotation_idx :] if annotation.begin_offset < self.end_offset
            ]
        return self._annotations

    def set_attributes(self, new_attributes: dict):
        self._attributes = new_attributes

    def _has_guesses(self) -> bool:
        return len([tk for tk in self.tokens if "guess" in tk.properties]) > 0

    def _has_props(self) -> bool:
        for tk in self.tokens:
            if tk.has_pos("Prop"):
                return True
        return False

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __getstate__(self):
        return self.__dict__

    def __getattr__(self, name: str) -> Union[None, str, Entity]:
        """
        Find an attribute or the first child instance of the concept with the given name. Some often used attributes are:

        * ``canonical``: canonical representation (``str``) of the concept
        * ``attributes``: attributes (``dict``) collected on the concept

        For example:

        .. code-block:: python

            # Find a child concept in this concept
            person = concept.Person
            # or print the attribute 'gender'
            print(person.gender)

        :param name: Attribute name
        :type name: ``str``

        :return: The first instance of the matching concept or the requested attribute value
        :type: :class:`Entity` or ``str``
        """

        if name in self._attributes:
            return ",".join(self._attributes[name])
        concept = self.find_first(name)
        if concept:
            return cast(Entity, concept)

    def find_first(self, uri: str) -> Union[None, Entity]:
        """
        Find the first child instance of the concept with the given URI in this concept

        For example:

        .. code-block:: python

            # Find a child concept in the current concept
            person = concept.find_first('Person'))

        :param uri: URI, or name, of the concept
        :type uri: ``str``

        :returns: The first matching child instance of the given concept
        :rtype: :class:`Entity`
        """
        try:
            return next(self._find(uri))
        except StopIteration:
            return None

    def find(self, uri: str) -> List[Entity]:
        """
        Find all child concepts with the given URI in this concept

        For example:

        .. code-block:: python

            # Find a child concept in the current concept
            for person in concept.find('Person')):
                print(person)

        :param uri: URI, or name, of the concept
        :type uri: str

        :returns: The matching child instances of the given concept
        :rtype: A ``list`` of :class:`Entity`
        """
        return [concept for concept in self._find(uri)]

    def _find(self, uri: str) -> Generator[Entity, None, None]:
        assert self._sentence_annotations is not None
        idx = _align(self._annotation_idx, self._sentence_annotations)
        sent_len = len(self._sentence_annotations)
        while idx < sent_len:
            annotation = self._sentence_annotations[idx]
            if annotation.is_concept and uri == cast(Entity, annotation).uri:
                yield cast(Entity, annotation)
            elif annotation.is_token:
                if annotation.begin_offset < self.end_offset:
                    pass
                else:
                    return
            idx += 1

    def match(self, call_able: Callable[[str], bool]) -> List[Entity]:
        """
        Find all child concepts with the given URI in this concept

        For example:

        .. code-block:: python

            # Find a child concept in the current concept
            for person in concept.find('Person')):
                print(person)

        :param uri: URI, or name, of the concept
        :type uri: str

        :returns: The matching child instances of the given concept
        :rtype: A ``list`` of :class:`Entity`
        """
        return [concept for concept in self._match(call_able)]

    def _match(self, call_able: Callable[[str], bool]) -> Generator[Entity, None, None]:
        assert self._sentence_annotations is not None
        idx = _align(self._annotation_idx, self._sentence_annotations)
        sent_len = len(self._sentence_annotations)
        while idx < sent_len:
            annotation = self._sentence_annotations[idx]
            if annotation.is_concept and call_able(cast(Self, annotation).uri):
                yield cast(Entity, annotation)
            elif annotation.is_token:
                if annotation.begin_offset < self.end_offset:
                    pass
                else:
                    return
            idx += 1

    def __getitem__(self, key):
        """
        :return: Attribute of the concept
        :rtype: ``str``
        """
        if self._dict and key in self._dict:
            return self._dict[key]

    def rich(self) -> str:
        """
        :return: A rich string representation of the entity
        :rtype: ``str``
        """
        retval = "<uri>C</uri>:" + Annotation.__repr__(self) + ": <uri>" + self.uri + "</uri>"
        if self._attributes:
            retval += ",@(<default>"
            for k, vs in sorted(self._attributes.items()):
                for v in vs:
                    retval += f"{k}='{v}' "
            retval += "</default>)"
        return retval

    def keys(self):
        """
        This function is used to convert a entity object to a dictionary

        .. code-block:: python

            { **entity }


        :return: a list of the keys of the entity.
        :rtype: list(str)


        """
        if not self._dict:
            self._dict = self.to_json()
        return self._dict.keys()

    def __repr__(self) -> str:
        retval = "C:" + Annotation.__repr__(self) + ": " + self.uri
        if self._attributes:
            retval += ",@("
            for k, vs in sorted(self._attributes.items()):
                for v in vs:
                    retval += f"{k}='{v}' "
            retval += ")"
        return retval

    def to_json(self):
        """
        :return: A dictionary representing a JSON object of the concept
        :rtype: ``dict``
        """
        dict_self = {"uri": self.uri, "literal": self.literal, "stem": self.stem}
        dict_attributes = {}
        for k, vl in self._attributes.items():
            dict_attributes[k] = ",".join([str(v) for v in vl])
        return {**dict_self, **dict_attributes}

    @staticmethod
    def _document_iter(doc, filter: FilterType = _filter_pass_thru) -> Iterator[Entity]:
        for sentence in doc:
            for annotation in sentence:
                if annotation.is_concept and filter(annotation):
                    yield annotation

    @staticmethod
    def _sentence_iter(sentence, filter: FilterType = _filter_pass_thru) -> Iterator[Entity]:
        for annotation in sentence:
            if annotation.is_concept and filter(annotation):
                yield annotation

    @staticmethod
    def _concept_iter(concept, filter: FilterType = _filter_pass_thru, align: bool = True) -> Iterator[Entity]:
        idx = _align(concept._annotation_idx, concept._sentence_annotations) if align else concept._annotation_idx + 1
        N = len(concept._sentence_annotations)
        while idx < N:
            if concept._annotation_idx != idx:
                annotation = concept._sentence_annotations[idx]
                if annotation.begin_offset >= concept.end_offset:
                    break
                if annotation.is_concept and filter(annotation) and annotation.end_offset <= concept.end_offset:
                    yield cast(Entity, annotation)
            idx += 1

    @staticmethod
    def iter(object, filter: FilterType = _filter_pass_thru, align: bool = True) -> Iterator[Entity]:
        """
        Iterate over the concepts in a document, an analysis, a sentence or a concept. For example:

        .. code-block:: python

            document = analyzer("Hello from Antwerp, said John Smith.")
            for entity in Entity.iter(document, lambda concept : concept.uri == "NP"):
                print(entity)

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
            yield from Entity._document_iter(object.analysis, filter)
        elif isinstance(object, Analysis):
            yield from Entity._document_iter(object, filter)
        elif isinstance(object, Sentence):
            yield from Entity._sentence_iter(object, filter)
        elif isinstance(object, Entity):
            yield from Entity._concept_iter(object, filter, align)
        else:
            raise TypeError(f"Expected Document, Analysis, Sentence, or Entity but got '{type(object)}'")

    @staticmethod
    def next(sentence: List[Annotation], object) -> Entity:
        """returns the next Entity"""
        index = object.index + 1
        sentence_length = len(sentence)
        while index < sentence_length:
            if sentence[index].is_concept:
                return cast(Entity, sentence[index])
            else:
                index += 1
        raise ErrorAnnotationNotFound

    @staticmethod
    def prev(sentence: List[Annotation], object) -> Entity:
        """returns the prev Entity"""
        index = object.index - 1
        while index >= 0:
            if sentence[index].is_concept:
                return cast(Entity, sentence[index])
            else:
                index -= 1
        raise ErrorAnnotationNotFound

    def set_sentence_annotations_index(self, sentence_annotations: list[Annotation], annotation_idx: int):
        self._sentence_annotations = sentence_annotations
        self._annotation_idx = annotation_idx

    def get_attribute(self, key: str):
        return self._attributes[key][0]

    def get_attributes(self, key: str):
        return self._attributes[key]
