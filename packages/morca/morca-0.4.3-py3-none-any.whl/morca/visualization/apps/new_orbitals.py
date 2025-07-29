import marimo

__generated_with = "0.13.10"
app = marimo.App(width="medium")


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
    return Molecule, Optional, OrcaOutput, Path, go, mo, pl, sys


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
def _(mo, output_file):
    # Dropdown with available .cube files
    _cube_files = dict(
        sorted(
            {f.name: f.resolve() for f in output_file.parent.glob("*.cube")}.items()
        )
    )
    cube_file_dropdown = mo.ui.dropdown(options=_cube_files)
    cube_file_dropdown
    return (cube_file_dropdown,)


@app.cell
def _(mo):
    # Isovalue radio
    iso = mo.ui.radio(
        label="Isovalue",
        value="0.050",
        options={"0.100": 0.1, "0.050": 0.05, "0.025": 0.025, "0.001": 0.001},
    )
    iso
    return (iso,)


@app.cell
def _(data, mo, pl):
    _orbitals = data.orbital_energies

    # For unrestricted calculations,
    # show two tables with alpha/beta
    # and also two plots.
    # Start the table around the HOMO/LUMO

    _homo = (
        _orbitals.filter(pl.col("Occ") > 0)
        .sort(by="Energy_Eh", descending=True)
        .drop(["Energy_Eh", "Energy_eV"])
    )
    mo.ui.table(_homo)
    return


@app.cell
def _(Molecule, Optional, Path, go, iso):
    def plot_with_isosurface(
        _mol: Molecule,
        _cube: Path,
        _iso: float = iso.value,
        _colors: Optional[tuple[str, str]] = None,
    ) -> go.Figure:
        if _colors:
            fig = _mol.create_fig_with_isosurface(
                _cube, isovalue=_iso, colors=_colors
            )
        else:
            fig = _mol.create_fig_with_isosurface(_cube, isovalue=_iso)
        return fig
    return (plot_with_isosurface,)


@app.cell
def _(cube_file_dropdown, mol, plot_with_isosurface):
    plot_with_isosurface(mol, cube_file_dropdown.value)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
