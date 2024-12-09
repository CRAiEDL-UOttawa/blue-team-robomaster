"""
File: detect_gesture.py
Author: Yasin, Vanisha, Michael
Date: 10/12/2024
Description: This script contains game logic for detecting a randomly selected gesture within a given time range,
when gesture is randomly selected, make function call. Borrowed logic from 'clap_recognition.py'
"""

# Game logic for detecting a randomly selected gesture within a given time range
# When gesture is randomly selected, make function call
# Borrowed logic from 'gestures.py' and 'clap_recognition.py'

gesture_af = ['AUDIO1', 'AUDIO2', 'AUDIO3', 'AUDIO4', 'AUDIO5']
gesture = ['two_clap', 'three_clap', 'capture', 'hands_up', 'hands_down']

# Robomaster command dict makes calling correct gesture easier (i hope)
gesture_dict = {'two_clap': rm_define.cond_sound_recognized_applause_twice, 'three_clap': rm_define.cond_sound_recognized_applause_thrice, 'capture': rm_define.cond_recognized_pose_capture, 'hands_up': rm_define.cond_recognized_pose_victory, 'hands_down': rm_define.cond_recognized_pose_give_in}

def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)

# Where 'gesture' is one of the several keys in 'gesture_dict'
def detect_gesture(gesture, simon_says:bool, round_time):

    gesture_cmd = gesture_dict.get(gesture)

    # timer
    tools.timer_ctrl(rm_define.timer_start)

    while tools.timer_current() < round_time:

        # If specified gesture is observed
        if media_ctrl.check_condition(gesture_cmd):

            # If simon did not say, player loses
            if simon_says:
                # led light changes to orange
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 0, 255, 0, rm_define.effect_always_on)
                media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
                # robot moves forward by 1 meter
                chassis_ctrl.move_with_distance(0,1)
                # put audio here

            else:
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
                shoot_one_lazer()

    # Timer ended, no gesture detected
    # Simon didn't say... (win)
    if tools.timer_current() > 10 & (not simon_says):
        # TODO - What occurs when player doesn't react and simon didn't say
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 0, 255, 0, rm_define.effect_always_on)
        
    
    # Simon did say... (lose)
    else:
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
        shoot_one_lazer()


    tools.timer_ctrl(rm_define.timer_reset)

# TODO - finding best camera settings for identifying gestures in game area