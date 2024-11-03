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
        time.sleep(10)
        if media_ctrl.check_condition(rm_define.cond_sound_recognized_applause_thrice):
            # led light changes to orange
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 161, 255, 69, rm_define.effect_always_on)
            media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
            # robot moves forward by 1 meter
            chassis_ctrl.move_with_distance(0,1)
            # put audio here
        else:
            time.sleep(10)
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
            shoot_one_lazer()