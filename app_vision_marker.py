
import random

# markers_num = [
#     rm_define.cond_recognized_marker_number_two,
#     rm_define.cond_recognized_marker_number_three,
#     rm_define.cond_recognized_marker_number_five,
# ]

# media_ctrl.play_sound(rm_define.media_custom_audio_0, wait_for_complete_flag=True)
# media_ctrl.play_sound(rm_define.media_custom_audio_1, wait_for_complete_flag=True)
# media_ctrl.play_sound(rm_define.media_custom_audio_2, wait_for_complete_flag=True)
# media_ctrl.play_sound(rm_define.media_custom_audio_3, wait_for_complete_flag=True)
# media_ctrl.play_sound(rm_define.media_custom_audio_4, wait_for_complete_flag=True)
# media_ctrl.play_sound(rm_define.media_custom_audio_5, wait_for_complete_flag=True)

markers_num_dict = {
    rm_define.cond_recognized_marker_number_two: rm_define.media_custom_audio_4, # 4
    rm_define.cond_recognized_marker_number_three: rm_define.media_custom_audio_0, # 0
    rm_define.cond_recognized_marker_number_five: rm_define.media_custom_audio_3, # 3
}

# marker_letter = [
#     rm_define.cond_recognized_marker_letter_M, # 5
#     rm_define.cond_recognized_marker_letter_S, # 1
# ]

## simon says = 2

marker_letter_dict = {
    rm_define.cond_recognized_marker_letter_M: rm_define.media_custom_audio_5,
    rm_define.cond_recognized_marker_letter_S: rm_define.media_custom_audio_1,
}


marker_num_all = rm_define.cond_recognized_marker_number_all
marker_letter_all = rm_define.cond_recognized_marker_letter_all

marker_all = [
    marker_num_all, marker_letter_all,
]

# list of all marker dictionaries
marker_dicts = [markers_num_dict, marker_letter_dict]

# which_num = random.randint(0,8)
# which_letter = random.randint(0,25)

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

    # randomly select one out of all the markers 
    # marker = markers_num[which_num]

    # select one dict out of all of them
    selected_dict = random.choice(marker_dicts)

    # select one key in dict
    marker = random.choice(list(selected_dict.keys()))

    # constantly running
    while True: 
        audio = markers_num_dict[marker]
        media_ctrl.play_sound(audio, wait_for_complete_flag=True)
        time.sleep(10)
        if vision_ctrl.check_condition(marker):
            # led light changes to orange
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 161, 255, 69, rm_define.effect_always_on)
            # robot moves forward by 1 meter
            chassis_ctrl.move_with_distance(0,1)
            # put audio here
        else:
            time.sleep(10)
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
            shoot_one_lazer()