from pathlib import Path
from typing import Optional

import polars as pl

from morca.core.parsers import (
    parse_absorption_spectrum,
    parse_active_space_orbitals,
    parse_charge,
    parse_energies,
    parse_fspe_eh,
    parse_geometry,
    parse_imaginary_modes,
    parse_ir_spectrum,
    parse_loewdin_orbital_compositions,
    parse_mult,
    parse_n_roots,
    parse_orbital_energies,
    parse_soc_absorption_spectrum,
    parse_soc_states,
    parse_tda,
    parse_tddft_excited_states,
    parse_run_time_h
)
from morca.visualization import create_simulated_spectrum_chart


class OrcaOutput:
    def __init__(self, file):
        self._file = Path(file)
        if not self._file.exists():
            raise FileNotFoundError(f"File '{self._file}' not found!")
        self.directory = self._file.parent

    @property
    def content(self):
        return self._file.read_text()

    @property
    def orbital_energies(self):
        return parse_orbital_energies(self._file)

    @property
    def absorption_spectrum(self):
        return parse_absorption_spectrum(self._file)

    @property
    def active_space_orbitals(self):
        return parse_active_space_orbitals(self._file)

    @property
    def excited_states(self):
        return parse_tddft_excited_states(self._file)

    @property
    def loewdin_orbital_compositions(self):
        return parse_loewdin_orbital_compositions(self._file)

    @property
    def ir_spectrum(self):
        return parse_ir_spectrum(self._file)

    @property
    def geometry(self):
        return parse_geometry(self._file)

    @property
    def energies(self):
        return parse_energies(self._file)

    @property
    def single_point_energy(self):
        print("the 'single_point_energy' method is deprecated - use `fspe_eh`")
        return parse_fspe_eh(self._file)

    @property
    def fspe_eh(self):
        return parse_fspe_eh(self._file)

    @property
    def gibbs_free_energy_eh(self):
        return parse_energies(self._file)["gibbs_free_energy_eh"]

    @property
    def gibbs_free_energy_correction_eh(self):
        return parse_energies(self._file)["gibbs_free_energy_correction_eh"]

    @property
    def enthalpy_eh(self):
        return parse_energies(self._file)["enthalpy_eh"]

    @property
    def entropy_correction_eh(self):
        return parse_energies(self._file)["entropy_correction_eh"]

    @property
    def thermal_correction_eh(self):
        return parse_energies(self._file)["thermal_correction_eh"]

    @property
    def tamm_dancoff(self):
        return parse_tda(self._file)

    @property
    def n_roots(self):
        return parse_n_roots(self._file)

    def get_state_vector(self, state: int, triplet: bool = False) -> int:
        tda = self.tamm_dancoff
        n_roots = self.n_roots
        if triplet:
            state += n_roots
        return state if tda else (2 * state) - 1

    def create_simulated_spectrum_chart(
        self,
        fwhm: float,
        spectrum: Optional[pl.DataFrame] = None,
        intensity_cutoff: float = 0.0,
    ):
        if spectrum is None:
            spectrum = self.absorption_spectrum

        if intensity_cutoff > 0:
            spectrum = spectrum.filter(pl.col("fosc") >= intensity_cutoff)

        return create_simulated_spectrum_chart(spectrum, fwhm)

    @property
    def charge(self):
        return parse_charge(self._file)

    @property
    def mult(self):
        return parse_mult(self._file)

    @property
    def soc_absorption_spectrum(self):
        return parse_soc_absorption_spectrum(self._file)

    @property
    def soc_states(self):
        return parse_soc_states(self._file)

    @property
    def imaginary_modes(self):
        return parse_imaginary_modes(self._file)

    @property
    def run_time_h(self):
        return parse_run_time_h(self._file)
