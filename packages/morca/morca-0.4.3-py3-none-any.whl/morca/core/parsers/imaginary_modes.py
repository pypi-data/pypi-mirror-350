from pathlib import Path


def parse_imaginary_modes(file: str | Path) -> list:
    """Parse imaginary modes from an ORCA output file.

    Returns None if there aren't any
    """
    imaginary_modes = []
    for line in Path(file).read_text().splitlines():
        if "***imaginary mode***" in line:
            mode, freq, *_ = line.strip().replace(":", "").split()
            imaginary_modes.append([mode, freq])
    return imaginary_modes
