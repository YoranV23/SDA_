import DoBotArm  # Import your Dobot control module

# Function to move the Dobot from home to another position
def move_to_position(dobot, x, y, z):
    # Move the Dobot to the specified position (x, y, z)
    dobot.moveArmXYZ(x, y, z, wait=True)

# Main program
if __name__ == "__main__":
    # Define the home position and the target positions
    homeX, homeY, homeZ = 120, 0, 60
    target_positions = [(114, -150, -35), (120, -170, -35), (140, -160, -35)]

    # Connect to the Dobot
    port = 'COM12'  # Replace with your Dobot's COM port
    dobot = DoBotArm.DoBotArm(port, homeX, homeY, homeZ, home=True)

    # Loop through the movements three times
    for _ in range(3):
        for target_position in target_positions:
            move_to_position(dobot, *target_position)

    # Disconnect from the Dobot
    dobot.dobotDisconnect()
