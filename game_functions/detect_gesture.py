# Game logic for detecting a randomly selected gesture within a given time range
# When gesture is randomly selected, make function call
# Borrowed logic from 'gestures.py' and 'clap_recognition.py'

gesture_af = ['AUDIO1', 'AUDIO2', 'AUDIO3', 'AUDIO4', 'AUDIO5']
gesture = ['two_clap', 'three_clap', 'capture', 'hands_up', 'hands_down']

# Robomaster command dict makes calling correct gesture easier (i hope)
gesture_dict = {'two_clap': 'rm_define.cond_sound_recognized_applause_twice', 'three_clap': 'rm_define.cond_sound_recognized_applause_thrice', 'capture': 'rm_define.cond_recognized_pose_capture', 'hands_up': 'rm_define.cond_recognized_pose_victory', 'hands_down': 'rm_define.cond_recognized_pose_give_in'}

def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)

# Where 'gesture' is one of the several keys in 'gesture_dict'
def detect_gesture(gesture, simon_says:bool):

    gesture_cmd = gesture_dict.get(gesture)

    # timer
    tools.timer_ctrl(rm_define.timer_start)

    # If specified gesture is observed
    if media_ctrl.check_condition(gesture_cmd):

        # If simon did not say, player loses
        if not simon_says:
            shoot_one_lazer()

        # led light changes to orange
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 161, 255, 69, rm_define.effect_always_on)
        media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
        # robot moves forward by 1 meter
        chassis_ctrl.move_with_distance(0,1)
        # put audio here

    else:
        # If timer runs out and Simon didn't say
        if tools.timer_current() > 10 & (not simon_says):
            # TODO - What occurs when player doesn't react and simon didn't say
            pass
        
        # If timer runs out and Simon did say
        elif tools.timer_current() > 10:
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)

        for count in range(5):
            shoot_one_lazer()


# TODO - finding best camera settings for identifying gestures in game area