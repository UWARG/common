# Position Emulator Test Script

This test script (`test_position_emulator_waypoints.py`) is designed to test the changes made to the `position_emulator.py` module by sending 2 waypoints and verifying that the drone moves correctly in Mission Planner.

## Purpose

The script tests the position emulator functionality by:
1. Connecting to a Pixhawk via Raspberry Pi (or simulation)
2. Enabling Hardware-in-the-Loop (HITL) mode with position emulation
3. Creating and uploading a mission with 2 test waypoints
4. Monitoring drone movement and providing real-time status updates
5. Verifying smooth GPS position interpolation in Mission Planner

## Prerequisites

### Pixhawk Parameter Configuration

Before running the test, you **must** configure the following parameters on your Pixhawk for HITL GPS simulation:

#### In Mission Planner:
1. Go to **CONFIG/TUNING > Full Parameter List**
2. Set the following parameters:

**Sensor Disabling:**
- `INS_ENABLE_MASK = 0`
- `COMPASS_ENABLE = 0`

**EKF Configuration:**
- `AHRS_EKF_TYPE = 3`
- `EK3_ENABLE = 1`
- `EK3_SRC1_POSXY = 3` (GPS)
- `EK3_SRC1_POSZ = 3` (GPS - altitude from GPS only)
- `EK3_SRC1_VELXY = 3` (GPS)
- `EK3_SRC1_VELZ = 3` (GPS)

**GPS Simulation via MAVLink:**
- `GPS_TYPE = 14` (Use MAVLink GPS_INPUT)
- `GPS_TYPE2 = 0`
- `GPS_AUTO_SWITCH = 0`
- `GPS_PRIMARY = 0`

3. **Write parameters** to the Pixhawk
4. **Reboot** the Pixhawk

⚠️ **Important**: The test script will check these parameters and warn you if they're not set correctly.

## Usage

### Raspberry Pi + Pixhawk Setup
```bash
# Run with physical hardware connection
python test_position_emulator_waypoints.py --connection /dev/ttyAMA0
```

### SITL Simulation
```bash
# Run with Software-in-the-Loop simulation
python test_position_emulator_waypoints.py --connection tcp:127.0.0.1:5762
```

### Mission Planner Connection
```bash
# Connect directly to Mission Planner
python test_position_emulator_waypoints.py --connection tcp:127.0.0.1:14550
```

### Custom Duration
```bash
# Monitor for 5 minutes instead of default 2 minutes
python test_position_emulator_waypoints.py --connection /dev/ttyAMA0 --duration 300
```

## Test Waypoints

The script uses predefined waypoints around the University of Waterloo area:

- **Home Position**: 43.43405°N, 80.57898°W, 373m altitude
- **Waypoint 1**: 43.43450°N, 80.57900°W, 30m above home (~50m north)
- **Waypoint 2**: 43.43400°N, 80.57850°W, 25m above home (~50m south, 50m east)

## What to Expect

### In Mission Planner
1. **Map View**: You should see 2 waypoints plotted on the map
2. **Drone Position**: The drone icon should move smoothly between waypoints
3. **GPS Updates**: Position should update continuously without jumps or glitches
4. **Status Messages**: Real-time position updates will appear in the messages panel

### In Terminal Output
- Connection status and HITL setup confirmation
- Mission upload confirmation with waypoint coordinates
- Real-time position updates every second
- Flight mode and armed status
- Next waypoint information

## Testing Checklist

When running this test, verify the following:

**Pre-flight Setup:**
- [ ] Required Pixhawk parameters are configured (script will check this)
- [ ] Pixhawk has been rebooted after parameter changes
- [ ] Script connects successfully to the Pixhawk
- [ ] HITL mode is enabled with position emulation

**Mission Execution:**
- [ ] Mission with 2 waypoints uploads successfully
- [ ] Drone position updates smoothly in Mission Planner
- [ ] No GPS jumps or position glitches occur
- [ ] Position interpolation follows expected path between waypoints
- [ ] Status messages appear in Mission Planner
- [ ] Terminal shows consistent position updates

**GPS Simulation Validation:**
- [ ] GPS_INPUT messages are being sent to Pixhawk
- [ ] EKF is using GPS as primary position source
- [ ] Altitude comes from GPS only (EK3_SRC1_POSZ = 3)

## Troubleshooting

### Connection Issues
- **Permission denied on /dev/ttyAMA0**: Run with `sudo` or add user to `dialout` group
- **Connection refused**: Check that Pixhawk is connected and powered
- **No heartbeat**: Verify baud rate (57600) and connection string

### Mission Issues
- **Mission upload fails**: Check drone is in a compatible flight mode
- **No waypoints visible**: Ensure Mission Planner is connected to the same port
- **Drone doesn't move**: Try setting flight mode to AUTO manually in Mission Planner

### Position Updates
- **No position updates**: Verify HITL position module is enabled
- **Jerky movement**: Check movement_speed parameter (default: 5.0 m/s)
- **Wrong coordinates**: Verify waypoint coordinates are correct for your area

## Configuration

Key parameters can be modified at the top of the script:

```python
# Movement speed for position interpolation
MOVEMENT_SPEED = 5.0  # m/s

# Update interval for status messages
UPDATE_INTERVAL = 1.0  # seconds

# Test waypoint coordinates
WAYPOINT_1_LAT = 43.43450
WAYPOINT_1_LON = -80.57900
WAYPOINT_1_ALT = 30.0
```

## Expected Results

A successful test should demonstrate:
1. Smooth position interpolation between waypoints
2. Consistent GPS updates without glitches
3. Proper integration with Mission Planner
4. Accurate position emulation matching the configured movement speed

This validates that the position_emulator changes work correctly with real hardware and can be used for testing drone missions without actual flight.
