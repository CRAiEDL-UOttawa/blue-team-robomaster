import random

def start():
	print('game start')
	# INTRO SCENE

	gamefunction = [detect_vmarker,detect_gesture]


	# GAME LOOP
	
	
	for i in range(0,10):
	
		SimonSays = random.randint(0,1)
		if(SimonSays):
			media_ctrl.play_sound(rm_define.media_custom_audio_SIMONSAYS, wait_for_complete_flag=True)
		

		#random.choice(gamefunction)
		


	# EXIT SCENE
