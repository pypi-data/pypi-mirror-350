from pathlib import Path

import polars as pl

from morca.core.parsers.utilities import HeaderOption, find_table_start

# ---------------------
# TD-DFT EXCITED STATES
# ---------------------

# the weight of the individual excitations are printed if larger than 1.0e-02

# UHF/UKS reference: multiplicity estimated based on rounded <S**2> value, RELEVANCE IS LIMITED!

# STATE  1:  E=   0.030330 au      0.825 eV     6656.7 cm**-1 <S**2> =   0.865312 Mult 2
#     83b ->  89b  :     0.050639
#     84b ->  89b  :     0.010861
#     86b ->  89b  :     0.415638
#     88b ->  89b  :     0.464258
#     88b ->  91b  :     0.036756

# STATE  2:  E=   0.031298 au      0.852 eV     6869.1 cm**-1 <S**2> =   0.842042 Mult 2
#     86b ->  89b  :     0.496552
#     86b ->  91b  :     0.010894
#     88b ->  89b  :     0.453114
#     88b ->  91b  :     0.012071

# STATE  3:  E=   0.052196 au      1.420 eV    11455.7 cm**-1 <S**2> =   3.051133 Mult 4
#     84a ->  90a  :     0.034181
#     88a ->  90a  :     0.343157


def parse_tddft_excited_states(file: str | Path) -> pl.DataFrame:
    lines = Path(file).read_text().splitlines()
    lines = [line.strip() for line in lines]

    HEADER_OPTIONS = [
        HeaderOption("TD-DFT EXCITED STATES", 7),
        HeaderOption("TD-DFT/TDA EXCITED STATES", 7),
        HeaderOption("TD-DFT/TDA EXCITED STATES (SINGLETS)", 5),
    ]

    table_start = find_table_start(lines, HEADER_OPTIONS)
    states = []
    this_state = []
    for i, line in enumerate(lines[table_start:]):
        if not line.strip():
            states.append(this_state)
            if lines[table_start + i + 1].startswith("STATE"):
                this_state = []
                continue
            break
        this_state.append(line)

    def is_number(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    data = []
    for state in states:
        header = state[0].replace(":", "")
        numbers = [float(token) for token in header.split() if is_number(token)]
        state_id, e_eh, e_ev, e_cm, s2, mult = numbers
        composition = []
        for line in state[1:]:
            try:
                from_orb, _, to_orb, _, weight = line.split()
            except ValueError:
                # TDDFT/TDA also prints some 'c' values
                from_orb, _, to_orb, _, weight, *_ = line.split()
            composition.append(
                {"from_orb": from_orb, "to_orb": to_orb, "weight": float(weight)}
            )
        data.append([state_id, mult, composition, e_eh, e_ev, e_cm, s2])

    df = pl.DataFrame(
        data,
        schema=["state_id", "mult", "composition", "e_eh", "e_ev", "e_cm", "s2"],
        orient="row",
    )
    df = df.explode("composition").unnest("composition")
    return df
