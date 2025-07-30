#!python
import sys
from pathlib import Path
import json
from wowool.anonymizer.pdf.transform import anonymize_pdf_document


DEFAULT_CONFIG = {
    "pipeline": [
        "swedish",
        "actapublica",
        {
            "name": "anonymizer.app",
            "options": {
                "annotations": ["Person", "City", "PersonalIdentificationNumber"],
                "formatters": {"Person": "#{uri}_{nr}#"},
            },
        },
    ]
}


def main() -> None:
    args = sys.argv
    if len(args) >= 2:
        input_pdf_path = Path(args[1])
        if len(args) >= 3:
            output_pdf_path = Path(args[2])
        else:
            output_pdf_path = input_pdf_path.with_suffix(".anonymized.pdf")
        application_config_fn = Path(args[0]).with_suffix(".json")
        if application_config_fn.exists():
            with open(application_config_fn, "r") as f:
                config = json.load(f)
        else:
            config = DEFAULT_CONFIG
        anonymize_pdf_document(input_pdf_path, config, output_pdf_path)
    else:
        print("Usage: python pdf_wow_anonymizer.py <input_pdf_path> [<output_pdf_path>]")
        sys.exit(1)


if __name__ == "__main__":

    main()
