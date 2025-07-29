from pathlib import Path


def parse_charge(file: str | Path) -> int:
    """Parse the charge from an ORCA output file."""
    for line in Path(file).read_text().splitlines():
        if line.strip().startswith("Total Charge"):
            return int(line.split()[-1])
    raise ValueError("Failed to parse charge")
