from pathlib import Path

import polars as pl


def parse_absorption_spectrum(file: str | Path) -> pl.DataFrame:
    lines = Path(file).read_text().splitlines()
    lines = [line.strip() for line in lines]

    HEADER: str = "ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS"
    HEADER_OFFSET: int = 5
    table_start = lines.index(HEADER) + HEADER_OFFSET

    rows = []
    for row in lines[table_start:]:
        if not row.strip():
            break
        rows.append(row)

    data = []
    for line in rows:
        transition_from, _, transition_to, e_ev, e_cm, nm, fosc, *_ = line.split()

        from_state, from_mult = transition_from.split("-")
        to_state, to_mult = transition_to.split("-")
        from_mult = from_mult[:-1]
        to_mult = to_mult[:-1]

        data.append(
            [
                int(from_state),
                float(from_mult),
                int(to_state),
                float(to_mult),
                float(e_ev),
                float(e_cm),
                float(nm),
                float(fosc),
            ]
        )

    df = pl.DataFrame(
        data,
        schema=[
            "from_state",
            "from_mult",
            "to_state",
            "to_mult",
            "energy_ev",
            "energy_cm",
            "wavelength_nm",
            "fosc",
        ],
        orient="row",
    )
    return df
