from wowool.annotation import Concept
from faker import Faker
from functools import wraps
from random import randint
import copy
from wowool.anonymizer.core.writer_interface import WriterInterface
from wowool.anonymizer.core.defines import (
    KW_URI,
    KW_ANONYMIZED,
    KW_TEXT,
    KW_BEGIN_OFFSET,
    KW_END_OFFSET,
    KW_BYTE_BEGIN_OFFSET,
    KW_BYTE_END_OFFSET,
)


def check_faker(fn):
    @wraps(fn)
    def wrapper(self, concept: Concept, *args, **kwargs):
        if not self.fake:
            self.fake = Faker(self.fake_locale)
        return fn(self, concept, *args, **kwargs)

    return wrapper


class DefaultWriter(WriterInterface):
    """
    This object will rewrite the original document.

    :param dummies: A dictionary that has a list of fake names for a given uri. Example: { "Person" : ["Hulk","Flash"] }
    :type dummies: dict( uri: list(names) )
    :param formatters: Format how an entity should be displayed in the document. Example: { "Person" : "{anonymized_literal}" }
    :type formatters: dict(uri, fstring format), internal variables that can be used. anonymized_literal, uri, nr, literal

    """

    def __init__(
        self,
        pseudonyms={},
        formatters=None,
        fake_locale: list[str] | None = None,
    ):
        self.pseudonyms = copy.deepcopy(pseudonyms)
        self.formatters = formatters
        self.clear()
        self.reset_document_data()
        self.input_data_ = None
        self.locations = []
        self.fake = None
        self.fake_locale = ["en_US", "en_GB"] if not fake_locale else fake_locale

    @check_faker
    def random_instance(self, concept: Concept):
        retval = ""

        if concept.canonical not in self.known_entries:
            match concept.uri:
                case "Person":
                    gender = concept.gender
                    match gender:
                        case "male":
                            retval = self.fake.name_male()
                        case "female":
                            retval = self.fake.name_female()
                        case _:
                            retval = self.fake.name()
                case "Company":
                    retval = self.fake.company()
                case "Position":
                    retval = self.fake.job()
                case "Email":
                    retval = self.fake.free_email()
                case "Country":
                    retval = self.fake.country()
                case "City":
                    retval = self.fake.city()
                case "Address":
                    retval = self.fake.address()
                case _:
                    retval = "###"
            self.known_entries[concept.canonical] = {"uri": retval, "nr": 0}
            return retval
        else:
            return self.known_entries[concept.canonical]["uri"]

    def reset_document_data(self):
        """clear the known_entries of the writer, which means that previous entries will not be the same in the following document"""
        self.counter, self.known_entries = {}, {}

    def set_input_data(self, input_data: str):
        """set the input data of the writer"""
        self.input_data_ = input_data

    @property
    def input_data(self):
        """return the input data of the writer"""
        return self.input_data_

    def clear(self):
        """clear the output data of the writer"""
        self.out = ""
        self.locations = []
        self.input_data_ = None

    def _add_literal_data(self, concept: Concept, literal):
        retval = self.format_string(concept)
        if retval:
            self.known_entries[literal] = {"uri": retval, "nr": 0}
        else:
            uri = concept.uri
            self.update_uri_counter(uri)
            self.known_entries[literal] = {
                "uri": f"{uri}_{self.counter[uri]}",
                "nr": self.counter[uri],
            }

    def format_string(
        self, concept: Concept, anonymized_literal_candidate: str | None = None
    ):
        canonical = concept.canonical
        uri = concept.uri
        literal = concept.literal  # noqa
        kw_literal = canonical
        concept_format_string = concept.attributes.get("formatter", None)
        if self.formatters or concept_format_string:
            nr = "not_set"
            literal_data = self.known_entries.get(kw_literal, None)
            if literal_data is not None:
                nr = literal_data.get("nr", "not_set")
                anonymized_literal = literal_data.get(
                    "uri", anonymized_literal_candidate
                )
            else:
                nr = self.counter.get(uri, 1)
                anonymized_literal = anonymized_literal_candidate

            if anonymized_literal is None:
                anonymized_literal = f"{uri}_{nr}"
            anonymized = anonymized_literal  # noqa used in f-string

            if uri not in self.formatters and "default" in self.formatters:
                mapping_kw = "default"
            else:
                mapping_kw = uri

            if mapping_kw in self.formatters:
                if "fake" in self.formatters[mapping_kw]:
                    fake = self.random_instance(concept)  # noqa

                anonymized_literal = eval('f"""' + self.formatters[mapping_kw] + '"""')
                return anonymized_literal
            elif concept_format_string:
                anonymized_literal = eval('f"""' + anonymized_literal + '"""')
                return anonymized_literal
            else:
                return anonymized_literal

    def update_uri_counter(self, uri: str):
        """update the counter for the given uri"""
        if uri not in self.counter:
            self.counter[uri] = 1
        else:
            self.counter[uri] += 1

    def anonymize(self, concept: Concept):
        """
        return a formated str or anonymized literal for the given literal with the given uri.

        :param uri: uri for the given literal
        :type uri: str
        :param literal: literal that needs to be anonymized
        :type literal: str

        """
        uri = concept.uri
        kw_literal = concept.canonical
        if kw_literal not in self.known_entries:
            if (
                self.pseudonyms
                and uri in self.pseudonyms
                and len(self.pseudonyms[uri]) > 0
            ):
                candidates = self.pseudonyms[uri]
                if candidates:
                    self.update_uri_counter(uri)

                    item_index = randint(0, len(candidates) - 1)
                    retval = self.format_string(
                        concept, anonymized_literal_candidate=candidates[item_index]
                    )
                    anonymized_literal_ = retval if retval else candidates[item_index]

                    self.known_entries[kw_literal] = {
                        "uri": anonymized_literal_,
                        "nr": self.counter[uri],
                    }

                    # remove this one from the list to avoid duplicates
                    del candidates[item_index]
                else:
                    self._add_literal_data(concept, kw_literal)
            else:
                self._add_literal_data(concept, kw_literal)
        anonymized_literal = self.known_entries[kw_literal]["uri"]
        return anonymized_literal

    def write(self, bytes_data: str):
        """write the given data to the output result"""
        self.out += bytes_data

    def write_location(self, bytes_data: str, concept: Concept):
        """write the given data to the output result"""
        begin_offset = len(self.out)
        self.out += bytes_data
        end_offset = len(self.out)
        self.locations.append(
            {
                KW_BEGIN_OFFSET: begin_offset,
                KW_END_OFFSET: end_offset,
                KW_TEXT: concept.canonical,
                KW_URI: concept.uri,
                KW_ANONYMIZED: bytes_data,
                KW_BYTE_BEGIN_OFFSET: concept.begin_offset,
                KW_BYTE_END_OFFSET: concept.end_offset,
            }
        )

    def write_substr(self, start: int, end: int | None = None):
        """write the given data to the output result"""
        assert self.input_data_ is not None, "input data is not set"
        if end is None:
            self.out += self.input_data_[start:]
        else:
            self.out += self.input_data_[start:end]

    def get_value(self):
        """return output result"""
        return {"text": self.out, "locations": self.locations}

    def get_bytes(self):
        """return output result"""
        return self.out.encode()
