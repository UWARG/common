"""
Test if the Rpi is not recieving enough voltage
"""

from datetime import datetime
import pathlib
import subprocess
import time


DELAY_TIME = 1.0  # seconds
TIMEOUT = 3.0  # seconds
LOG_FILE_PATH = pathlib.Path("logs", f"undervoltage_{time.time_ns()}.log")
DATETIME_FMT = "%Y-%m-%d_%H-%M-%S"


def get_voltage_status() -> None:
    """
    Get voltage status of the Rpi

    `vcgencmd get_throttled` should be in the format `throttled=0x1`
    https://forums.raspberrypi.com/viewtopic.php?p=1570562&sid=e34c4c7122b8e7d232fb0673415135a3
    """
    try:
        result = subprocess.run(
            ["vcgencmd", "get_throttled"],
            capture_output=True,
            check=True,
            encoding="utf-8",
            timeout=TIMEOUT,
        )
        if result.stdout:
            bitmap = int(result.stdout.split("=")[1], base=0)
            if bitmap & (1 << 0) != 0:
                print("currently undervolted")
                with open(LOG_FILE_PATH, "w", encoding="utf-8") as log_file:
                    log_file.write(
                        f"{datetime.now().strftime(DATETIME_FMT)}  -  currently undervolted"
                    )
            if bitmap & (1 << 1) != 0:
                print("ARM frequency currently capped")
                with open(LOG_FILE_PATH, "w", encoding="utf-8") as log_file:
                    log_file.write(
                        f"{datetime.now().strftime(DATETIME_FMT)}  -  ARM frequency currently capped"
                    )
            if bitmap & (1 << 2) != 0:
                print("currently throttled")
                with open(LOG_FILE_PATH, "w", encoding="utf-8") as log_file:
                    log_file.write(
                        f"{datetime.now().strftime(DATETIME_FMT)}  -  currently throttled"
                    )
            if bitmap & (1 << 3) != 0:
                print("soft temperature limit reached")
                with open(LOG_FILE_PATH, "w", encoding="utf-8") as log_file:
                    log_file.write(
                        f"{datetime.now().strftime(DATETIME_FMT)}  -  soft temperature limit reached"
                    )
            if bitmap & (1 << 16) != 0:
                print("under-voltage has occurred since last reboot")
            if bitmap & (1 << 17) != 0:
                print("ARM frequency capping has occurred since last reboot")
            if bitmap & (1 << 18) != 0:
                print("throttling has occurred since last reboot")
            if bitmap & (1 << 19) != 0:
                print("soft temperature reached since last reboot")
        elif result.stderr:
            print("Error:", result.stderr)
    except subprocess.TimeoutExpired:
        print("Timeout")


if __name__ == "__main__":
    while True:
        get_voltage_status()
        time.sleep(DELAY_TIME)
