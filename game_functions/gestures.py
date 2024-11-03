import random

# CUSTOME AUDIO 3 = Simon Says
# CUSTOME AUDIO 2 = Take Photo
# CUSTOME AUDI0 1 = HANDS UP
# CUSTOME AUDIO 0 = Hands Down

rm_define.media_custom_audio_0
rm_define.media_custom_audio_1
rm_define.media_custom_audio_2

"rm_define.cond_recognized_pose_victory"
rm_define.cond_recognized_pose_give_in
rm_define.cond_recognized_pose_capture

gesture_poses = [rm_define.cond_recognized_pose_capture, rm_define.cond_recognized_pose_victory,rm_define.cond_recognized_pose_give_in]
gesture_audios = [rm_define.media_custom_audio_2,rm_define.media_custom_audio_1,rm_define.media_custom_audio_0]

# shoot lazer out
def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)
	

def hands_up():
	vision_ctrl.enable_detection(rm_define.vision_detection_pose)
	gimbal_ctrl.rotate(rm_define.gimbal_up)
	media_ctrl.play_sound("CUSTOM AUDIO1")
	media_ctrl.play_sound("CUSTOM AUDIO2")
	tools.timer_ctrl(rm_define.timer_start)

	while True:
		if vision_ctrl.check_condition(rm_define.cond_recognized_pose_victory):
			media_ctrl.play_sound("CUSTOM AUDIO3")
			rmexit()
		else:
			if tools.timer_current() > 10:
				gun_ctrl.fire_continuous()
				for count in range(5):
					ir_blaster_ctrl.fire_continuous()
					time.sleep(1)
				rmexit()
	

def start():
	led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 50, 0, rm_define.effect_always_on)
	vision_ctrl.enable_detection(rm_define.vision_detection_pose)
	gimbal_ctrl.rotate(rm_define.gimbal_up)

	gameLoopCounter = -1

	while True:

		# Says simon says each action in a loop
		if(gameLoopCounter<0):
			media_ctrl.play_sound(rm_define.media_custom_audio_3,wait_for_complete_flag=True)
			gameLoopCounter+=1

		selected_audio = random.choice(gesture_audios)
		selected_pose = gesture_poses.index(selected_audio)
		media_ctrl.play_sound(selected_audio)

		tools.timer_ctrl(rm_define.timer_start)

		if vision_ctrl.check_condition(selected_pose):			
			media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
			gameLoopCounter-=1
		else:
			if tools.timer_current() > 10:
				shoot_one_lazer()
				gameLoopCounter-=1		