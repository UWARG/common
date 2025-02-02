"""
Enumeration for Worker Types.

This enum class defines unique identifiers for different worker types in the system.
Each worker type is associated with a specific task, represented by a unique integer ID.

Workers can be found in UWARG/computer-vision-python Github repository

Usage:
    This enum can be used to identify and categorize workers programmatically.
    For example, `Worker_Enum.COMMUNICATIONS_WORKER.value` will return the integer ID `3`.
"""

from enum import Enum


class WorkerEnum(Enum):
    """
    Enum class for worker classes. Acts as message ID
    """

    CLUSTER_ESTIMATION_WORKER = 1
    COMMUNICATIONS_WORKER = 2
    DATA_MERGE_WORKER = 3
    DETECT_TARGET_WORKER = 4
    FLIGHT_INTERFACE_WORKER = 5
    GEOLOCATION_WORKER = 6
    VIDEO_INPUT_WORKER = 7
