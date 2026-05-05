import time
from typing import List, Tuple

_MARKS: List[Tuple[str, float]] = []


def mark(label: str):
    _MARKS.append((label, time.perf_counter()))


def report() -> str:
    if not _MARKS:
        return "Startup timing report\n(no marks)"

    lines = ["Startup timing report"]
    start_ts = _MARKS[0][1]
    prev_ts = start_ts

    for label, ts in _MARKS:
        delta_ms = (ts - prev_ts) * 1000
        total_ms = (ts - start_ts) * 1000
        lines.append(f"- {label}: +{delta_ms:.2f} ms (total {total_ms:.2f} ms)")
        prev_ts = ts

    return "\n".join(lines)
