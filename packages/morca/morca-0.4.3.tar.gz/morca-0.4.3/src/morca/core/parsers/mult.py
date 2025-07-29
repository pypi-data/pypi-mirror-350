from pathlib import Path


def parse_mult(file: str | Path) -> int:
    """Parse the mult from an ORCA output file."""
    for line in Path(file).read_text().splitlines():
        if line.strip().startswith("Multiplicity"):
            return int(line.split()[-1])
    raise ValueError("Failed to parse mult")
