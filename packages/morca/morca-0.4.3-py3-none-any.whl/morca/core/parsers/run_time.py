from pathlib import Path


def parse_run_time_h(file: Path | str) -> float:
    line = Path(file).read_text().splitlines()[-1]

    if not line.startswith("TOTAL RUN TIME"):
        raise ValueError(f"Total run time not found in ({line})")

    # TOTAL RUN TIME: 0 days 1 hours 51 minutes 13 seconds 739 msec
    _, _, _, days, _, hours, _, minutes, _, seconds, _, msec, _ = line.split()
    total_run_time_hours = int(days)*24 + int(hours) + int(minutes)/60 + int(seconds)/3600
    return round(total_run_time_hours, 2)
