"""
Emulates camera input to PI.

Requires OBS Virtual Camera on Windows or
v4l2loopback for Linux to be installed to work
"""

import os
import time
import pyvirtualcam
import cv2

IMAGE_SIZE = (720, 480)
IMAGE_FORMATS = (".png", ".jpeg", "jpg")
CAMERA_FPS = 30


class CameraEmulator:
    """
    Setup for camera emulator.
    """

    __create_key = object()

    @classmethod
    def create(cls, images_path: str) -> "tuple[True, CameraEmulator] | tuple[False, None]":
        """
        Setup camera emulator.

        Args:
            images_path: Path to the directory containing images for the camera emulator. Cycles through these images to simulate camera input (every 1 second).

        Returns:
            Success, CameraEmulator instance.
        """

        if not isinstance(images_path, str):
            return False, None

        try:
            virtual_camera_instance = pyvirtualcam.Camera(IMAGE_SIZE[0], IMAGE_SIZE[1], CAMERA_FPS)

        # Required for catching library exceptions
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            print(
                "Error creating virtual camera (Check if OBS or v4l2loopback is installed): "
                + str(e)
            )
            return False, None

        if virtual_camera_instance is None:
            return False, None

        return True, CameraEmulator(cls.__create_key, images_path, virtual_camera_instance)

    def __init__(
        self, class_private_create_key: object, images_path: str, virtual_camera: pyvirtualcam
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is CameraEmulator.__create_key, "Use create() method"

        self.__image_folder_path = images_path
        self.__virtual_camera = virtual_camera
        self.__image_paths: "list[str]" = []
        self.__current_frame = None
        self.__image_index = 0
        self.__next_image_time = time.time() + 1.0

        self.__get_images()
        self.update_current_image()

    def periodic(self) -> None:
        """
        Periodic function.
        """
        try:
            # Send frame and pace to target FPS
            self.send_frame()
            self.sleep_until_next_frame()

            now = time.time()
            if now >= self.__next_image_time:
                # Cycle image once per second
                try:
                    self.next_image()
                    self.update_current_image()
                except Exception as exc:  # pylint: disable=broad-except
                    print(f"HITL camera image update error: {exc}")
                self.__next_image_time = now + 1.0
        except Exception as exc:  # pylint: disable=broad-except
            print(f"HITL camera periodic error: {exc}")

    def send_frame(self) -> None:
        """
        sends a new frame to virtual camera, should be called in a loop

        """
        try:
            self.__virtual_camera.send(self.__current_frame)

        # Required for catching library exceptions
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            print("Cannot send frame" + str(e))

    def sleep_until_next_frame(self) -> None:
        """
        Waits an amount of time to maintain targeted framerate
        (Wrapper for pyvirtualcam)
        """
        self.__virtual_camera.sleep_until_next_frame()

    def update_current_image(self) -> None:
        """
        sets curr_img to the image specified by the curr_img_index
        """

        has_image = False
        loop_count = 0

        # loop to skip image if read fails
        while not has_image and loop_count < len(self.__image_paths):
            try:
                image_path = self.__image_paths[self.__image_index]
                image = cv2.imread(image_path)
                self.__current_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                has_image = True

            # Required for catching library exceptions
            # pylint: disable-next=broad-exception-caught
            except Exception as e:
                print("Could not read image: " + image_path + " Error: " + str(e))
                self.next_image()
                loop_count += 1

    def next_image(self) -> None:
        """
        increments image index by 1
        """

        self.__image_index = (self.__image_index + 1) % len(self.__image_paths)

    def __get_images(self) -> None:
        """
        populates _images array with paths of all images in the folder
        """
        try:
            for image in os.listdir(self.__image_folder_path):
                if image.endswith(IMAGE_FORMATS):
                    path = os.path.join(self.__image_folder_path, image)
                    self.__image_paths.append(path)

        # Required for catching library exceptions
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            print("Error reading images: " + str(e))
