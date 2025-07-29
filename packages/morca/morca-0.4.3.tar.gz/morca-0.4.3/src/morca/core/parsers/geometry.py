from pathlib import Path


def parse_geometry(file: str | Path) -> str:
    lines = Path(file).read_text().splitlines()

    HEADER: str = "CARTESIAN COORDINATES (ANGSTROEM)"
    HEADER_OFFSET: int = 2

    coordinate_table_indicies = []
    for i, line in enumerate(lines):
        if HEADER in line:
            coordinate_table_indicies.append(i)

    table_start = coordinate_table_indicies[-1] + HEADER_OFFSET

    rows = []
    for row in lines[table_start:]:
        if not row.strip():
            break
        rows.append(row)

    atoms = []
    for line in rows:
        symbol, x, y, z = line.split()

        if symbol == "XX":
            symbol = "X"

        atoms.append(
            [
                str(symbol),
                float(x),
                float(y),
                float(z),
            ]
        )

    xyz_str = f"{len(atoms)}\n\n"
    xyz_str += "\n".join(
        (f"{a[0]:4} {a[1]:>8.4f} {a[2]:>8.4f} {a[3]:>8.4f}" for a in atoms)
    )
    return xyz_str
