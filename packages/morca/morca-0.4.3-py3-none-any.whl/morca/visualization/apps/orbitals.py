import marimo

__generated_with = "0.13.10"
app = marimo.App(width="medium")


@app.cell
def _(file_text):
    file_text
    return


@app.cell
def settings(isovalue_radio, mo, orbital_dropdown, orbital_file_dropdown):
    # Display the settings

    mo.hstack([orbital_dropdown, isovalue_radio, orbital_file_dropdown])
    return


@app.cell
def dashboards(
    mo,
    show_active_space,
    show_loewdin_orbital_compositions,
    show_spin_density,
):
    mo.hstack(
        [show_spin_density, show_active_space, show_loewdin_orbital_compositions]
    )
    return


@app.cell
def orbital_display(isovalue, mo, orbital, orbital_file, structure):
    # Display the selected orbital

    with mo.status.spinner(title=f"Creating orbital {orbital}..") as _spinner:
        _density = structure.create_molecular_orbital(orbital_file, orbital)

    mo.vstack(
        [
            mo.md(f"## Molecular orbital {orbital} ({_density.name})").center(),
            structure.create_fig_with_isosurface(_density, isovalue=isovalue),
        ]
    )
    return


@app.cell
def orbital_list(mo, orbitals_df, show_orbitals):
    mo.stop(not show_orbitals.value)

    mo.ui.dataframe(orbitals_df, page_size=20)
    return


@app.cell
def spin_density(mo, orbital_file, show_spin_density, structure):
    # Display spin density

    mo.stop(not show_spin_density.value)

    with mo.status.spinner(
        title="Creating spin density..", subtitle="This might take up to a minute"
    ) as _spinner:
        _density = structure.create_spin_density(orbital_file, grid=80)

    try:
        _fig = structure.create_fig_with_isosurface(
            _density, isovalue=0.5, colors=("#24FF51", "#FA7496")
        )
    except ValueError as e:
        _fig = mo.md(
            f"/// error | Isovalue too extreme, the surface would protrude the grid volume. Is this an open-shell calculation?\n{e}"
        )

    mo.vstack([mo.md(f"## Spin density ({_density.name})").center(), _fig])
    return


@app.cell
def loewdin_compositions(
    OrcaOutput,
    file,
    mo,
    show_loewdin_orbital_compositions,
):
    mo.stop(not show_loewdin_orbital_compositions.value)

    _loewdin_orbital_compositions = OrcaOutput(file).loewdin_orbital_compositions

    mo.ui.dataframe(_loewdin_orbital_compositions, page_size=15)
    return


@app.cell
def active_space_analysis(
    OrcaOutput,
    active_space,
    file,
    isovalue,
    mo,
    orbital_file,
    pl,
    show_active_space,
    structure,
):
    # Display active space orbitals

    mo.stop(not show_active_space.value)

    _output = OrcaOutput(file)
    _active_space = _outout.active_space_orbitals
    _loewdin_orbital_compositions = _output.loewdin_orbital_compositions

    _orbital_dashboards = []
    with mo.status.progress_bar(
        title="Analyzing active space orbitals..", total=len(_active_space)
    ) as _progress_bar:
        for _o in active_space:
            # Create a figure to display the orbital
            _density = structure.create_molecular_orbital(orbital_file, _o)
            _fig = structure.create_fig_with_isosurface(_density, isovalue=isovalue)

            # Get the atomic orbital compositions
            _comp = _loewdin_orbital_compositions.filter(pl.col("Id") == _o).sort(
                by="Weight", descending=True
            )

            # Create the dashboard view
            _dashboard = mo.vstack(
                [_fig, _comp],
                align="center",
            )
            _orbital_dashboards.append(_dashboard)
            _progress_bar.update_progress(f"{_o} done")

    mo.hstack(
        _orbital_dashboards,
        wrap=True,
    )
    return


@app.cell
def _():
    from pathlib import Path

    import cotwo as co
    import marimo as mo
    import polars as pl

    from morca import OrcaOutput
    return OrcaOutput, Path, co, mo, pl


@app.cell
def _(Path, mo):
    # Support giving a file as command-line argument when launching.
    # This could be more robust, but probably works fine for now.

    import sys

    file_arg = Path(sys.argv[-1])
    # if not file_arg.suffix == ".out":
    #     file_arg = None

    file_text = mo.ui.text(
        placeholder="Path to output file",
        value=str(file_arg) if file_arg else "",
        full_width=True,
    )
    return (file_text,)


