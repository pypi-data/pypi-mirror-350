from pathlib import Path

# Determined orbital ranges:
#    Internal       0 -   78 (  79 orbitals)
#    Active        79 -   85 (   7 orbitals)
#    External      86 -  746 ( 661 orbitals)

def parse_active_space_orbitals(file: str | Path) -> list[int]:
    """Parse the active space orbital ids from an ORCA output file."""
    lines = Path(file).read_text().splitlines()
    try:
        orbital_range_index = lines.index("Determined orbital ranges:")
    except ValueError:
        raise ValueError("Failed to parse orbital ranges")
    _, _start, _, _stop, *_ = lines[orbital_range_index + 2].split()
    return list(range(int(_start), int(_stop) + 1))
