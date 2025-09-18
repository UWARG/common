"""
Setup for HITL modules.
"""

import time
from threading import Event, Thread
from modules.hitl.position_emulator import PositionEmulator
from modules.hitl.camera_emulator import CameraEmulator
from ..mavlink import dronekit


class HITL:
    """
    Hardware In The Loop (HITL) setup for emulating drone hardware.
    Provides a way to emulate the drone's position and camera input
    for testing purposes without needing actual hardware.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        drone: dronekit.Vehicle,
        hitl_enabled: bool,
        position_module: bool,
        camera_module: bool,
        images_path: str | None = None,
    ) -> "tuple[True, HITL] | tuple[False, None]":
        """
        Factory method to create a HITL instance.

        Args:
            drone: The dronekit instance to use for sending MAVLink messages.
            hitl_enabled: Boolean indicating if HITL is enabled.
            position_module: Boolean indicating if the position module is enabled.
            camera_module: Boolean indicating if the camera module is enabled.
            images_path: Optional path to the images directory for the camera emulator.

        Returns:
            Success, HITL instance | None.
        """
        if not isinstance(drone, dronekit.Vehicle):
            return False, None

        if not hitl_enabled:
            return True, HITL(cls.__create_key, drone, None, None)

        if position_module:
            result, position_emulator = PositionEmulator.create(drone)
            if not result:
                return False, None

        if camera_module:
            result, camera_emulator = CameraEmulator.create(images_path)
            if not result:
                return False, None

        hitl = HITL(
            cls.__create_key,
            drone,
            position_emulator if position_module else None,
            camera_emulator if camera_module else None,
        )

        return True, hitl

    def __init__(
        self,
        class_private_create_key: object,
        drone: dronekit.Vehicle,
        position_emulator: "PositionEmulator | None" = None,
        camera_emulator: "CameraEmulator | None" = None,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is HITL.__create_key, "Use create() method"

        self.drone = drone
        self.position_emulator = position_emulator
        self.camera_emulator = camera_emulator

    def set_inject_position(self) -> None:
        """
        Start HITL module threads.
        """
        if self._stop_event is not None:
            return

        self._stop_event = Event()
        self._threads = []

        if self.position_emulator is not None:
            t = Thread(target=self.run_position, name="HITL-Position", daemon=True)
            self._threads.append(t)
            t.start()

        if self.camera_emulator is not None:
            t = Thread(target=self.run_camera, name="HITL-Camera", daemon=True)
            self._threads.append(t)
            t.start()

    def shutdown(self, join_timeout: float | None = 5.0) -> None:
        """
        Signal threads to stop and join them.
        """
        if self._stop_event is None:
            return

        self._stop_event.set()

        for t in self._threads:
            if t.is_alive():
                t.join(timeout=join_timeout)

        self._threads.clear()
        self._stop_event = None

    def __del__(self) -> None:
        """
        Best-effort cleanup when HITL object is destroyed.
        Ensures threads are stopped and the drone connection is closed.
        """
        try:
            self.shutdown()
        except Exception:  # pylint: disable=broad-except
            pass

    def run_position(self) -> None:
        """
        Runs the position emulator periodic function in a loop.
        """
        assert self._stop_event is not None
        while not self._stop_event.is_set():
            try:
                self.position_emulator.periodic()
            except Exception as exc:  # pylint: disable=broad-except
                print(f"HITL position thread error: {exc}")
                time.sleep(0.1)

    def run_camera(self) -> None:
        """
        Runs the camera emulator periodic function in a loop.
        """
        assert self._stop_event is not None
        while not self._stop_event.is_set():
            try:
                self.camera_emulator.periodic()
            except Exception as exc:  # pylint: disable=broad-except
                print(f"HITL camera thread error: {exc}")
                time.sleep(0.1)
