from pathlib import Path
import polars as pl

def parse_orbital_energies(file: str | Path) -> pl.DataFrame:
    """Parse the last ORBTIAL ENERGIES table from an ORCA output file.

    Returns a pl.DataFrame:
        restricted:   ("Id", "Occ", "Energy_Eh", "Energy_eV")
        unrestricted: ("Id", "Occ", "Energy_Eh", "Energy_eV", "Spin")
    """
    TABLE_HEADER_TO_DATA_OFFSET = 4

    lines = Path(file).read_text().splitlines()

    # Find the last occurence of ORBITAL ENERGIES
    all_occurences = [i for i, line in enumerate(lines) if line.strip() == "ORBITAL ENERGIES"]
    if len(all_occurences) == 0:
            raise ValueError("No orbital energies found")
    table_start_index = all_occurences[-1] + TABLE_HEADER_TO_DATA_OFFSET

    # Identify unrestricted calculation
    unrestricted = True if lines[table_start_index - 2].strip() == "SPIN UP ORBITALS" else False

    def parse_table(table_start: int) -> list:
        """Helper function for parsing an orbital energies table."""
        table_rows = []
        for line in lines[table_start:]:
            line = line.strip()
            if not line or line.startswith("*"):
                break

            # Split by whitespace and convert to appropriate types
            values = line.split()
            if len(values) < 4:
                continue  # Skip rows that don't have enough values

            table_rows.append({
                "Id": int(values[0]),
                "Occ": float(values[1]),
                "Energy_Eh": float(values[2]),
                "Energy_eV": float(values[3])
            })
        return table_rows

    if unrestricted:
        spin_up_data = parse_table(table_start_index)
        for row in spin_up_data:
            row["Spin"] = "up"
        spin_down_data = parse_table(table_start_index + len(spin_up_data) + 3)
        for row in spin_down_data:
            row["Spin"] = "down"
        data = spin_up_data + spin_down_data
    else:
        data = parse_table(table_start_index)
    return pl.from_dicts(data)
