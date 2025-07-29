from collections import namedtuple
from enum import Enum
from pathlib import Path

Energy = namedtuple("Energy", ["name", "keyword", "token_id"])


class Energies(Enum):
    FSPE = Energy("single_point_energy_eh", "FINAL SINGLE POINT ENERGY", -1)
    ZPE = Energy("zero_point_energy_eh", "Zero point energy", -4)
    THERMAL_CORRECTION = Energy("thermal_correction_eh", "Total thermal correction", -4)
    ENTHALPY = Energy("enthalpy_eh", "Total Enthalpy", -2)
    ENTROPY_CORRECTION = Energy("entropy_correction_eh", "Total entropy correction", -4)
    GIBBS_FREE_ENERGY = Energy("gibbs_free_energy_eh", "Final Gibbs free energy", -2)
    GIBBS_FREE_ENERGY_CORRECTION = Energy(
        "gibbs_free_energy_correction_eh", "G-E(el)", -4
    )


def _parse_keyword(file: str | Path, value: Energy) -> float:
    lines = Path(file).read_text().splitlines()

    for line in reversed(lines):
        if value.keyword in line:
            return float(line.split()[value.token_id])
    raise ValueError(f"'{value.keyword}' not found.")


def parse_fspe_eh(file: str | Path) -> float:
    return _parse_keyword(file, Energies.FSPE.value)


def parse_energies(file: str | Path) -> dict:
    return {ev.name: _parse_keyword(file, ev) for ev in [e.value for e in Energies]}
