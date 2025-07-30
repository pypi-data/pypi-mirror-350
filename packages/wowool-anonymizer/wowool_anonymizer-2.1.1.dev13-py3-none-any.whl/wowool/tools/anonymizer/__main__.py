#!/usr/bin/python3
# ex :  python3 -m wowool.anonymizer  -f ~/dev/csv2_test/net.csv

from jsonargparse import ArgumentParser, ActionConfigFile, set_loader
from argparse import RawDescriptionHelpFormatter
import sys
from wowool.document.document_interface import DocumentInterface
from wowool.native.core.pipeline import Pipeline
from wowool.anonymizer.core.anonymizer import Anonymizer, DefaultWriter
from wowool.anonymizer.core.anonymizer_config import DEFAULT_PSEUDONYMS
from wowool.utility import clean_up_empty_keywords
from wowool.document import Document
from wowool.error import Error
from sys import stderr
from pathlib import Path
from wowool.utility.apps.yml_include import custom_yaml_load
from wowool.tools.anonymizer.writer_config import WriterConfig
from wowool.anonymizer.writers.factory.writer import Writer

set_loader("yaml_custom", custom_yaml_load)


def parse_arguments(argv):
    """
    The anonymizer is an EyeOnText tool that allows you to obscure data from documents

    Example: anonymizer -f ~/corpus/english  --pipeline english,entity --suffix '.out'
    """
    parser = ArgumentParser(
        prog="./anonymizer",
        fromfile_prefix_chars="@",
        formatter_class=RawDescriptionHelpFormatter,
        description=parse_arguments.__doc__,
    )

    parser.add_argument("-f", "--file", help="folder or file", required=True)
    parser.add_argument(
        "-p",
        "--pipeline",
        help="domains used to anonymize the document, without the anonymizer.app",
        required=True,
    )
    parser.add_argument(
        "-a", "--annotations", help="The entities that you want to anonymize"
    )

    parser.add_argument(
        "--formatters",
        help="description on how to format the output, dict[str,str]",
        default=None,
    )

    parser.add_argument(
        "--pseudonyms",
        help="dictionary of with list of pseudonyms, dict[str,list[str]]",
        default=None,
    )

    parser.add_argument("--suffix", help="suffix of the output files.")
    parser.add_argument("-c", "--config", action=ActionConfigFile)
    return parser.parse_args(argv)


def get_anonymizer(anonymizers, document: DocumentInterface, config, writer):

    if document.mime_type not in anonymizers:
        print(document.mime_type)
        anonymizers[document.mime_type] = Anonymizer(config.annotations, writer)
    return anonymizers[document.mime_type]


def get_writer(writers, document: DocumentInterface, config):

    if document.mime_type not in writers:
        print(document.mime_type)
        writer = DefaultWriter(config.pseudonyms, config.formatters)
        writers[document.mime_type] = writer
    return writers[document.mime_type]


def anonymizer(
    file,
    writer_config: WriterConfig,
    pipeline,
):

    ip_collection = [fn for fn in Document.glob(Path(file), raw=True)]
    try:
        pipeline_ = Pipeline(pipeline)

    except Error as ex:
        print(ex)
        exit(-1)

    writer = Writer(writer_config)
    for document in ip_collection:
        print(f"processing:{document.id} ...", file=stderr)
        output_fn = writer(document, pipeline_)
        print(f"file:{document.id} -> {output_fn}", file=stderr)


def main():
    args = dict(parse_arguments(sys.argv[1:])._get_kwargs())
    del args["config"]
    clean_up_empty_keywords(args)
    writer_config = WriterConfig(annotations=args["annotations"])
    if "formatters" in args:
        writer_config.formatters = args["formatters"]
        del args["formatters"]

    if "pseudonyms" in args:
        writer_config.pseudonyms = args["pseudonyms"]
        del args["pseudonyms"]
    else:
        writer_config.pseudonyms = DEFAULT_PSEUDONYMS

    anonymizer(
        writer_config=writer_config, file=args["file"], pipeline=args["pipeline"]
    )


if __name__ == "__main__":
    main()
