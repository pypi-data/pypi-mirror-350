import marimo

__generated_with = "0.13.10"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    from pathlib import Path
    import sys
    from typing import Optional

    import polars as pl
    import plotly.graph_objects as go

    from cotwo import Molecule
    from morca import OrcaOutput
    from morca.visualization.simulated_fig import create_simulated_spectrum_fig
    return (
        Molecule,
        OrcaOutput,
        Path,
        create_simulated_spectrum_fig,
        mo,
        pl,
        sys,
    )


@app.cell
def _(Path, mo, sys):
    # Output file input

    # Check for command line argument
    _arg = sys.argv[-1]
    if _arg.endswith(".out"):
        _default = Path(_arg)
    else:
        _default = ""

    # Create a text input for the ORCA output file
    output_file_input = mo.ui.text(
        label="ORCA output file input",
        value=_default,
        placeholder="Enter the path to the output file",
        full_width=True,
    ).form()
    output_file_input
    return (output_file_input,)


@app.cell
def _(Molecule, OrcaOutput, Path, mo, output_file_input):
    # Validate ORCA output file path
    mo.stop(
        not output_file_input.value, "Please provide a valid ORCA output file path."
    )
    output_file = Path(output_file_input.value)
    if not output_file.exists():
        mo.stop(True, f"The file '{output_file}' does not exist.")

    # Define global variables
    data = OrcaOutput(output_file)
    mol = Molecule.from_file(output_file)
    return data, mol, output_file


@app.cell
def _(energy_unit_radio, mo):
    _unit = energy_unit_radio.value

    _units = {
        "energy_cm": dict(
            label=f"FWHM (1/cm)",
            start=1,
            stop=5000,
            value=2000,
            step=10,
        ),
        "wavelength_nm": dict(
            label=f"FWHM (nm)",
            start=1,
            stop=100,
            value=20,
            step=1,
        ),
    }

    fwhm_number = mo.ui.slider(
        **_units[_unit],
        show_value=True,
        debounce=True,
        full_width=True,
    )
    fwhm_number
    return (fwhm_number,)


@app.cell
def _(mo):
    energy_unit_radio = mo.ui.radio(
        options={
            "Wavenumber (1/cm)": "energy_cm",
            "Wavelength (nm)": "wavelength_nm",
        },
        value="Wavenumber (1/cm)",
        label="Energy unit",
    )
    energy_unit_radio
    return (energy_unit_radio,)


@app.cell
def _(create_simulated_spectrum_fig, data, energy_unit_radio, fwhm_number, mo):
    _unit = energy_unit_radio.value

    _units = {
        "energy_cm": dict(energy_column="energy_cm", grid_domain=[0, 60_000]),
        "wavelength_nm": dict(
            energy_column="wavelength_nm", grid_domain=[200, 800]
        ),
    }

    _fig = create_simulated_spectrum_fig(
        data.absorption_spectrum,
        fwhm=fwhm_number.value,
        **_units[_unit],
    )
    fig = mo.ui.plotly(_fig)
    fig
    return (fig,)


@app.cell
def _(data, fig, mo, pl):
    idx = [i + 1 for i in fig.indices]
    if idx:
        _df = data.absorption_spectrum.filter(pl.col("to_state").is_in(idx))
    else:
        _df = data.absorption_spectrum

    _df = _df.drop(["from_state", "from_mult"])
    selected_states = mo.ui.table(
        _df,
        selection="single",
        format_mapping={
            "wavelength_nm": "{:.0f}",
            "energy_cm": "{:.0f}",
            "energy_ev": "{:.2f}",
            "fosc": "{:.3f}",
        },
    )
    selected_states
    return (selected_states,)


@app.cell
def _(mo):
    # Isovalue radio
    iso = mo.ui.radio(
        label="Isovalue",
        value="0.0025",
        options={
            "0.1000": 0.1,
            "0.0500": 0.05,
            "0.0250": 0.025,
            "0.0025": 0.0025,
            "0.0010": 0.001,
        },
    )
    iso
    return (iso,)


@app.cell
def _(data, iso, mo, mol, output_file, selected_states):
    gbw_file = output_file.with_suffix(".gbw")


    if selected_states.value.is_empty():
        state = None
    else:
        state = selected_states.value["to_state"].item()

    if state:
        with mo.status.spinner(title="Rendering difference density..") as _spinner:
            _dd = mol.create_difference_density(
                gbw_file, data.get_state_vector(state)
            )
        _fig = mol.create_fig_with_isosurface(
            _dd, isovalue=iso.value, colors=("#CCBE00", "#CC0022")
        )
    else:
        _fig = mol.create_fig()
    _fig
    return gbw_file, state


@app.cell
def _(data, mo, pl, state):
    mo.stop(state is None)

    root_df = mo.ui.table(
        data.excited_states.filter(pl.col("state_id") == state)
        .select(
            pl.col("from_orb"),
            pl.col("to_orb"),
            pl.col("weight").round(2),
        )
        .sort(by="weight", descending=True),
        selection="single",
    )
    root_df
    return (root_df,)


@app.cell
def _(gbw_file, mo, mol, root_df):
    mo.stop(root_df.value.is_empty())

    orbs = (root_df.value["from_orb"].item(), root_df.value["to_orb"].item())
    with mo.status.spinner(title="Rendering molecular orbitals..") as _spinner:
        from_orb = mol.create_molecular_orbital(gbw_file, orbs[0])
        to_orb = mol.create_molecular_orbital(gbw_file, orbs[1])
    _fig_from = mol.create_fig_with_isosurface(from_orb, isovalue=0.05)
    _fig_to = mol.create_fig_with_isosurface(to_orb, isovalue=0.05)
    mo.hstack([_fig_from, _fig_to])
    return


if __name__ == "__main__":
    app.run()
