from wowool.document.analysis.analysis import Analysis
from wowool.annotation import Concept


class HasNotBeenProcessedByLanguage(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Document was not processed by a Language.")


def remove_pos(analysis: Analysis, begin_offset: int, end_offset: int, pos: str, unicode_offset=True):
    assert isinstance(analysis, Analysis)
    if analysis._cpp:
        analysis.reset()
        return analysis._cpp.remove_pos(begin_offset, end_offset, pos, unicode_offset)
    else:
        raise HasNotBeenProcessedByLanguage()


def get_internal_concept(analysis: Analysis, concept: Concept, unicode_offset=True):
    assert isinstance(analysis, Analysis)
    if analysis._cpp:
        return analysis._cpp.get_concept(concept.begin_offset, concept.end_offset, concept.uri, unicode_offset)
    else:
        raise HasNotBeenProcessedByLanguage


def get_internal_concept_args(analysis: Analysis, begin_offset, end_offset, uri, unicode_offset=True):
    assert isinstance(analysis, Analysis)
    if analysis._cpp:
        return analysis._cpp.get_concept(begin_offset, end_offset, uri, unicode_offset)
    else:
        raise HasNotBeenProcessedByLanguage


def add_internal_concept(analysis: Analysis, begin_offset, end_offset, uri, unicode_offset=True):
    assert isinstance(analysis, Analysis)
    if analysis._cpp:
        analysis.reset()
        return analysis._cpp.add_concept(begin_offset, end_offset, uri, unicode_offset)
    else:
        raise HasNotBeenProcessedByLanguage


def add_internal_concept_attribute(analysis: Analysis, internal_concept, key, value):
    assert isinstance(analysis, Analysis)
    if analysis._cpp:
        analysis.reset()
        internal_concept.add_attribute(key, value)
    else:
        raise HasNotBeenProcessedByLanguage


def remove_internal_concept_attribute(analysis: Analysis, internal_concept):
    assert isinstance(analysis, Analysis)
    if analysis._cpp:
        analysis.reset()
        internal_concept.remove()
    else:
        raise HasNotBeenProcessedByLanguage


# renaming the function above with breaking stuff
def remove_internal_concept(analysis: Analysis, internal_concept):
    assert isinstance(analysis, Analysis)
    if analysis._cpp:
        analysis.reset()
        internal_concept.remove()
    else:
        raise HasNotBeenProcessedByLanguage


def get_byte_offset(analysis: Analysis, offset):
    assert isinstance(analysis, Analysis)
    if analysis._cpp:
        return analysis._cpp.get_byte_offset(offset)
    else:
        raise HasNotBeenProcessedByLanguage
