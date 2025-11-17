"""This following code ensures assertion of expected parameters with Mavlink data.
It reads a baseline file of expected Pixhawk parameters and compares them
against values retrieved over MAVLink.
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple, Union

# Default connection settings used if environment variables are not set.
DEFAULT_PIXHAWK_ADDRESS = "/dev/ttyAMA0"
DEFAULT_PIXHAWK_BAUD = 57600

ParamValue = Union[int, float, str]
Pathish = Union[str, Path]

# parses expectations file by spliting each expected parameter into parameter
# name (before comma) and value
_LINE_RE = re.compile(r"^([^,]+)\s*,\s*(.+)$")


def _coerce_value(value_str: str) -> ParamValue:
    """
    This function allows for value interpretation as a number.

    It tries to convert a string into a float, and if that float is an integer
    value, it converts it to an int. Otherwise, it leaves the string as-is.
    """
    try:
        float_value = float(value_str)
        return int(float_value) if float_value.is_integer() else float_value
    except ValueError:
        return value_str


def parse_params_file(path: Pathish) -> Dict[str, ParamValue]:
    """
    reads param_expectations line by line and builds a dictionary

    Each non-empty, non-comment line is expected to look like:
        PARAM_NAME, VALUE   # optional inline comment

    Returns:
        dict mapping parameter name -> coerced value.
    """
    param_path = Path(path)
    params: Dict[str, ParamValue] = {}

    with param_path.open("r", encoding="utf-8", errors="replace") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            match = _LINE_RE.match(line)
            if not match:
                continue

            key, raw_value = match.group(1).strip(), match.group(2).strip()

            # allow inline comments after value
            if "#" in raw_value:
                raw_value = raw_value.split("#", 1)[0].strip()

            params[key] = _coerce_value(raw_value)

    return params


def _float_equal(a: float, b: float, eps: float = 1e-6) -> bool:
    """Helper that checks if two floats are equal within a small epsilon."""
    return abs(a - b) <= eps


def _values_equal(a: ParamValue, b: ParamValue) -> bool:
    """
    Ensures values are approprialtley cmpared via rounding / tolerance.

    If both values are numeric, they are compared using a float tolerance.
    Otherwise, a normal equality comparison is used.
    """
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return _float_equal(float(a), float(b))
    return a == b


def diff_params(
    actual: Dict[str, ParamValue],
    expected: Dict[str, ParamValue],
) -> Tuple[List[str], List[Tuple[str, ParamValue, ParamValue]], List[str]]:
    """
    Takes actual and expected values as parameters to build three lists of
    missing, mismatched and extras.

    Returns:
        missing:    parameters that are in expected but not found in actual.
        mismatches: (name, expected_value, actual_value) for value differences.
        extras:     parameters that are found on dron but not in file.
    """
    missing: List[str] = []
    mismatches: List[Tuple[str, ParamValue, ParamValue]] = []
    extras: List[str] = []

    # builds missing and mismatches lists in case
    for name, expected_value in expected.items():
        if name not in actual:
            missing.append(name)
        elif not _values_equal(actual[name], expected_value):
            mismatches.append((name, expected_value, actual[name]))

    # checks for parameters that are fouund on dron but not in file
    for name in actual:
        if name not in expected:
            extras.append(name)

    missing.sort()
    mismatches.sort(key=lambda item: item[0])
    extras.sort()

    return missing, mismatches, extras


def fetch_all_params_mavlink(
    address: str,
    baud: int = DEFAULT_PIXHAWK_BAUD,
    timeout_s: int = 25,
) -> Dict[str, ParamValue]:
    """
    Opens MAVLink connection directly and builds a dictionary by listening in
    for PARAM_VALUE messages.

    It:
    - checks if vehicle is alive using a heartbeat
    - requests params
    - decrypts and strips messages into values
    """
    # imported here so other modules can import this file without pymavlink
    from pymavlink import mavutil   # pylint: disable=import-outside-toplevel

    # checks if vehicle is alive
    connection = mavutil.mavlink_connection(address, baud=baud)
    heartbeat = connection.wait_heartbeat(timeout=timeout_s)
    if not heartbeat:
        raise RuntimeError("Drone is not operating")

    # requests params
    connection.mav.param_request_list_send(
        connection.target_system,
        connection.target_component,
    )

    params: Dict[str, ParamValue] = {}
    seen_names: set[str] = set()
    total_count: int | None = None
    end_time = time.time() + timeout_s

    try:
        while time.time() < end_time:
            msg = connection.recv_match(
                type="PARAM_VALUE",
                blocking=True,
                timeout=2.0,
            )
            if not msg:
                continue

            # decrypt and strip message into values
            raw_id = msg.param_id
            if isinstance(raw_id, bytes):
                name = raw_id.decode("ascii", errors="ignore").strip("\x00")
            else:
                name = str(raw_id).strip("\x00")

            params[name] = float(msg.param_value)
            seen_names.add(name)  # keeps track of how many parameters collected

            try:
                total_count = int(msg.param_count)
            except (TypeError, ValueError):
                total_count = None

            # break early if all have been collected
            if total_count and len(seen_names) >= total_count:
                break
    finally:
        # best-effort close, failure here is non-fatal
        try:
            connection.close()
        except Exception:  # pylint: disable=broad-except
            pass

    return params


def main() -> int:
    """
    Main function which calls all others and compares expected parameters to
    actual parameters.
    """
    address = os.environ.get("PIXHAWK_ADDRESS", DEFAULT_PIXHAWK_ADDRESS)
    baud_str = os.environ.get("PIXHAWK_BAUD", str(DEFAULT_PIXHAWK_BAUD))
    baud = int(baud_str)

    baseline = Path(__file__).with_name("parameter_expectations.param")

    if not baseline.exists():
        print(f"Baseline not found: {baseline}")
        return 2  # checks for expectations file

    try:
        actual = fetch_all_params_mavlink(address, baud=baud, timeout_s=25)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        # attempts to connect to mavlink and returns 2 if failiyre
        print(f"Failed to fetch params via MAVLink: {exc}")
        return 2

    expected = parse_params_file(baseline)
    missing, mismatches, extras = diff_params(actual, expected)

    if not missing and not mismatches and not extras:
        print("All Pixhawk parameters match baseline.")
        return 0  # success

    # prints exactly which parameters were not found or are not right
    print("Differences found:")
    if missing:
        print(f"- Missing ({len(missing)}): {missing}")
    if mismatches:
        lines = [
            f"{name}: expected={exp} actual={act}"
            for name, exp, act in mismatches
        ]
        print(f"- Mismatches ({len(mismatches)}):")
        print("  " + "\n  ".join(lines))
    if extras:
        print(f"- Extras ({len(extras)}): {extras}")

    return 1  # returns 1 if differences are found


if __name__ == "__main__":
    sys.exit(main())
