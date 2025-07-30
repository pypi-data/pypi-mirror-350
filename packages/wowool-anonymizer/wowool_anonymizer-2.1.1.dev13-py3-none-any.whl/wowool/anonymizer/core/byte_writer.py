from wowool.anonymizer.core.writer_interface import WriterInterface
from random import randint
import copy
from wowool.annotation import Concept


class ByteWriter(WriterInterface):
    """
    This object will rewrite the original document.

    :param dummies: A dictionary that has a list of fake names for a given uri. Example: { "Person" : ["Hulk","Flash"] }
    :type dummies: dict( uri: list(names) )
    :param formatters: Format how an entity should be displayed in the document. Example: { "Person" : "{anonymized_literal}" }
    :type formatters: dict(uri, fstring format), internal variables that can be used. anonymized_literal, uri, nr, literal
    """

    def __init__(
        self,
        dummies={},
        formatters=None,
        using_byte_offset=False,
    ):
        self.dummies = copy.deepcopy(dummies)
        self.formatters = formatters
        self.clear()
        self.reset_document_data()
        self.using_byte_offset = using_byte_offset

    def reset_document_data(self):
        """clear the known_entries of the writer, which means that previous entries will not be the same in the following document"""
        self.counter, self.known_entries = {}, {}

    def clear(self):
        """clear the output data of the writer"""
        if self.using_byte_offset:
            self.out = b""
        else:
            self.out = ""

    def _add_literal_data(self, uri, literal):
        if uri not in self.counter:
            self.counter[uri] = 0
        self.counter[uri] += 1
        self.known_entries[literal] = {
            "uri": f"{uri}_{self.counter[uri]}",
            "nr": self.counter[uri],
        }

    def anonymize(self, concept: Concept):
        """
        return a formated str or anonymized literal for the given literal with the given uri.

        :param uri: uri for the given literal
        :type uri: str
        :param literal: literal that needs to be anonymized
        :type literal: str

        """
        uri, literal = concept.uri, concept.literal
        if literal not in self.known_entries:
            if uri in self.dummies and len(self.dummies[uri]) > 0:
                candidates = self.dummies[uri]
                if candidates:

                    item_index = randint(0, len(candidates) - 1)
                    self.known_entries[literal] = {
                        "uri": candidates[item_index],
                        "nr": "0",
                    }
                    # remove this one from the list to avoid duplicates
                    del candidates[item_index]
                else:
                    self._add_literal_data(uri, literal)
            else:
                self._add_literal_data(uri, literal)
        anonymized_literal = self.known_entries[literal]["uri"]

        if self.formatters:
            nr = "not_set"
            if "nr" in self.known_entries[literal]:
                nr = self.known_entries[literal]["nr"]
            if uri in self.formatters:
                return eval('f"' + self.formatters[uri] + '"')
            elif "all" in self.formatters:
                return eval('f"' + self.formatters["all"] + '"')
        return anonymized_literal

    def write(self, bytes_data):
        """write the given data to the output result"""
        self.out += bytes_data

    def get_value(self):
        """return output result"""
        return self.out.decode()

    def get_bytes(self):
        """return output result"""
        return self.out
