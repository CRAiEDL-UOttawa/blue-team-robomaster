import random

# Arrays of audio files corresponding to specific actions within our game and arrays containing those actions
claps_af = [rm_define.media_custom_audio_5, rm_define.media_custom_audio_6] 
claps = ['two_clap', 'three_clap'] 

vmarker_af = [rm_define.media_custom_audio_7,rm_define.media_custom_audio_4 , rm_define.media_custom_audio_8]
vmarker = [2,3,5]

gesture_af = [rm_define.media_custom_audio_3, rm_define.media_custom_audio_1, rm_define.media_custom_audio_0]
gesture = ['capture', 'hands_up', 'hands_down']

# Dictionary makes command calls easier
actions_dict = {
    'two_clap': rm_define.cond_sound_recognized_applause_twice,
    'three_clap': rm_define.cond_sound_recognized_applause_thrice,
    'capture': rm_define.cond_recognized_pose_capture,
    'hands_up': rm_define.cond_recognized_pose_victory, 
    'hands_down': rm_define.cond_recognized_pose_give_in,
    2: rm_define.cond_recognized_marker_number_two,
    3: rm_define.cond_recognized_marker_number_three, 
    5: rm_define.cond_recognized_marker_number_five
}
        


def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)

def detect_gesture_vmarker(action, simon_says:bool, round_time):
    # Set camera exposure to low for better detection
    media_ctrl.exposure_value_update(rm_define.exposure_value_small)

    # Get robomaster call from dict
    gestureOrvmarker_cmd = actions_dict.get(action)

    # timer
    tools.timer_ctrl(rm_define.timer_start)

    while tools.timer_current() < round_time:

        # If vmarker is detected
        if vision_ctrl.check_condition(gestureOrvmarker_cmd):

            # If Simon didn't say, player loses
            if simon_says:
                # led light changes to green
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 0, 255, 0, rm_define.effect_always_on)
                media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
                # robot moves forward by 1 meter
            
            else:
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
                shoot_one_lazer()
    

    # Timer ended, no vmarker detected
    # Simon didn't say... (win)
    if tools.timer_current() > 10 & (not simon_says):
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 0, 255, 0, rm_define.effect_always_on)

    # Simon did say... (lose)
    else:
        
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
        # TODO - What occurs when vmarker not detected and simon didn't say
        shoot_one_lazer()
    
    tools.timer_ctrl(rm_define.timer_reset)

# Where 'clap' is one of the several keys in 'actions_dict'
def detect_claps(clap, simon_says:bool, round_time):

    clap_cmd = actions_dict.get(clap)

    # timer
    tools.timer_ctrl(rm_define.timer_start)

    while tools.timer_current() < round_time:

        # If specified clap is observed
        if media_ctrl.check_condition(clap_cmd):

            # If simon did not say, player loses
            if simon_says:
                # led light changes to orange
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 0, 255, 0, rm_define.effect_always_on)
                media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
                # robot moves forward by 1 meter
                chassis_ctrl.move_with_distance(0,1)
                # put audio here
                print('YAY') 

            else:
                print("lose loser")
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
                shoot_one_lazer()

    # Timer ended, no clap detected
    # Simon didn't say... (win)
    if tools.timer_current() > 10 & (not simon_says):
        # TODO - What occurs when player doesn't react and simon didn't say
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 0, 255, 0, rm_define.effect_always_on)
        print('huge win')
        
    
    # Simon did say... (lose)
    else:
        print('you lose')
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
        shoot_one_lazer()


    tools.timer_ctrl(rm_define.timer_reset)

# TODO - finding best camera settings for identifying things in game area

def start():
    print('game start')
    # INTRO SCENE

    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.enable_detection(rm_define.vision_detection_pose)

    print('begin game')
    # GAME LOOP
    
    
    for i in range(0,10):
    
        simonSays = random.randint(0,1)

        if simonSays:
            media_ctrl.play_sound(rm_define.media_custom_audio_2, wait_for_complete_flag=True)
        

        gf = random.randint(0,2)      

        if gf==0:  # assuming this is part of a larger conditional structure
            selected_audio = random.choice(gesture_af)
            selected_index = gesture_af.index(selected_audio)
            selected_pose = gesture[selected_index]
            media_ctrl.play_sound(selected_audio, wait_for_complete_flag=True)
            detect_gesture_vmarker(selected_pose, simonSays, 10)
        elif gf==1:
            selected_audio = random.choice(vmarker_af)
            selected_index = vmarker_af.index(selected_audio)
            selected_marker = vmarker[selected_index]
            media_ctrl.play_sound(selected_audio, wait_for_complete_flag=True)
            detect_gesture_vmarker(selected_marker, simonSays, 10)
        else:
            selected_audio = random.choice(claps_af)
            selected_index = claps_af.index(selected_audio)
            selected_clap = claps[selected_index]
            media_ctrl.play_sound(selected_audio, wait_for_complete_flag=True)
            detect_claps(selected_clap, simonSays, 10)

            
          
        





        


    # EXIT SCENE
