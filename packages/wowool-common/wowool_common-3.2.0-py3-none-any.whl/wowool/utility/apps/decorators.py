import logging
from wowool.diagnostic import Diagnostics, Diagnostic, DiagnosticType
from wowool.document.analysis.document import AnalysisDocument
from functools import wraps
from wowool.document.analysis.analysis import APP_ID as APP_ID_ANALYSIS

logger = logging.getLogger(__name__)


def exceptions_to_diagnostics(fn):
    @wraps(fn)
    def wrapper(self, document: AnalysisDocument, *args, **kwargs):
        diagnostics = Diagnostics()
        app_id = self.ID if hasattr(self, "ID") else f"{type(self)}"
        try:
            document = fn(self, document, *args, diagnostics=diagnostics, **kwargs)
        except Exception as ex:
            # logger.exception(ex)
            if isinstance(document, AnalysisDocument):
                diagnostics.add(Diagnostic(document.id, f"Exception {ex}", DiagnosticType.Critical))
            else:
                raise ex
        if diagnostics:
            document.add_diagnostics(app_id, diagnostics)
        return document

    return wrapper


def requires_app(app_id):
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, document: AnalysisDocument, diagnostics: Diagnostics, *args, **kwargs):
            if not document.has(app_id):
                diagnostics.add(Diagnostic(document.id, f"Missing {app_id}", DiagnosticType.Critical))
                return document

            result = fn(self, document, *args, diagnostics=diagnostics, **kwargs)
            return result

        return wrapper

    return decorator


def requires_analysis(fn):
    @wraps(fn)
    def wrapper(self, document: AnalysisDocument, diagnostics: Diagnostics, *args, **kwargs):
        if not isinstance(document, AnalysisDocument):
            raise TypeError("Document must be an AnalysisDocument")
        if not document.has_results(APP_ID_ANALYSIS):
            diagnostics.add(Diagnostic(document.id, f"Missing language component ({APP_ID_ANALYSIS})", DiagnosticType.Critical))
            return document
        document = fn(self, document, *args, diagnostics=diagnostics, **kwargs)
        return document

    return wrapper


def check_requires_concepts(app_id, document: AnalysisDocument, diagnostics: Diagnostics, required_concepts, msg=None):
    if (
        not document.metadata
        or "concepts" in document.metadata
        and (document.metadata["concepts"] & required_concepts) != required_concepts
    ):
        if msg is None:
            missing_concepts = required_concepts - (document.metadata["concepts"] & required_concepts)
            msg = f"Missing a domain that can produce any of these required concepts: {missing_concepts}, add a domain domain in your pipeline."
        diagnostics.add(Diagnostic(document.id, msg, DiagnosticType.Warning))
        document.add_diagnostics(app_id, diagnostics)
