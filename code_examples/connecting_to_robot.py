from pyniryo import *
from pyniryo.vision import *

robot = NiryoRobot('169.254.200.200')

robot.calibrate_auto()
robot_pose_1 = PoseObject(x = -0.0430, y = -0.2777, z = 0.1023,roll = -0.255, pitch = 1.160, yaw = -1.733)
robot_pose_2 = PoseObject(x = 0.2106, y = 0.2751, z = 0.1507, roll = 0.212, pitch = 0.880, yaw = 0.923)
wait_flag = True
joint_pose = robot.get_joints()
print("joint",joint_pose)
robot.update_tool()

# Your code should be here
try:
    # robot.led_ring_flashing([255, 0, 0])
    pose = robot.get_pose()
    # print(pose)
    # robot.wait(5)
    # print("Moving to home pose")
    # robot.move_to_home_pose()
    # robot.wait(5)
    # print("reducing speed")
    # robot.set_arm_max_velocity(40)
    # print("Moving to pos 1")
    # # robot.move_pose(robot_pose_1)
    # robot.wait(5)
    # print("Moving to pos 2")
    # robot.move_pose(robot_pose_2)
    print("gripper open")
    robot.release_with_tool()
    print("close gripper")
    robot.grasp_with_tool()


except KeyboardInterrupt as e:
    print(f"An error occurred: {e}")
    robot.close_connection()


# x = -0.0430, y = -0.2777, z = 0.1023
# roll = -0.255, pitch = 1.160, yaw = -1.733


# x = 0.2106, y = 0.2751, z = 0.1507
# roll = 0.212, pitch = 0.880, yaw = 0.923