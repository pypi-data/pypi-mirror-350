from io import StringIO
from typing import Union, Any, Generator
from wowool.annotation import Entity, Annotation, Token, Sentence
import json
from wowool.diagnostic import Diagnostics
from wowool.document.analysis.analysis import (
    _filter_pass_thru_concept,
    Analysis,
    AnalysisInputProvider,
)
from wowool.document.analysis.analysis import APP_ID as APP_ID_ANALYSIS
from typing import cast
from wowool.document.analysis.apps.topics import convert_topics, Topic
from wowool.document.analysis.apps.themes import convert_themes, Theme
from wowool.document.analysis.apps.chunks import convert_chunks, Chunk
from wowool.document.document_interface import DocumentInterface, MT_PLAINTEXT, MT_ANALYSIS_JSON
from wowool.document.document import Document
from wowool.document.defines import WJ_ID, WJ_DATA, WJ_MIME_TYPE, WJ_METADATA, WJ_ENCODING
from json import JSONEncoder


RESULTS = "results"
DIAGNOSTICS = "diagnostics"


class AnalysisJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        else:
            return getattr(obj, "to_json")() if hasattr(obj, "to_json") else super().default(obj)


def to_json_convert(obj):
    if isinstance(obj, set):
        return str(list(obj))
    return obj


STR_MISSING_ANALYSIS = "Document has not been processed by a Language"


