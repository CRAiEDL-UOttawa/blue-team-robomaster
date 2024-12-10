"""
File: follow_line.py
Author: Yasin, Vanisha, Michael
Date: 17/11/2024
Description: This script leverages follows a line and leveraged PID to do so
"""

# Code for following line (currently blue)
# Needs further testing + Mod

# Define variables, list for lines and PID for line following
variable_lineList = 0
variable_X = 0
variable_V = 0
list_LineList = RmList()
pid_FollowLine = PIDCtrl()

def start():
    global variable_lineList
    global variable_X
    global variable_V
    global list_LineList
    global pid_FollowLine
    # Enable line detection and define which color the line is
    vision_ctrl.enable_detection(rm_define.vision_detection_line)
    vision_ctrl.line_follow_color_set(rm_define.line_follow_color_blue)

    # Adjust exposure for viewing line
    media_ctrl.exposure_value_update(rm_define.exposure_value_small)
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)

    # Recommended to set gimbal down 20 degrees
    gimbal_ctrl.rotate_with_degree(rm_define.gimbal_down,20)

    gimbal_ctrl.rotate(rm_define.gimbal_right)
    pid_FollowLine.set_ctrl_params(100,0,15)

    while True:
        list_LineList=RmList(vision_ctrl.get_line_detection_info())

        if len(list_LineList) > 2:
            # LEDs for testing, help confirm that line is identified
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_flash)
            led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 0, rm_define.effect_flash)
            media_ctrl.play_sound(rm_define.media_sound_recognize_success)

            # Current understanding is, when the line list has a size of 42...
            # We have a line to follow!
            if len(list_LineList) == 42:
                # Not quite familiar with this, but these IF statements tell us if there is more line to traverse...
                if list_LineList[2] == 1:
                    variable_X = list_LineList[11]
                    pid_FollowLine.set_error(variable_X - 0.5)
                    variable_V = (0.2 * abs(list_LineList[11])) / 180
                    chassis_ctrl.move_with_speed(variable_V / 2,0,pid_FollowLine.get_output())

                else: # Else, we don't move
                    chassis_ctrl.move_with_speed(0,0,0)

        time.sleep(1) # Sleep each cycle
