from dataclasses import dataclass


@dataclass
class HeaderOption:
    title: str
    offset: int


def find_table_start(
    lines: list[str], header_options: HeaderOption | list[HeaderOption]
) -> int:
    # Normalize to a list
    if isinstance(header_options, HeaderOption):
        header_options = [header_options]

    for idx, line in enumerate(lines):
        for header in header_options:
            if header.title == line.strip():
                return idx + header.offset
    raise ValueError(f"None of the headers {header_options} were found.")
