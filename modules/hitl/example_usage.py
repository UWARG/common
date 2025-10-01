#!/usr/bin/env python3
"""
Example usage of the JSON Position Emulator in HITL mode.
This demonstrates how the position emulator cycles through JSON coordinates.
"""

import time
from modules.hitl.hitl_base import HITL
from modules.mavlink import dronekit

def example_json_position_emulator():
    """
    Example showing how the JSON position emulator works.
    """
    
    # Example 1: Basic usage with JSON file
    print("=== Example 1: Basic JSON Position Emulation ===")
    
    # Create a mock drone (in real usage, this would be a real dronekit.Vehicle)
    # For this example, we'll assume you have a real drone connection
    # drone = dronekit.connect("tcp:127.0.0.1:5760")  # SITL connection
    
    # Create HITL with JSON coordinates
    success, hitl = HITL.create(
        drone=None,  # Replace with actual drone connection
        hitl_enabled=True,
        position_module=True,
        camera_module=False,
        json_file_path="test_coordinates.json",  # Our test file
        position_update_interval=1.0  # 1 second intervals
    )
    
    if success and hitl:
        print("✅ HITL created successfully with JSON position emulation")
        print("📁 JSON file: test_coordinates.json")
        print("⏱️  Update interval: 1.0 seconds")
        print("🔄 Will cycle through coordinates every second")
        
        # Start the HITL system
        hitl.start()
        print("🚀 HITL started - position emulation running...")
        
        # Simulate running for 5 seconds to show coordinate cycling
        print("\n📊 Coordinate cycling simulation:")
        for i in range(5):
            time.sleep(1)
            print(f"⏰ Time: {i+1}s - Position emulator is running...")
        
        # Stop the system
        hitl.shutdown()
        print("🛑 HITL stopped")
    
    print("\n" + "="*60)
    
    # Example 2: Custom update interval
    print("=== Example 2: Custom Update Interval (2 seconds) ===")
    
    success, hitl2 = HITL.create(
        drone=None,  # Replace with actual drone connection
        hitl_enabled=True,
        position_module=True,
        camera_module=False,
        json_file_path="test_coordinates.json",
        position_update_interval=2.0  # 2 second intervals
    )
    
    if success and hitl2:
        print("✅ HITL created with 2-second update interval")
        print("⏱️  Coordinates will change every 2 seconds")
    
    print("\n" + "="*60)
    
    # Example 3: No JSON file (uses Ardupilot)
    print("=== Example 3: No JSON File (Ardupilot Mode) ===")
    
    success, hitl3 = HITL.create(
        drone=None,  # Replace with actual drone connection
        hitl_enabled=True,
        position_module=True,
        camera_module=False
        # No json_file_path - will use Ardupilot pathing
    )
    
    if success and hitl3:
        print("✅ HITL created without JSON file")
        print("🎯 Will use Ardupilot's internal pathing")
        print("❌ No 1-second coordinate shifting")

def explain_coordinate_cycling():
    """
    Explains how the coordinate cycling works internally.
    """
    print("\n" + "="*60)
    print("🔍 HOW COORDINATE CYCLING WORKS INTERNALLY")
    print("="*60)
    
    print("""
1. 📁 JSON Loading:
   - Loads coordinates from test_coordinates.json
   - Validates format: [[lat, lon, alt], [lat, lon, alt], ...]
   - Stores in self.json_coordinates list

2. ⏰ Timing Control:
   - Sets next_coordinate_time = current_time + update_interval
   - Checks every periodic() call if it's time to update

3. 🔄 Coordinate Cycling:
   - Gets current coordinate: json_coordinates[current_index]
   - Calls set_target_position(lat, lon, alt)
   - Increments current_index (cycles back to 0 at end)
   - Updates next_coordinate_time for next cycle

4. 📡 Position Injection:
   - inject_position() sends GPS data to flight controller
   - Uses MAVLink GPS_INPUT message
   - Simulates GPS coordinates for the drone

5. 🎯 Priority System:
   - JSON coordinates have priority over Ardupilot
   - If JSON available: use JSON cycling
   - If no JSON: fallback to Ardupilot pathing
""")

def show_json_format():
    """
    Shows the expected JSON format and example data.
    """
    print("\n" + "="*60)
    print("📄 JSON FILE FORMAT")
    print("="*60)
    
    print("""
Expected JSON format:
[
    [latitude, longitude, altitude],
    [latitude, longitude, altitude],
    ...
]

Example (test_coordinates.json):
[
    [43.43405014107003, -80.57898027451816, 373.0],
    [40.0, -40.0, 200.0],
    [41.29129039399329, -81.78471782918818, 373.0]
]

This will cycle through:
1. First coordinate for 1 second
2. Second coordinate for 1 second  
3. Third coordinate for 1 second
4. Back to first coordinate (loops forever)
""")

if __name__ == "__main__":
    print("🚁 HITL JSON Position Emulator Example")
    print("="*60)
    
    # Show JSON format
    show_json_format()
    
    # Explain how it works
    explain_coordinate_cycling()
    
    # Run examples (commented out since we don't have real drone)
    print("\n" + "="*60)
    print("💡 TO USE IN REAL CODE:")
    print("="*60)
    print("""
# In your flight_controller.py:
from modules.hitl.hitl_base import HITL

# Create HITL with JSON coordinates
success, hitl = HITL.create(
    drone=your_drone_connection,
    hitl_enabled=True,
    position_module=True,
    camera_module=False,
    json_file_path="path/to/your/coordinates.json",
    position_update_interval=1.0  # seconds
)

if success:
    hitl.start()  # Start position emulation
    # Your main flight loop here
    hitl.shutdown()  # Clean shutdown
""")
    
    # Uncomment to run actual examples (requires drone connection):
    # example_json_position_emulator()
