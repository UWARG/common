"""
Test flight interface's send_statustext_msg function.
"""

import pytest

from pymavlink import mavutil

from modules.mavlink.flight_controller import FlightController


@pytest.fixture
def mock_drone(mocker):
    """
    Mock drone to return test message.
    """
    mock_drone = mocker.Mock()
    mock_drone.message_factory.statustext_encode.return_value = "test_message"
    return mock_drone


def test_send_statustext_msg_valid(mock_drone):
    """
    Test message under 50 characters.
    """
    controller = FlightController(
        class_private_create_key=FlightController._FlightController__create_key,
        vehicle=mock_drone,
    )

    result = controller.send_statustext_msg("OK")

    assert result is True
    mock_drone.message_factory.statustext_encode.assert_called_once_with(
        mavutil.mavlink.MAV_SEVERITY_INFO, b"OK"
    )
    mock_drone.send_mavlink.assert_called_once_with("test_message")


def test_send_statustext_msg_invalid(mock_drone):
    """
    Test message over 50 characters.
    """
    controller = FlightController(
        class_private_create_key=FlightController._FlightController__create_key,
        vehicle=mock_drone,
    )

    invalid_message = "x" * 51  # 51 bytes
    result = controller.send_statustext_msg(invalid_message)

    assert result is False
    mock_drone.message_factory.statustext_encode.assert_not_called()
    mock_drone.send_mavlink.assert_not_called()
