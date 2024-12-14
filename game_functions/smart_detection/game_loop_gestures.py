import random

# CUSTOME AUDIO 2 = Simon Says
# CUSTOME AUDIO 3 = Take Photo
# CUSTOME AUDIO 1 = HANDS UP
# CUSTOME AUDIO 0 = Hands Down

gesture_poses = [
    rm_define.cond_recognized_pose_capture,
    rm_define.cond_recognized_pose_victory,
    rm_define.cond_recognized_pose_give_in
]
gesture_audios = [
    rm_define.media_custom_audio_3,
    rm_define.media_custom_audio_1,
    rm_define.media_custom_audio_0
]

# Shoot lazer out
def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)


def start():
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 50, 0, rm_define.effect_always_on)
    vision_ctrl.enable_detection(rm_define.vision_detection_pose)
    gimbal_ctrl.rotate(rm_define.gimbal_up)
    

    for i in range(0,10):
        media_ctrl.play_sound(rm_define.media_custom_audio_2, wait_for_complete_flag=True)
        selected_audio = random.choice(gesture_audios)
        selected_index = gesture_audios.index(selected_audio)
        selected_pose = gesture_poses[selected_index]
        media_ctrl.play_sound(selected_audio,wait_for_complete_flag=True)

        tools.timer_ctrl(rm_define.timer_start)

        win = False

        while tools.timer_current() < 10:
            if vision_ctrl.check_condition(selected_pose):
                media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
                win = True
                         
        if win == False:
            shoot_one_lazer()
            shoot_one_lazer()
            shoot_one_lazer()   

        tools.timer_ctrl(rm_define.timer_reset)  
    

# While Loop game loop [NOT WORKING]  
#
# gameLoopCounter = -1

#     while True:
#         # Says Simon says each action in a loop
#         if gameLoopCounter < 0:
#             media_ctrl.play_sound(rm_define.media_custom_audio_2, wait_for_complete_flag=True)
#             gameLoopCounter += 1

#         selected_audio = random.choice(gesture_audios)
#         selected_index = gesture_audios.index(selected_audio)
#         selected_pose = gesture_poses[selected_index]
#         media_ctrl.play_sound(selected_audio)

#         tools.timer_ctrl(rm_define.timer_start)

#         # You likely don't need this nested loop; it can cause issues
#         while (gameLoopCounter == 0):
#             if vision_ctrl.check_condition(selected_pose):
#                 media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
#                 gameLoopCounter -= 1
#             else:
#                 if tools.timer_current() > 10:
#                     shoot_one_lazer()
#                     gameLoopCounter -= 1