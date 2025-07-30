from wowool.annotation import Token
from wowool.annotation import Entity
from wowool.annotation import Sentence
from wowool.document.analysis.document import AnalysisDocument


# TODO: make visit a member method of the base class
def Visit(object, parent):
    """
    Visit the a annotation object like Document or Sentence and call back using
    the functions __token__ or __concept__ or __sentence__

    .. code-block:: python
    :linenos:

        import wowool
        from wowool.native import Language
        from wowool.native import Domain

        class MyVisitor:
            def __token__(self, token):
                print(token)

        analyzer = Language(domains='english-entity.dom')
        entities = Domain(domains='english-entity.dom')
        doc = analyzer("Philippe Forest works in EyeOnText.")
        wowool.Visit(doc, MyVisitor)
    """
    visit_concept = hasattr(parent, "__concept__")
    visit_token = hasattr(parent, "__token__")
    visit_init_sentence = hasattr(parent, "__init_sentence__")
    visit_uninit_sentence = hasattr(parent, "__uninit_sentence__")

    if visit_token and isinstance(object, Token):
        parent.__token__(object)
    elif visit_concept and isinstance(object, Entity):
        parent.__concept__(object)
    elif isinstance(object, Sentence):
        if visit_init_sentence:
            parent.__init_sentence__(object)
        for aa in object:
            Visit(aa, parent)
        if visit_uninit_sentence:
            parent.__uninit_sentence__(object)
    elif isinstance(object, AnalysisDocument):
        for aa in object:
            Visit(aa, parent)
