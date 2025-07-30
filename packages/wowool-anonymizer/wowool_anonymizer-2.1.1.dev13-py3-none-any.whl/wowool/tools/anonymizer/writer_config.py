from dataclasses import dataclass, field


@dataclass
class WriterConfig:
    formatters: dict[str, str] | None = None
    pseudonyms: dict[str, list[str]] | None = None
    fake_locale: list[str] | None = None  # ["en_US", "en_GB"]
    annotations: list[str] | None = None
    suffix: str = ".anonymized"
