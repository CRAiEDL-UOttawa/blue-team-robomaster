"""
File: detect_vision_card_upDown.py
Author: Yasin, Vanisha, Michael
Date: 10/12/2024
Description: Script for detecting 3 claps within a time frame
"""
# shoot lazer out
def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)


def start():
    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)
    while True:
        media_ctrl.play_sound(audio, wait_for_complete_flag=True)
        # timer
        tools.timer_ctrl(rm_define.timer_start)
        if media_ctrl.check_condition(rm_define.cond_sound_recognized_applause_thrice):
            # led light changes to orange
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 161, 255, 69, rm_define.effect_always_on)
            media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
            # robot moves forward by 1 meter
            chassis_ctrl.move_with_distance(0,1)
            # put audio here
        else:
            if tools.timer_current() > 10:
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
            for count in range(5):
                shoot_one_lazer()
            rmexit()