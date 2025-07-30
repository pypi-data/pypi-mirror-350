from wowool.document import DocumentInterface
from wowool.sdk import Pipeline
from wowool.tools.anonymizer.writer_config import WriterConfig


class Writer:
    """
    Base class for all writers.
    """

    def __init__(self, writer_config: WriterConfig):
        self.writer_config = writer_config
        self.anonymizers = {}

    def get_anonymizer(self, mime_type):
        """
        Get the anonymizers for the writer.
        """
        if mime_type not in self.anonymizers:
            if mime_type == "text/plain":
                from wowool.anonymizer.writers.text.writer import Writer as TextWriter

                self.anonymizers[mime_type] = TextWriter(self.writer_config)
                return self.anonymizers[mime_type]
            elif mime_type == "application/pdf":
                from wowool.anonymizer.writers.pdf.writer import Writer as PdfWriter

                self.anonymizers[mime_type] = PdfWriter(self.writer_config)
                return self.anonymizers[mime_type]
        else:
            return self.anonymizers[mime_type]

    def __call__(self, document: DocumentInterface, pipeline: Pipeline):
        """
        Write the document to the specified path.
        """
        if not isinstance(document, DocumentInterface):
            raise TypeError("document must be an instance of DocumentInterface")
        if not isinstance(pipeline, Pipeline):
            raise TypeError("pipeline must be an instance of Pipeline")
        if anonymizer_ := self.get_anonymizer(document.mime_type):
            return anonymizer_(document, pipeline)
        else:
            raise NotImplementedError(f"Writer unknown data type: {document.mime_type}")
