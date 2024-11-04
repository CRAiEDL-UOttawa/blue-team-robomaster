
import random

markers_num_dict = {
    rm_define.cond_recognized_marker_number_two: rm_define.media_custom_audio_4, 
    rm_define.cond_recognized_marker_number_three: rm_define.media_custom_audio_0, 
    rm_define.cond_recognized_marker_number_five: rm_define.media_custom_audio_3, 
}

# shoot lazer out
def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)

def start():
    # vision detection enabled
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 50, 0, rm_define.effect_always_on)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)

    # max distance 
    vision_ctrl.set_marker_detection_distance(1)

    # constantly running
    while True: 
        # select one key in dict
        marker = random.choice(list(markers_num_dict.keys()))

        audio = markers_num_dict[marker]
        media_ctrl.play_sound(audio, wait_for_complete_flag=True)
        # timer
        tools.timer_ctrl(rm_define.timer_start)
        if vision_ctrl.check_condition(marker):
            # led light changes to orange
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 161, 255, 69, rm_define.effect_always_on)
            media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
            # robot moves forward by 1 meter
            chassis_ctrl.move_with_distance(0,1)
             
        else:
            if tools.timer_current() > 10:
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
            for count in range(5):
                shoot_one_lazer()