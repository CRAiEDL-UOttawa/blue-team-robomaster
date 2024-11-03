import random

def start():
	print('game start')
	# INTRO SCENE



	# GAME LOOP
	gameLoopCounter = -1

	while True:

		# Says simon says each action in a loop
		if(gameLoopCounter<0):
			media_ctrl.play_sound("SIMON SAYS AUDIO",wait_for_complete_flag=True)
			gameLoopCounter+=1

		# CODE TO RANDOMLY SELECT
		selected_audio = []
		selected_action = []
		media_ctrl.play_sound(selected_audio)

		# Start the timer
		tools.timer_ctrl(rm_define.timer_start)

		if vision_ctrl.check_condition(selected_action):			
			media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
			gameLoopCounter-=1
		else:
			if tools.timer_current() > 10:
				shoot_one_lazer()
				gameLoopCounter-=1		


	# EXIT SCENE
