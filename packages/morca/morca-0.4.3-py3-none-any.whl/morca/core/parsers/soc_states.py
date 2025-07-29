from pathlib import Path

import polars as pl

# The threshold for printing is 1.0e-02
# Eigenvectors of the SOC matrix:

#              E(cm-1)  Weight      Real         Imag     : Root  Spin  Ms
#  STATE  0:      0.00
#                       0.99834     -0.99306     -0.11035 : 0     0     0
#  STATE  1:  20564.92
#                       0.01013     -0.02533      0.09743 : 3     1     0
#                       0.48336      0.34877     -0.60143 : 1     1    -1
#                       0.48336      0.01163      0.69515 : 1     1     1
#  STATE  2:  20585.13
#                       0.29648     -0.46547     -0.28252 : 1     1     0
#                       0.34450      0.41247     -0.41757 : 1     1    -1
#                       0.34450      0.18005     -0.55864 : 1     1     1
#  STATE  3:  20586.50
#                       0.68690      0.06752      0.82604 : 1     1     0
#                       0.15006      0.37272      0.10552 : 1     1    -1
#                       0.15006      0.35064     -0.16464 : 1     1     1
#  ...
#
#  STATE254:  46317.28
#                     0.99977     -0.93371     -0.35770 : 62     0     0
#  STATE255:  46582.07
#                     0.99973      0.98344      0.18050 : 63     0     0
#  STATE256:  46728.22
#                     0.99975      0.92721      0.37420 : 64     0     0

# -----------------------------
# TD-DFT/TDA-EXCITATION SPECTRA


def parse_soc_states(file: str | Path) -> pl.DataFrame:
    lines = Path(file).read_text().splitlines()
    lines = [line.strip() for line in lines]

    HEADER: str = "Eigenvectors of the SOC matrix:"
    HEADER_OFFSET: int = 3
    table_start = lines.index(HEADER)
    table_start += HEADER_OFFSET

    states = []
    this_state = []
    for i, line in enumerate(lines[table_start:]):
        if not line.strip():
            states.append(this_state)
            break
        if line.strip().startswith("STATE"):
            if this_state:
                states.append(this_state)
            this_state = []
        this_state.append(line)

    data = []
    for state in states:
        state_id, energy_cm = state[0].strip("STATE").replace(":", "").split()
        state_id = int(state_id)
        energy_cm = float(energy_cm)
        contributions = []
        for contrib in state[1:]:
            weight, _, _, _, root, spin, ms = contrib.strip().split()
            contributions.append(
                {
                    "weight": float(weight),
                    "root": int(root),
                    "spin": float(spin),
                    "m_s": int(ms),
                }
            )
        data.append([state_id, energy_cm, contributions])

    df = pl.DataFrame(
        data,
        schema=["state_id", "energy_cm", "contributions"],
        orient="row",
    )
    df = df.explode("contributions").unnest("contributions")
    return df
