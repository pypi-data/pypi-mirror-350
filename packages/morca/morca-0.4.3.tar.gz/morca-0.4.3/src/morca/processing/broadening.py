from typing import List, Optional, Tuple

import numpy as np
import polars as pl


def _gaussian(x: np.ndarray, fwhm: float) -> np.ndarray:
    """
    Gaussian function used for spectral broadening.

    Parameters
    ----------
    x : np.ndarray
        Energy/frequency offset relative to center.
    fwhm : float
        Full width at half maximum (FWHM) of the Gaussian.

    Returns
    -------
    np.ndarray
        Gaussian values evaluated at x.
    """
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    if sigma == 0:
        return np.zeros_like(x)
    return np.exp(-(x**2) / (2 * sigma**2))


def apply_gaussian_convolution(
    df: pl.DataFrame,
    fwhm: float,
    energy_column: str = "energy_cm",
    intensity_column: str = "fosc",
    name_column: str = "to_state",
    grid_points: int = 500,
    grid_padding: float = 2.0,
    grid: Optional[np.ndarray] = None,
) -> Tuple[List[pl.DataFrame], np.ndarray]:
    """
    Apply Gaussian convolution to spectral transitions.

    Returns a new, broadened dataframe for each transition in the original and the grid used.

    Parameters
    ----------
    df : pl.DataFrame
        Input dataframe with spectral transitions
    fwhm : float
        Full width at half maximum for Gaussian broadening
    grid_points : int
        Number of points in the energy grid
    energy_column : str
        Column name for energy values
    intensity_column : str
        Column name for intensity values
    name_column : str
        Column name for identifiers
    grid_padding : float
        Padding beyond min/max energies in units of fwhm
    grid : np.ndarray, optional
        Predefined energy grid to use instead of creating one

    Returns
    -------
    Tuple[List[pl.DataFrame], np.ndarray]
        List of dataframes with convolved spectra for each transition,
        Common energy grid used for the convolution
    """
    # Create energy grid if not provided
    if grid is None:
        emin = df.select(pl.col(energy_column)).min().item() - grid_padding * fwhm
        emax = df.select(pl.col(energy_column)).max().item() + grid_padding * fwhm
        grid = np.linspace(emin, emax, grid_points)
    assert grid is not None

    # Process each transition
    convolved_dfs = []
    for row in df.iter_rows(named=True):
        # Calculate Gaussian profile for this transition
        energy0 = row[energy_column]
        intensity = row[intensity_column]

        if intensity < 1e-6:
            continue

        y = intensity * _gaussian(grid - energy0, fwhm)

        # Create dataframe for this transition (only where intensity is significant)
        df_line = pl.DataFrame(
            {
                name_column: [row[name_column]] * grid.size,
                energy_column: grid,
                intensity_column: y,
            }
        ).filter(pl.col(intensity_column) > 0)

        convolved_dfs.append(df_line)

    return convolved_dfs, grid


def compute_total_spectrum(
    convolved_spectra: List[pl.DataFrame],
    grid: np.ndarray,
    energy_column: str = "energy_cm",
    intensity_column: str = "fosc",
) -> pl.DataFrame:
    """
    Compute the overall spectrum by summing individual convolved spectra.

    Parameters
    ----------
    convolved_spectra : List[pl.DataFrame]
        List of dataframes with convolved spectra
    grid : np.ndarray
        Common energy grid used for the convolution
    energy_column : str
        Column name for energy values

    Returns
    -------
    pl.DataFrame
        Dataframe with the total spectrum
    """
    # Initialize array to hold summed intensities
    total_intensity = np.zeros_like(grid)

    # Sum up contributions from each transition
    for df in convolved_spectra:
        # Build a mapping from energy to intensity for this spectrum
        # This handles potential filtering in the individual dataframes
        energy_to_intensity = {
            e: i
            for e, i in zip(
                df.select(energy_column).to_numpy().flatten(),
                df.select(intensity_column).to_numpy().flatten(),
            )
        }

        # Add intensity at each grid point
        for i, e in enumerate(grid):
            if e in energy_to_intensity:
                total_intensity[i] += energy_to_intensity[e]

    # Create and return dataframe with total spectrum
    return pl.DataFrame({energy_column: grid, intensity_column: total_intensity})
