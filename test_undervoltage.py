"""
Test if the Rpi is not recieving enough voltage
"""

import subprocess
import time


DELAY_TIME = 1.0  # seconds
TIMEOUT = 3.0  # seconds


def get_voltage_status() -> None:
    # Should be in the format "throttled=0x1"
    # https://forums.raspberrypi.com/viewtopic.php?p=1570562&sid=e34c4c7122b8e7d232fb0673415135a3
    try:
        result = subprocess.run(
            ['vcgencmd', 'get_throttled'],
            capture_output=True,
            encoding='utf-8',
            timeout=TIMEOUT
        )
        if result.stdout:
            bitmap = int(result.stdout.split('=')[1], base=0)
            if bitmap & (1 << 0) != 0:
                print("currently undervolted")
            if bitmap & (1 << 1) != 0:
                print("ARM frequency currently capped")
            if bitmap & (1 << 2) != 0:
                print("currently throttled")
            if bitmap & (1 << 3) != 0:
                print("soft temperature limit reached")
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
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    while True:
        get_voltage_status()
        time.sleep(DELAY_TIME)
