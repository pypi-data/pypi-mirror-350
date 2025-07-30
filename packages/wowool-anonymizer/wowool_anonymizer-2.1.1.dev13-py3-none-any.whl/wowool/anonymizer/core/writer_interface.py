from typing import Protocol, runtime_checkable, Any
from wowool.annotation import Concept


@runtime_checkable
class WriterInterface(Protocol):

    def anonymize(self, concept: Concept):
        """
        return a formatted str or anonymized literal for the given literal with the given uri.

        :param concept: concept that needs to be anonymized
        :type concept: Concept
        """
        return "***"

    def write(self, bytes_data: str):
        """write the given data to the output result"""
        pass

    def clear(self):
        """clear the output data of the writer"""
        pass

    def get_value(self) -> dict[str, Any]:
        """return the output data of the writer"""
        pass
