from wowool.diagnostic import Diagnostics, Diagnostic, DiagnosticType
from wowool.native.core.engine import Engine, default_engine
from wowool.native.core import Pipeline
from wowool.native.core.pipeline_resolver import resolve
from wowool.annotation import Concept
from wowool.error import Error
from random import randint
from wowool.document import Document
import copy
from wowool.utility.apps.decorators import (
    exceptions_to_diagnostics,
    requires_analysis,
    check_requires_concepts,
)
from wowool.document.analysis.document import AnalysisDocument
from wowool.document.factory import Factory
from wowool.anonymizer.core.app_id import APP_ID
from logging import getLogger
import re
from wowool.anonymizer.core.default_writer import DefaultWriter

logger = getLogger(__name__)

INVALID_FORMAT_STRING = re.compile("import|from")


def validate_format_string(format_string):
    """Validate the format string"""
    return True


def get_default_pseudonyms():
    from wowool.anonymizer.core.anonymizer_config import DEFAULT_PSEUDONYMS

    return DEFAULT_PSEUDONYMS


class Anonymizer:
    """
    This object traverses the given document and calls back the writer.
    The writer can format the document as you see fit. See DefaultWriter for more information on how to overwrite the Writer

    :param language: language to process
    :type language: str
    :param domains: list of domains to use.
    :type domains: str
    :param writer: Object used to format your output results.
    :type writer: callable object


    Using fake names.

    .. literalinclude:: ../../comp-wowool-anonymizer-py/samples/english_anonymize.py
        :caption: english_anonymize.py

    Using a formatter, note that you can set a formatter for every entity separately.

    .. literalinclude:: ../../comp-wowool-anonymizer-py/samples/english_anonymize_formatter.py
        :caption: english_anonymize_formatter.py


    """

    docs = """
# Anonymizer

The Anonymizer is a tool that can be used to anonymize text data. It can be used to replace sensitive information with fake names or other data. The Anonymizer can be used to replace names, addresses, phone numbers, and other sensitive information with fake data. The Anonymizer can be used to protect the privacy of individuals and organizations by replacing sensitive information with fake data.

## Arguments

- `annotations`: A list of annotations to anonymize. If not provided, all annotations will be anonymized.
- `pseudonyms`: A dictionary of fake names to use for each annotation. If not provided, a default list of fake names will be used.
- `formatters`: A dictionary of formatters to use for each annotation. If not provided, the default formatter will be used.

## Example

```
{
  "annotations": ["Person"],
  "pseudonyms": {
    "Person": ["John Doe", "Jane Smith"]
  },
  "formatters": {
    "Person": "###{anonymized_literal}###"
  },
}
```
"""

    ID = APP_ID

    def __init__(
        self,
        annotations: list[str] | None = None,
        writer=None,
        pseudonyms: dict[str, list[str]] | None = None,
        formatters: dict[str, str] | None = None,
        fake_locale: list[str] | None = None,
    ):
        self.pseudonyms = (
            pseudonyms if pseudonyms is not None else get_default_pseudonyms()
        )
        self.writer = (
            writer
            if writer
            else DefaultWriter(
                pseudonyms=self.pseudonyms,
                formatters=formatters,
                fake_locale=fake_locale,
            )
        )
        self.DEFAULT_SKIP_LIST = set(["Sentence", "VP", "NP", "Event"])
        # We use this so the we do not need all method.

        if annotations:
            if isinstance(annotations, str):
                self.annotations = set(annotations.split(","))
                self.document_level_annotations = self.annotations
            elif isinstance(annotations, list) or isinstance(annotations, set):
                self.annotations = set(annotations)
                self.document_level_annotations = self.annotations
            else:
                assert False, "Invalid object type for 'annotations' collection"
        else:
            self.annotations = None
            self.document_level_annotations = None

    @exceptions_to_diagnostics
    @requires_analysis
    def __call__(
        self, document: AnalysisDocument, diagnostics: Diagnostics
    ) -> AnalysisDocument:
        """
        process a InputProvider of str. The result will be stored by the writer.

        :param input_provider: InputProvider
        :type input_provider: str or InputProvider
        """

        if self.document_level_annotations is None:
            self.document_level_annotations = set(document.metadata["concepts"])

        self.writer.clear()
        self.writer.reset_document_data()
        self.writer.set_input_data(document.text)
        begin_section_offset = 0
        begin_offset = 0
        for concept in Concept.iter(document):
            if (
                concept.uri in self.document_level_annotations
                and concept.begin_offset >= begin_offset
            ):
                anonymized_data = self.writer.anonymize(concept)
                begin_offset = concept.begin_offset
                self.writer.write_substr(begin_section_offset, begin_offset)
                self.writer.write_location(anonymized_data, concept)

                begin_section_offset = concept.end_offset
                begin_offset = concept.end_offset

        self.writer.write_substr(begin_section_offset, None)
        if results := self.writer.get_value():
            document.add_results(APP_ID, results)
        return document
