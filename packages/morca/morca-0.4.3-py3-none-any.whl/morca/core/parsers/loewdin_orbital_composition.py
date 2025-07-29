from pathlib import Path

import polars as pl

# ----------------------------
# LOEWDIN ORBITAL-COMPOSITIONS
# ----------------------------

#                       0         1         2         3         4         5
#                  -261.55378 -32.13544 -27.61592 -27.61575 -27.60717 -15.84360
#                    2.00000   2.00000   2.00000   2.00000   2.00000   2.00000
#                   --------  --------  --------  --------  --------  --------
#  0 Fe s             100.0      99.9       0.0       0.0       0.0       0.0
#  0 Fe pz              0.0       0.0      82.4      17.4       0.3       0.0
#  0 Fe px              0.0       0.0      16.3      80.9       2.8       0.0
#  0 Fe py              0.0       0.0       1.3       1.8      96.9       0.0
#  2 N  dxz             0.0       0.0       0.0       0.0       0.0       0.2
#  3 N  s               0.0       0.0       0.0       0.0       0.0      99.0
#  4 N  dxz             0.0       0.0       0.0       0.0       0.0       0.2

#                      6         7         8         9        10        11
#                 -15.73786 -15.72994 -15.72962 -15.72937 -15.72788 -15.69238
#                   2.00000   2.00000   2.00000   2.00000   2.00000   2.00000
#                  --------  --------  --------  --------  --------  --------
# 0 Fe dz2             0.0       0.1       0.0       0.0       0.0       0.0
# 1 N  s               0.0      99.8       0.0       0.0       0.0       0.0
# 3 N  dxz             0.0       0.0       0.0       0.0       0.0       0.2
# 4 N  s               0.0       0.0       0.0       0.0       0.0      99.4
# 5 N  s               0.0       0.0      99.5       0.0       0.0       0.0
# 6 N  s               0.0       0.0       0.0       0.0      99.5       0.0
# 7 N  s              99.6       0.0       0.0       0.0       0.0       0.0
# 8 N  s               0.0       0.0       0.0      99.5       0.0       0.0


def parse_loewdin_orbital_compositions(
    file: str | Path, threshold: float = 1.0
) -> pl.DataFrame:
    """Parse the Löwdin orbital compositions.

    Threshold (%) determines cutoff for inclusion by orbital weight.
    """
    # go through lines and collect composition tables
    #   stop if after empty line (which separates the tables) the next line can't be mapped into integers
    lines = Path(file).read_text().splitlines()

    loewdin_orbital_composition_start = lines.index("LOEWDIN ORBITAL-COMPOSITIONS") + 3
    tables = []
    _table = []
    for i, line in enumerate(lines[loewdin_orbital_composition_start:]):
        idx = loewdin_orbital_composition_start + i
        if not line.strip():
            tables.append(_table)
            _table = []

            # Check for end of loewdin orbital compositions:
            try:
                list(map(int, lines[idx + 1].split()))
                continue
            except ValueError:
                # no more compositions
                break
        _table.append(line.split())

    # a '_table':
    # [['744', '745', '746'],
    # ['33.87159', '33.94614', '34.56336'],
    #  ['0.00000', '0.00000', '0.00000'],
    #  ['--------', '--------', '--------'],
    #  ['1', 'N', 's', '3.5', '0.0', '0.2'],
    #  ['2', 'N', 's', '13.7', '2.3', '1.3'],
    #  ['3', 'N', 's', '0.9', '0.2', '96.6'],
    #  ['3', 'N', 'dxz', '0.0', '0.0', '0.1'],
    #  ['4', 'N', 's', '0.8', '0.0', '0.1'],
    #  ['5', 'N', 's', '19.8', '33.7', '1.3'],
    #  ['6', 'N', 's', '25.5', '16.7', '0.0'],
    #  ['7', 'N', 's', '18.1', '22.4', '0.0'],
    #  ['8', 'N', 's', '17.0', '24.2', '0.0']]

    orbitals = []
    for table in tables:
        ids, energies_eh, occs, _, *compositions = table
        for i, id in enumerate(ids):
            orbital = {
                "Id": int(id),
                "Energy_Eh": float(energies_eh[i]),
                "Occ": float(occs[i]),
                "Composition": [
                    {
                        "Atom_id": int(c[0]),
                        "Symbol": c[1],
                        "Orbital_type": c[2],
                        "Weight": float(c[i + 3]),
                    }
                    for c in compositions
                ],
            }
            orbitals.append(orbital)
    df = pl.DataFrame(orbitals)
    flat_df = (
        df.explode(
            "Composition"
        ).unnest(  # turn each list of structs into separate rows
            "Composition"
        )  # extract fields from each struct into separate columns
    )
    flat_df = flat_df.filter(pl.col("Weight") >= threshold)

    return flat_df
