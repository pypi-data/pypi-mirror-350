# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "altair==5.5.0",
#     "cotwo==1.1.10",
#     "marimo",
#     "morca==0.3.1",
#     "polars==1.28.1",
# ]
# ///

import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from pathlib import Path

    import polars as pl
    import altair as alt
    import cotwo

    from morca import OrcaOutput
    from morca.visualization import create_simulated_spectrum_chart
    return OrcaOutput, Path, cotwo, create_simulated_spectrum_chart, pl


@app.cell
def _(mo):
    file_text = mo.ui.text(
        label="Path to output file",
        value="/Users/freddy/Documents/Projects/morca/test/singlet_soc_tddft/singlet_soc_tddft.out",
        full_width=True,
    )
    file_text
    return (file_text,)


@app.cell
def _(Path, file_text, mo):
    file = Path(file_text.value)

    if not file.exists():
        mo.md("File not found!")
    return (file,)


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
def _(OrcaOutput, file_text, mo):
    data = None

    try:
        data = OrcaOutput(file_text.value)
    except FileNotFoundError as e:
        print(e)

    mo.stop(data is None)
    return (data,)


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
def _(mo):
    y_scale = mo.ui.slider(
        start=0, stop=2, step=0.001, value=1, label="Y axis scale", debounce=True, full_width=True
    )
    y_scale
    return (y_scale,)


@app.cell
def _(
    create_simulated_spectrum_chart,
    data,
    energy_unit_radio,
    fwhm_number,
    mo,
    y_scale,
):
    _unit = energy_unit_radio.value

    _units = {
        "energy_cm": dict(energy_column="energy_cm", grid_domain=[0, 60_000]),
        "wavelength_nm": dict(
            energy_column="wavelength_nm", grid_domain=[200, 600]
        ),
    }

    _chart = create_simulated_spectrum_chart(
        data.soc_absorption_spectrum,
        fwhm=fwhm_number.value,
        intensity_cutoff=0.001,
        intensity_domain=[0, y_scale.value],
        **_units[_unit],
    )

    c = mo.ui.altair_chart(_chart)
    c
    return (c,)


@app.cell
def _(c, cotwo, data, file_text):
    selected_soc_state = c.apply_selection(data.soc_absorption_spectrum)
    tda = data.tamm_dancoff
    n_roots = data.n_roots
    structure = cotwo.Molecule.from_file(file_text.value)
    return selected_soc_state, structure


@app.cell
def _(data, mo, pl, selected_soc_state):
    mo.stop(len(selected_soc_state) > 1)

    _soc_state_id = selected_soc_state["to_state"].item()
    _soc_state_contributions = data.soc_states.filter(
        pl.col("state_id") == _soc_state_id
    )

    selected_soc_state_contributions = mo.ui.table(
        _soc_state_contributions, selection="single"
    )
    selected_soc_state_contributions
    return (selected_soc_state_contributions,)


@app.cell
def _(data, file, mo, selected_soc_state_contributions, structure):
    mo.stop(selected_soc_state_contributions.value.is_empty())

    _contrib = selected_soc_state_contributions.value

    root = _contrib["root"].item()
    mult = (2 * _contrib["spin"].item()) + 1

    gbw_file = file.with_suffix(".gbw")

    with mo.status.spinner(title="Rendering difference density..") as _spinner:
        _state_vec = data.get_state_vector(
            root, triplet=True if mult == 3 else False
        )
        _diffdens = structure.create_difference_density(
            gbw_file, state_vector=_state_vec
        )
        _fig = structure.create_fig_with_isosurface(
            _diffdens, isovalue=0.001, colors=("#CCBE00", "#CC0022")
        )

    mo.md(
        f"State {root} (Ms = {mult}) (State Vector: {_state_vec})\n{mo.hstack([mo.ui.plotly(_fig)])}"
    )
    return


@app.cell
def _():
    # mo.stop(root.value.is_empty())

    # with mo.status.spinner(title="Rendering molecular orbitals..") as _spinner:
    #     _from_orb = root.value["from_orb"].item()
    #     _to_orb = root.value["to_orb"].item()

    #     _donor = structure.create_molecular_orbital(gbw_file, _from_orb)
    #     _acceptor = structure.create_molecular_orbital(gbw_file, _to_orb)

    #     _donor_fig = mo.ui.plotly(
    #         structure.create_fig_with_isosurface(_donor, isovalue=0.05)
    #     )
    #     _acceptor_fig = mo.ui.plotly(
    #         structure.create_fig_with_isosurface(_acceptor, isovalue=0.05)
    #     )

    # mo.hstack(
    #     [
    #         mo.md(f"Donor Orbital ({_from_orb}) {_donor_fig}"),
    #         mo.md(f"Acceptor Orbital ({_to_orb}) {_acceptor_fig}"),
    #     ]
    # )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
