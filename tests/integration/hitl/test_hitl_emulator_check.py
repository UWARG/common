"""
HITL Test - GPS + Camera Feed Verification

"""

import cv2
import os
import time

from modules.mavlink import flight_controller

# /dev/ttyAMA0 for drone, tcp:127.0.0.1:14550 for mission planner simulator
PIXHAWK_ADDRESS = "tcp:127.0.0.1:14550"
TEST_DURATION = 100


def test_camera_feed() -> bool:
    """
    Returns True if camera feed is available, False otherwise.
    """
    try:
        camera = cv2.VideoCapture(2)

        if not camera.isOpened():
            camera.release()
            return False

        ret, frame = camera.read()
        camera.release()

        if ret and frame is not None and frame.size > 0:
            return True

        return False

    except Exception:
        return False


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
    if controller.hitl_instance is not None:
        print("HITL emulators running")

        print("Waiting for camera creation...")
        time.sleep(2)

        print("Checking for camera...")
        camera_available = test_camera_feed()
        if camera_available:
            print("Camera: detected")
        else:
            print("Camera: not detected")

    else:
        print("ERROR: HITL instance not created")
        return -1

    try:
        print(f"\nRunning test for {TEST_DURATION}s...")
        start_time = time.time()
        gps_count = 0
        camera_count = 0

        while time.time() - start_time < TEST_DURATION:
            current_time = time.time() - start_time

            if int(current_time) % 2 == 0 and current_time > 0:
                success, location = controller.get_location()
                
                if success and location is not None:
                    lat, lon, alt = location
                    gps_count += 1
                    print(f"GPS: {lat:.6f}, {lon:.6f}, {alt:.1f}m")
                    controller.hitl_instance.position_emulator.set_target_position(
                        lat + 0.001,  
                        lon + 0.001,  
                        alt + 10      
                    )
                    

                else:
                    print("GPS: No data")
                    
            # Test camera feed every 3 seconds
            if int(current_time) % 3 == 0 and current_time > 1:
                if test_camera_feed():
                    camera_count += 1
                    print("Camera: Feed available")
                else:
                    print("Camera: No feed")

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
