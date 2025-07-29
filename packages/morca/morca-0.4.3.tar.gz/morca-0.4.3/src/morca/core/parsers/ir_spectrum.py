from pathlib import Path

import polars as pl


def parse_ir_spectrum(file: str | Path) -> pl.DataFrame:
    lines = Path(file).read_text().splitlines()
    lines = [line.strip() for line in lines]

    HEADER: str = "IR SPECTRUM"
    HEADER_OFFSET: int = 6
    table_start = lines.index(HEADER) + HEADER_OFFSET

    rows = []
    for row in lines[table_start:]:
        if not row.strip():
            break
        rows.append(row)

    data = []
    for line in rows:
        mode, freq, eps, intensity, t2, *_ = line.split()

        mode = mode.strip(":")

        data.append(
            [
                int(mode),
                float(freq),
                float(eps),
                float(intensity),
                float(t2),
            ]
        )

    df = pl.DataFrame(
        data,
        schema=[
            "mode",
            "freq",
            "eps",
            "intensity",
            "t2",
        ],
        orient="row",
    )
    return df
