"""
HITL Test - GPS + Camera Feed Verification

Tests:
1. Read GPS data from FlightController
2. Check camera feed from image emulator
"""

import os
import time

from modules.mavlink import flight_controller


PIXHAWK_ADDRESS = "tcp:localhost:5762"
TEST_DURATION = 10


def main() -> int:
    """
    GPS data reading + camera feed check.
    Returns 0 on success, non-zero on failure.
    """
    images_path = os.path.join("tests", "integration", "camera_emulator", "images")

    print("HITL Test")
    print("=============")

    # Create FlightController with HITL enabled
    result, controller = flight_controller.FlightController.create(
        PIXHAWK_ADDRESS, 57600, True, True, True, images_path
    )

    if not result or controller is None:
        print("ERROR: FlightController creation failed")
        return -1

    print("FlightController created")

    # Start HITL emulators
    if controller.hitl_instance is not None:
        controller.hitl_instance.start()
        print("HITL emulators started")
    else:
        print("ERROR: HITL instance not created")
        return -1

    time.sleep(2)  # Initialization time

    try:
        print(f"\nRunning test for {TEST_DURATION}s...")
        start_time = time.time()
        gps_count = 0
        camera_count = 0

        while time.time() - start_time < TEST_DURATION:
            current_time = time.time() - start_time

            # Test GPS data every 2 seconds
            if int(current_time) % 2 == 0 and current_time > 0:
                success, location = controller.get_location()
                if success and location is not None:
                    lat, lon, alt = location
                    gps_count += 1
                    print(f"GPS: {lat:.6f}, {lon:.6f}, {alt:.1f}m")
                else:
                    print("GPS: No data")

            # Test camera feed every 3 seconds  
            if int(current_time) % 3 == 0 and current_time > 1:
                if controller.hitl_instance and controller.hitl_instance.camera_emulator:
                    try:
                        frame = controller.hitl_instance.camera_emulator._CameraEmulator__current_frame
                        if frame is not None:
                            camera_count += 1
                            print("Camera: Frame available")
                        else:
                            print("Camera: No frame")
                    except Exception as exc:
                        print(f"Camera: Error accessing frame - {exc}")
                else:
                    print("Camera: No emulator")

            time.sleep(0.5)

        # Results
        print(f"\nResults:")
        print(f"GPS readings: {gps_count}")
        print(f"Camera frames: {camera_count}")

        success = gps_count > 0 and camera_count > 0
        print("PASS" if success else "FAIL")
        return 0 if success else 1

    except Exception as exc:
        print(f"Test error: {exc}")
        return 1
    finally:
        if controller.hitl_instance is not None:
            controller.hitl_instance.shutdown()

if __name__ == "__main__":
    exit(main())
    