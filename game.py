import random

def start():
	print('game start')
	# INTRO SCENE

	gamefunction = [detect_vmarker,detect_gesture]
	gestures = ['two_clap', 'three_clap', 'capture', 'hands_up', 'hands_down']
	vmarker = [2,3,5]
	

	# GAME LOOP
	
	
	for i in range(0,10):
	
		SimonSays = random.randint(0,1)

		if(SimonSays):
			media_ctrl.play_sound(rm_define.media_custom_audio_SIMONSAYS, wait_for_complete_flag=True)
		

		roundAction = random.choice(gamefunction)

		roundAction(,,)





		


	# EXIT SCENE
