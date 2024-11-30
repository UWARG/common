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
    "Enum class for worker classes. Acts as message ID"
    ADD_RANDOM_WORKER = 1
    CLUSTER_ESTIMATION_WORKER = 2
    COMMUNICATIONS_WORKER = 3
    CONCACENATOR_WORKER = 4
    COUNTUP_WORKER = 5
    DATA_MERGE_WORKER = 6
    DETECT_TARGET_WORKER = 7
    FLIGHT_INTERFERENCE_WORKER = 8
    GEOLOCATION_WORKER = 9
    VIDEO_INPUT_WORKER = 10
