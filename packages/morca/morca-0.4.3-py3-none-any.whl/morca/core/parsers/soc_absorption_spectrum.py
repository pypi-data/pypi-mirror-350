from pathlib import Path

import polars as pl


def parse_soc_absorption_spectrum(file: str | Path) -> pl.DataFrame:
    lines = Path(file).read_text().splitlines()
    lines = [line.strip() for line in lines]

    HEADER: str = (
        "SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS"
    )
    HEADER_OFFSET: int = 5
    table_start = lines.index(HEADER) + HEADER_OFFSET

    rows = []
    for row in lines[table_start:]:
        if not row.strip():
            break
        rows.append(row)

    data = []
    for line in rows:
        (
            transition_from,
            _,
            transition_to,
            energy_ev,
            energy_cm,
            wavelength_nm,
            fosc,
            *_,
        ) = line.split()

        from_state, from_mult = transition_from.rstrip("A").split("-")
        to_state, to_mult = transition_to.rstrip("A").split("-")

        data.append(
            [
                int(from_state),
                float(from_mult),
                int(to_state),
                float(to_mult),
                float(energy_ev),
                float(energy_cm),
                float(wavelength_nm),
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
