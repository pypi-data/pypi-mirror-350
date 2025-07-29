import marimo

__generated_with = "0.13.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    navigation = mo.nav_menu({
        "/orbitals": "Orbitals",
        "/tddft": "TDDFT",
        "/soc_tddft": "SOC-TDDFT",
    })
    navigation
    return


if __name__ == "__main__":
    app.run()
