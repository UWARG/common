"""
Test for the hitl camera emulator

See test_camera_slideshow for instructions
"""

import cv2

def main() -> None:
    """
    Shows video feed from camera
    """
    camera = cv2.VideoCapture(2)

    while True:
        ret, frame = camera.read()
        if ret:
            cv2.imshow("Camera", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
