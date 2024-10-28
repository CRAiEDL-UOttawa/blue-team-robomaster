# CUSTOME AUDIO 1 = Simon Says
# CUSTOME AUDI0 2 = HANDS UP
# CUSTOME AUDIO 3 = Hands Down


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

def hands_down():
	vision_ctrl.enable_detection(rm_define.vision_detection_pose)
	gimbal_ctrl.rotate(rm_define.gimbal_up)
	media_ctrl.play_sound("CUSTOM AUDIO1")
	media_ctrl.play_sound("CUSTOM AUDIO3")
	tools.timer_ctrl(rm_define.timer_start)

	while True:
		if vision_ctrl.check_condition(rm_define.cond_recognized_pose_give_in):
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
	hands_up()
	#hands_down()