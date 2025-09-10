from pyniryo import *
from pyniryo.vision import *

robot = NiryoRobot('169.254.200.200')

robot.calibrate_auto()

# Define the four corners of the square
corner_1 = PoseObject(x=0.2, y=0.2, z=0.2, roll=0, pitch=0, yaw=0)
corner_2 = PoseObject(x=0.2, y=-0.2, z=0.2, roll=0, pitch=0, yaw=0)
corner_3 = PoseObject(x=-0.2, y=-0.2, z=0.2, roll=0, pitch=0, yaw=0)
corner_4 = PoseObject(x=-0.2, y=0.2, z=0.2, roll=0, pitch=0, yaw=0)

try:
    # Move to each corner of the square
    print("Moving to Corner 1")
    robot.move_joints(corner_1)
    robot.wait(2)

    print("Moving to Corner 2")
    robot.move_joints(corner_2)
    robot.wait(2)

    print("Moving to Corner 3")
    robot.move_joints(corner_3)
    robot.wait(2)

    print("Moving to Corner 4")
    robot.move_joints(corner_4)
    robot.wait(2)

    print("Returning to Corner 1")
    robot.move_joints(corner_1)
    robot.wait(2)

except KeyboardInterrupt as e:
    print(f"An error occurred: {e}")
finally:
    robot.close_connection()