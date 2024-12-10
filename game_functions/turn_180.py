"""
File: detect_obliteration.py
Author: Yasin, Vanisha, Michael
Date: 10/12/2024
Description: This script holds function for rotating the robomaster s1 180 degrees right 
"""

def turn_180_right():
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.rotate_with_speed(rm_define.clockwise,180)
    time.sleep(1)

def turn_180_left():
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.rotate_with_speed(rm_define.anticlockwise,180)
    time.sleep(1)