@app.cell
def _(OrcaOutput, Path, co, file_text, mo):
    mo.stop(not file_text.value)

    file = Path(file_text.value)

    orbital_energies = OrcaOutput(file).orbital_energies
    structure = co.Molecule.from_file(file)
    return file, orbital_energies, structure


@app.cell
def _(orbital_energies, pl):
    # Process the orbital energies dataframe.

    # HOMO as the lowest-energy occupied orbital
    # (change anything for unrestricted calculations?)
    _homo = orbital_energies.filter(pl.col("Occ") != 0).sort(
        by="Energy_Eh", descending=True
    )[0]

    # Global HOMO id
    homo = _homo["Id"].item()

    # Add energies relative to the HOMO
    orbitals_df = orbital_energies.with_columns(
        (pl.col("Energy_Eh") - _homo["Energy_Eh"].item())
        .round(6)
        .alias("Rel_Energy_Eh")
    )

    # Show only the first LUMO_RANGE unoccupied orbitals
    LUMO_RANGE: int = 5
    orbitals_df = orbitals_df.filter(pl.col("Id") <= homo + LUMO_RANGE).sort(
        by="Id", descending=True
    )
    return homo, orbitals_df


@app.cell
def _(file, mo):
    # Create orbital file (.gbw, .qro, etc.) dropdown.

    # Check the file.parent directory for any (known) available orbital files
    _ORBITAL_FILE_SUFFIXES = [".gbw", ".qro", ".unso", ".uno", ".uco"]
    _orbital_files = {
        f.name: f
        for suffix in _ORBITAL_FILE_SUFFIXES
        for f in file.parent.glob(f"*{suffix}")
    }

    # Default to .gbw file
    _default_gbw_file = file.with_suffix(".gbw").name

    orbital_file_dropdown = mo.ui.dropdown(
        label="Orbital file", options=_orbital_files, value=_default_gbw_file
    )
    return (orbital_file_dropdown,)


@app.cell
def _(mo):
    isovalue_radio = mo.ui.radio(
        label="Isovalue",
        value="0.05",
        options={"0.1": 0.1, "0.05": 0.05, "0.025": 0.025, "0.001": 0.001},
        inline=True,
    )
    return (isovalue_radio,)


@app.cell
def _(homo, mo, orbital_energies, orbitals_df):
    # Create orbital dropdown.

    _orbital_dicts = orbitals_df.to_dicts()
    is_unrestricted = True if "Spin" in orbital_energies.columns else False

    # Label orbitals as "92 (2.00, 230 kJ/mol)" or "92b (2.00, 230 kJ/mol)"
    for _o in _orbital_dicts:
        if is_unrestricted:
            _o["Spin"] = "a" if _o["Spin"] == "up" else "b"
        else:
            _o["Spin"] = ""

        _o["Label"] = (
            f"{_o['Id']}{_o['Spin']} ({_o['Occ']:<8.2f}, {_o['Rel_Energy_Eh'] * 2625.5:8.1f} kJ/mol)"
        )

        # Find the HOMO dict
        if _o["Id"] == homo:
            _homo = _o

    orbital_dropdown = mo.ui.dropdown(
        label="Select orbital: ",
        options={o["Label"]: o for o in _orbital_dicts},
        value=_homo["Label"],
    )
    return (orbital_dropdown,)


@app.cell
def _(orbital_dropdown):
    _orbital = orbital_dropdown.value
    orbital = str(_orbital["Id"]) + _orbital["Spin"]
    return (orbital,)


@app.cell
def _(isovalue_radio, orbital_file_dropdown):
    isovalue = isovalue_radio.value
    orbital_file = orbital_file_dropdown.value
    return isovalue, orbital_file


@app.cell
def _(OrcaOutput, file, mo):
    # Define run_buttons

    show_orbitals = mo.ui.run_button(label="Show orbital table")
    show_spin_density = mo.ui.run_button(label="Show spin density")

    try:
        active_space = OrcaOutput(file).active_space_orbitals
        _disable_active_space = False
    except ValueError:
        _disable_active_space = True
    show_active_space = mo.ui.run_button(
        label="Analyze active space", disabled=_disable_active_space
    )

    try:
        loewdin_compositions = OrcaOutput(file).loewdin_orbital_compositions
        _disable_loewdin_comp = False
    except ValueError:
        _disable_loewdin_comp = True
    show_loewdin_orbital_compositions = mo.ui.run_button(
        label="Löwdin population analysis", disabled=_disable_loewdin_comp
    )
    return (
        active_space,
        show_active_space,
        show_loewdin_orbital_compositions,
        show_orbitals,
        show_spin_density,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
