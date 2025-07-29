from pathlib import Path


def parse_tda(file: str | Path) -> bool:
    for line in Path(file).read_text().splitlines():
        if "Tamm-Dancoff approximation     ... deactivated" in line:
            return False
        elif "Tamm-Dancoff approximation     ... operative" in line:
            return True
    raise ValueError("No TDA information found in file")
