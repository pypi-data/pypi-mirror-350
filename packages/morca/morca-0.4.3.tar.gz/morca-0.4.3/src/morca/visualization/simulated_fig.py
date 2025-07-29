from typing import Optional

import altair as alt
import numpy as np
import polars as pl
import plotly.graph_objects as go
import plotly

from morca.processing import apply_gaussian_convolution, compute_total_spectrum


def create_simulated_spectrum_fig(
    bar_spectrum: pl.DataFrame,
    fwhm: float,
    energy_column: str = "energy_cm",
    intensity_column: str = "fosc",
    name_column: str = "to_state",
    grid_points: int = 500,
    grid_domain: tuple[float, float] = (0, 60_000),
    intensity_cutoff: float = 0.0,
    intensity_domain: Optional[tuple[float, float]] = None,
) -> go.Figure:
    bar_spectrum = bar_spectrum.filter(
        pl.col(intensity_column) >= intensity_cutoff
    )

    grid = np.linspace(*grid_domain, grid_points)
    _gaussians, _grid = apply_gaussian_convolution(
        bar_spectrum,
        fwhm,
        energy_column,
        intensity_column,
        name_column,
        grid=grid,
    )
    _simulated_spectrum_df = compute_total_spectrum(
        _gaussians, _grid, energy_column, intensity_column
    )

    # Create a Plotly figure
    fig = go.Figure()


    # Add individual Gaussian curves as filled areas
    for i, gaussian_df in enumerate(_gaussians):
        state_name = f"State {i}"

        fig.add_trace(
            go.Scatter(
                x=gaussian_df[energy_column],
                y=gaussian_df[intensity_column],
                mode="lines",
                name=str(state_name),
                fill="tozeroy",
                line=dict(width=0),
            )
        )

    # Add the sum as a line
    fig.add_trace(
        go.Scatter(
            x=_simulated_spectrum_df[energy_column],
            y=_simulated_spectrum_df[intensity_column],
            mode="lines",
            name="Total",
            line=dict(width=2, color="black"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=bar_spectrum[energy_column],
            y=bar_spectrum[intensity_column],
            text=bar_spectrum[name_column],
            mode="markers+text",
            textposition="bottom center",
            name="Vertical Transitions",
            marker=dict(size=6, color="black", symbol="circle"),
        )
    )

    # Configure the layout
    layout = dict(
        xaxis=dict(
            title=energy_column,
            range=grid_domain,
        ),
        yaxis=dict(
            title=intensity_column,
            range=intensity_domain,
        ),
        showlegend=True,
    )

    fig.update_layout(layout)

    return fig
