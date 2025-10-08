from __future__ import annotations
from pathlib import Path
import re
from typing import Dict, List, Tuple, Union
from pymavlink import matliv

#python parameter_check_logic.py drone_actual.param
ParamValue = Union[int, float, str]
Pathish = Union[str, Path]

__all__ = [
    "parse_params_file",
    "diff_params",
    "check_file_against_baseline",
    "ParamValue",
]

#Compile once for speed 
_LINE_RE = re.compile(r"^([^,]+)\s*,\s*(.+)$")

def parse_params_file(path: Pathish) -> Dict[str, ParamValue]:
    p = Path(path)
    params: Dict[str, ParamValue] = {}

    with p.open("r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            m = _LINE_RE.match(ln)
            if not m:
                continue
            k, v = m.group(1).strip(), m.group(2).strip()
            try:
                fv = float(v)
                params[k] = int(fv) if fv.is_integer() else fv
            except ValueError:
                params[k] = v
    return params

def diff_params(
    actual: Dict[str, ParamValue],
    expected: Dict[str, ParamValue],
) -> Tuple[List[str], List[Tuple[str, ParamValue, ParamValue]], List[str]]:
    
    missing: List[str] = []
    mismatches: List[Tuple[str, ParamValue, ParamValue]] = []
    extras: List[str] = []

    for k, exp in expected.items():
        if k not in actual:
            missing.append(k)
        elif actual[k] != exp:
            mismatches.append((k, exp, actual[k]))

    for k in actual:
        if k not in expected:
            extras.append(k)

    missing.sort()
    mismatches.sort(key=lambda t: t[0])
    extras.sort()

    return missing, mismatches, extras

def check_file_against_baseline(
    actual_file: Pathish,
    baseline_file: Pathish,
) -> Tuple[List[str], List[Tuple[str, ParamValue, ParamValue]], List[str]]:
    actual = parse_params_file(actual_file)
    expected = parse_params_file(baseline_file)
    return diff_params(actual, expected)

if __name__ == "__main__":
    import sys
    from pathlib import Path

    BASELINE_FILE = Path("parameter_expectations.param")

    if len(sys.argv) != 2:
        print("Usage: python parameter_check_logic.py <actual_file>")
        sys.exit(2)

    actual_path = Path(sys.argv[1])
    baseline_path = BASELINE_FILE

    if not baseline_path.exists():
        print(f"Baseline file not found: {baseline_path}")
        sys.exit(2)
    if not actual_path.exists():
        print(f"Actual file not found: {actual_path}")
        sys.exit(2)

    missing, mismatches, extras = check_file_against_baseline(actual_path, baseline_path)

    if not missing and not mismatches and not extras:
        print("Files match baseline")
        sys.exit(0)
    else:
        print("Differences found:")
        if missing:
            print(f"Missing: {missing}")
        if mismatches:
            print(f"Mismatches: {mismatches}")
        if extras:
            print(f"Extras: {extras}")
        sys.exit(1)
