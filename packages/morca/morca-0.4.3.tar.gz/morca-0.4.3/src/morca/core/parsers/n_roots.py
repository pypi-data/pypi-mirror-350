from pathlib import Path


def parse_n_roots(file: str | Path) -> int:
    for line in Path(file).read_text().splitlines():
        if "Number of roots to be determined" in line:
            return int(line.split()[-1])
    raise ValueError("N_roots not found")
