from wowool.document import DocumentInterface
from wowool.sdk import Pipeline
from wowool.anonymizer.core.anonymizer import Anonymizer, DefaultWriter
from sys import stderr
from pathlib import Path
from wowool.tools.anonymizer.writer_config import WriterConfig


class Writer:
    def __init__(self, writer_config: WriterConfig) -> Path:
        self.writer_config = writer_config
        self.suffix = "suffix" if writer_config.suffix is None else writer_config.suffix
        self.writer = DefaultWriter(
            writer_config.pseudonyms,
            writer_config.formatters,
            writer_config.fake_locale,
        )
        self.anonymizer = Anonymizer(
            writer_config.annotations,
            self.writer,
        )

    def __call__(self, document: DocumentInterface, pipeline: Pipeline):
        writer = self.writer
        anonymizer_ = self.anonymizer
        writer.set_input_data(document.data)

        document = pipeline(document)
        document = anonymizer_(document)
        if document.has_diagnostics():
            from wowool.utility.diagnostics import print_diagnostics

            print_diagnostics(document, file=stderr)
        else:
            input_file = Path(document.id)
            output_file = input_file.with_suffix(f"{self.suffix}{input_file.suffix}")
            with open(output_file, "wb") as f:
                f.write(writer.get_bytes())
            return output_file