class AnalysisDocument(DocumentInterface):
    """
    :class:`Document` is a class that stores the data related to a document. Instances of this class are returned from a Pipeline, a Language or a Domain object.
    """

    MIME_TYPE = MT_ANALYSIS_JSON

    def __init__(self, document: DocumentInterface, metadata: dict | None = None):
        """
        Initialize a :class:`AnalysisDocument` instance
        """
        super().__init__()

        self.input_document = document
        self._metadata = metadata if metadata is not None else {**self.input_document.metadata}
        self._apps = {}

    @property
    def text(self) -> str | None:
        """
        :return: The text data of the document
        :rtype: ``str``
        """
        if self.input_document.mime_type == MT_PLAINTEXT:
            return self.input_document.data
        else:
            return None

    @property
    def id(self) -> str:
        """
        :return: The unique identifier of the document
        :rtype: ``str``
        """
        return self.input_document.id

    @property
    def mime_type(self) -> str:
        """
        :return: The data type of the document
        :rtype: 'MimeType'
        """
        return AnalysisDocument.MIME_TYPE

    @property
    def encoding(self) -> str:
        """
        :return: The data type of the document
        :rtype: 'MimeType'
        """
        return "json"

    @property
    def data(self) -> str:
        """
        :return: The text data of the document
        :rtype: 'str | None'
        """

        analysis_data = {"apps": self._apps}
        return json.loads(json.dumps(analysis_data, cls=AnalysisJsonEncoder))

    @property
    def metadata(self) -> dict:
        """
        :return: The metadata of the document
        :rtype: ``dict``
        """
        return self._metadata

    @property
    def analysis(self):
        """
        :return: The :class:`Analysis <wowool.analysis.Analysis>` of the document, containing the :class:`Sentences <wowool.annotation.sentence.Sentence>`, :class:`Tokens <wowool.annotation.token.Token>` and :class:`Concepts <wowool.annotation.entity.Entity>`, or ``None`` if the document has not been processed by a Language

        .. literalinclude:: ../../../../common/py/eot/wowool/init_document_analysis.py

        :rtype: :class:`Analysis <wowool.analysis.Analysis>`
        """
        return cast(Analysis, self.results(APP_ID_ANALYSIS))

    def app_ids(self):
        """
        Iterate over the application identifiers

        :return: A generator expression yielding application identifiers
        :rtype: ``str``
        """
        for app_id in self._apps:
            yield app_id

    def has(self, app_id: str) -> bool:
        return self.has_results(app_id)

    def has_results(self, app_id: str) -> bool:
        """
        :return: Whether the application, as identified by the given application identifier, is in the document
        :rtype: ``bool``
        """
        return app_id in self._apps

    def add_results(self, app_id: str, results):
        """
        Add the given application results to the document

        :param app_id: Application identifier
        :type app_id: ``str``
        :param results: Application results
        :type results: A JSON serializable object type
        """
        if app_id in self._apps:
            self._apps[app_id][RESULTS] = results
        else:
            self._apps[app_id] = {RESULTS: results}
        return results

    def results(self, app_id: str) -> Union[Any, None]:
        """
        :return: The results of the given application. See the different type of :ref:`application results <apps>`

        :param app_id: Application identifier
        :type app_id: ``str``
        :param defaults: The defaults result to create when the application identifier is not present
        :type default: Any JSON serializable object
        """
        if app_id in self._apps and RESULTS in self._apps[app_id]:
            return self._apps[app_id][RESULTS]

    def add_diagnostics(self, app_id: str, diagnostics: Diagnostics):
        """
        Add the given application diagnostics to the document

        :param app_id: Application identifier
        :type app_id: ``str``
        :param diagnostics: Application diagnostics
        :type diagnostics: :class:`Diagnostics <wowool.diagnostic.Diagnostics>`
        """
        if app_id in self._apps:
            self._apps[app_id][DIAGNOSTICS] = diagnostics
        else:
            self._apps[app_id] = {DIAGNOSTICS: diagnostics}

    def has_diagnostics(self, app_id: str | None = None) -> bool:
        """
        :param app_id: Application identifier
        :type app_id: ``str`` or ``None``
        :return: Whether the document contains diagnostics for the given application or any diagnostics if no application identifier is provided
        :rtype: ``bool``
        """
        if app_id is None:
            for app_id in self._apps:
                if DIAGNOSTICS in self._apps[app_id]:
                    return True
            return False
        else:
            if app_id in self._apps and DIAGNOSTICS in self._apps[app_id]:
                return True
            else:
                return False

    def diagnostics(self, app_id: str = None) -> Diagnostics:
        """
        :param app_id: Application identifier
        :type app_id: ``str`` or ``None``

        :return: The diagnostics of the given application. See the different type of :ref:`application results <apps>`
        :rtype: :class:`Diagnostics <wowool.diagnostic.Diagnostics>`
        """
        if app_id is None:
            diagnostics = Diagnostics()
            for _, app_data in self._apps.items():
                if DIAGNOSTICS in app_data:
                    diagnostics.extend(app_data[DIAGNOSTICS])
            return diagnostics
        else:
            if app_id in self._apps and DIAGNOSTICS in self._apps[app_id]:
                return self._apps[app_id][DIAGNOSTICS]
            else:
                raise ValueError(f"App '{app_id}' has no diagnostics")

    def to_json(self) -> dict:
        """
        :return: A dictionary representing a JSON object of the document
        :rtype: ``dict``
        """
        from json import JSONEncoder

        class Encoder(JSONEncoder):
            def default(self, obj):
                if isinstance(obj, set):
                    return list(obj)
                else:
                    return getattr(obj, "to_json")() if hasattr(obj, "to_json") else super().default(obj)

        document = {
            WJ_ID: self.id,
            WJ_MIME_TYPE: AnalysisInputProvider.MIME_TYPE,
            WJ_DATA: self.data,
            WJ_ENCODING: "json",
            WJ_METADATA: self.metadata,
        }
        return json.loads(json.dumps(document, cls=Encoder))

    @staticmethod
    def from_dict(document_json: dict) -> "AnalysisDocument":
        assert WJ_ID in document_json, "Invalid Document json format"
        assert WJ_MIME_TYPE in document_json, "Invalid Document json format"
        json_doc = document_json
        assert WJ_DATA in json_doc, "Invalid Document json format"
        assert "apps" in json_doc[WJ_DATA]

        input_document = Document.create(**json_doc)
        doc = AnalysisDocument(input_document)
        assert AnalysisInputProvider.MIME_TYPE == doc.mime_type
        doc._apps = input_document.data["apps"]

        if APP_ID_ANALYSIS in doc._apps:
            analysis_ = doc._apps[APP_ID_ANALYSIS]
            assert isinstance(analysis_, dict), f"Expected dict, not '{type(analysis_)}'"
            # phforest : this should no be a assert, in case we have errors there will be no results.
            # assert RESULTS in analysis_, f"Missing {RESULTS} in {APP_ID_ANALYSIS}"
            if RESULTS in analysis_:
                analysis = Analysis.parse(analysis_[RESULTS])
                # doc.input_document = AnalysisInputProvider(json.dumps(analysis_[RESULTS]), doc.id)
                doc.add_results(APP_ID_ANALYSIS, analysis)

        for _, app_data in doc._apps.items():
            if DIAGNOSTICS in app_data:
                app_data[DIAGNOSTICS] = Diagnostics.from_json(app_data[DIAGNOSTICS])

        return doc

    def concepts(self, filter=_filter_pass_thru_concept):
        """
        Access the concepts in the analysis of the document

        :param filter: Optional filter to select or discard concepts
        :type filter: Functor accepting a :class:`Entity <wowool.annotation.entity.Entity>` and returning a ``bool``

        :return: A generator expression yielding the concepts in the processed document
        :rtype: :class:`Concepts <wowool.annotation.entity.Entity>`
        """
        return self.analysis.concepts(filter) if self.analysis else iter([])

    def __repr__(self):
        if self.text:
            sz = len(self.text) if self.text else 0
            text = '"' + self.text[:50].strip().replace("\n", " ") + '"' if self.text else None
            return f"<AnalysisDocument id={self.id} mime_type={self.mime_type} size={sz} text={text} >"
        else:
            return "<AnalysisDocument id={self.id} mime_type={self.mime_type} >"

    def __str__(self):
        with StringIO() as output:
            if self.analysis:
                output.write(str(self.analysis))
            else:
                output.write(self.__repr__())
                output.write("\n")

            # print the rest of the applications.
            for app_id, app_data in self._apps.items():
                if app_id == APP_ID_ANALYSIS:
                    # we already have printed the self.analysis
                    continue

                if RESULTS in app_data:
                    output.write(f"{app_id}, {json.dumps(app_data[RESULTS], indent=2)}\n")
                elif DIAGNOSTICS in app_data:
                    output.write(f"{app_id}, {app_data[DIAGNOSTICS].to_json()}\n")

            return output.getvalue()

    @property
    def entities(self) -> Generator[Entity, Any, None]:
        """
        :return: The entities of the document
        :rtype: ``Generator``
        """
        if self.analysis is not None:
            yield from self.analysis.entities
        else:
            raise ValueError(STR_MISSING_ANALYSIS)

    @property
    def tokens(self) -> Generator[Token, Any, None]:
        """
        :return: The tokens of the document
        :rtype: ``Generator``
        """
        if self.analysis is not None:
            yield from self.analysis.tokens
        else:
            raise ValueError(STR_MISSING_ANALYSIS)

    @property
    def annotations(self) -> Generator[Annotation, Any, None]:
        """
        :return: The annotations of the document
        :rtype: ``list``
        """
        if self.analysis is not None:
            yield from self.analysis.annotations
        else:
            raise ValueError(STR_MISSING_ANALYSIS)

    @property
    def sentences(self) -> Generator[Sentence, Any, None]:
        """
        :return: The annotations of the document
        :rtype: ``list``
        """

        if self.analysis is not None:
            yield from self.analysis.sentences
        else:
            raise ValueError(STR_MISSING_ANALYSIS)

    @property
    def topics(self) -> list[Topic] | list:
        """
        :return: The topics of the document
        :rtype: ``list``
        """
        if self.has("wowool_topics"):
            return convert_topics(self.results("wowool_topics"))
        else:
            return []

    @property
    def categories(self) -> list[Theme] | list:
        """
        :return: The categories of the document
        :rtype: ``list``
        """
        if self.has("wowool_themes"):
            return convert_themes(self.results("wowool_themes"))
        else:
            return []

    @property
    def chunks(self) -> list[Chunk] | list:
        """
        :return: The chunks data of the document
        :rtype: ``list``
        """
        if self.has("wowool_chunks"):
            return convert_chunks(self.results("wowool_chunks"))
        else:
            return []

    @property
    def themes(self) -> list[Theme] | list:
        """
        :return: The categories of the document
        :rtype: ``list``
        """
        return self.categories

    @property
    def language(self):
        """
        :return: The language of the document
        :rtype: ``str``
        """
        if self.has("wowool_language_identifier"):
            return self.results("wowool_language_identifier")["language"]
        else:
            if self.has(APP_ID_ANALYSIS):
                language = self.results(APP_ID_ANALYSIS).language
                if "@" in language:
                    return language.split("@")[0]
                return self.results(APP_ID_ANALYSIS).language
            else:
                return None

    @staticmethod
    def deserialize(document: dict):
        """
        Deserialize a document from JSON format.
        :param document: JSON representation of the document.
        :return: Document object.
        :rtype: ``Document``
        """

        return AnalysisDocument.from_dict(document)
