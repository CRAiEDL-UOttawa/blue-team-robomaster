import random

# Dictionary of RGB colors
RGB = {
    "red": [255,0,0],
    "yellow": [255,255,0],
    "blue": [0,0,255],
    "green": [0,255,0],
    "pink": [255,0,150],
    "magenta": [224,0,255],
    "purple": [100,0,100],
    "blue": [36,103,255],
    "cyan": [69,215,255],
    "lime": [161,255,69],
    "yellow": [255,193,0],
    "orange": [255,50,0],
    "white": [255,255,255]
}

LED_Effects = {
    'pulsing': 2,
    'scanning': 4,
    'flashing': 3,
    'solid': 0,
    'off': 1
}

# Arrays of audio files corresponding to specific actions within our game and arrays containing those actions
claps_af = [rm_define.media_custom_audio_2, rm_define.media_custom_audio_1] 
claps = ['two_clap', 'three_clap'] 

vmarker_af = [rm_define.media_custom_audio_5,rm_define.media_custom_audio_8 , rm_define.media_custom_audio_9,rm_define.media_custom_audio_7]
vmarker = [3,3,5,5]

gesture_af = [rm_define.media_custom_audio_3, rm_define.media_custom_audio_4, rm_define.media_custom_audio_0]
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

# Initialize array of players
# 1 -> PLAYER ALIVE
# 0 -> PLAYER DEAD
players = [1,1,1,1,1]

def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)

def detect_gesture_vmarker(action, simon_says:bool, round_time,isGesture,round_number):
    # Set camera exposure to low for better detection
    
    if(isGesture):
        media_ctrl.exposure_value_update(rm_define.exposure_value_medium)
    else:
        media_ctrl.exposure_value_update(rm_define.exposure_value_small)

    # Get robomaster call from dict
    gestureOrvmarker_cmd = actions_dict.get(action)
    print(gestureOrvmarker_cmd)
    
    # Flag that indicates vision detection
    detected = False
    
    # timer
    tools.timer_ctrl(rm_define.timer_start)

    while tools.timer_current() < round_time:

        detected = True
        
        # If vmarker is detected
        if vision_ctrl.check_condition(gestureOrvmarker_cmd):

            # If Simon didn't say, player loses
            if simon_says:
                # led light changes to green
                set_led_color("green", "green", "solid")
                media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
            
            else:
                set_led_color("red", "red", "solid")
                shoot_one_lazer()
                # Find the correct player and set them to 0 (dead)
                players[round_number%5]=0
    

    # Timer ended, no vmarker detected
    # Simon didn't say... (win)
    if not simon_says and not detected:
        set_led_color("green", "green", "solid")
        media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)

    # Simon did say... (lose)
    elif simon_says and not detected:
        set_led_color("red", "red", "solid")
        shoot_one_lazer()
        players[round_number%5]=0
    
    tools.timer_ctrl(rm_define.timer_reset)

# Where 'clap' is one of the several keys in 'actions_dict'
def detect_claps(clap, simon_says:bool, round_time,round_number):

    clap_cmd = actions_dict.get(clap)
    print(clap_cmd)

    detected = False
    
    # timer
    tools.timer_ctrl(rm_define.timer_start)

    while tools.timer_current() < round_time:

        detected = True
        
        # If specified clap is observed
        if media_ctrl.check_condition(clap_cmd):

            # If simon did not say, player loses
            if simon_says:
                # led light changes to orange
                set_led_color("green", "green", "solid")
                media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)

            else:
                print("lose loser")
                set_led_color("red", "red", "solid")
                shoot_one_lazer()
                # Find the correct player and set them to 0 (dead)
                players[round_number%5]=0  
                
                

    # Timer ended, no clap detected
    # Simon didn't say... (win)
    if not simon_says and not detected:
        # TODO - What occurs when player doesn't react and simon didn't say
        set_led_color("green", "green", "solid")
        media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
        
    
    # Simon did say... (lose)
    elif simon_says and not detected:
        set_led_color("red", "red", "solid")
        shoot_one_lazer()
        # Find the correct player and set them to 0 (dead)
        players[round_number%5]=0

    tools.timer_ctrl(rm_define.timer_reset)

# TODO - finding best camera settings for identifying things in game area

# using colours defined in dictionary
def set_led_color(top_color, bottom_color, effect):
    # get RGB values for colors
    top_rgb = RGB.get(top_color)
    bottom_rgb = RGB.get(bottom_color)
    
    effect_color = LED_Effects.get(effect)
    print(actions_dict.get('two_clap'))
    print(effect_color)
    print(top_rgb)
    
    # check if both colors exist in dictionary
    if top_rgb is None:
        raise ValueError(f"Top color '{top_color}' not found.")
    if bottom_rgb is None:
        raise ValueError(f"Bottom color '{bottom_color}' not found.")
    
    if effect=="scanning":
        led_ctrl.set_top_led(rm_define.armor_top_all, top_rgb[0], top_rgb[1], top_rgb[2], effect_color)
    else:
        # set the top and bottom LEDs 
        led_ctrl.set_top_led(rm_define.armor_top_all, top_rgb[0], top_rgb[1], top_rgb[2], effect_color)
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, bottom_rgb[0], bottom_rgb[1], bottom_rgb[2], effect_color)


# using user's 2 arrays
def set_led_colors_dif(top_rgb, bottom_rgb, effect):
    # check each array has three values
    if len(top_rgb) != 3 or len(bottom_rgb) != 3:
        raise ValueError("Each array should contain exactly three elements: [x1, x2, x3]")
    
    top_x1, top_x2, top_x3 = top_rgb
    bottom_x1, bottom_x2, bottom_x3 = bottom_rgb
    
    led_ctrl.set_top_led(rm_define.armor_top_all, top_x1, top_x2, top_x3, effect)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, bottom_x1, bottom_x2, bottom_x3, effect)
    
    

def start():
    print('game start')
    # INTRO SCENE

    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.enable_detection(rm_define.vision_detection_pose)
    gimbal_ctrl.rotate(rm_define.gimbal_up)

    print('begin game')
    # GAME LOOP
    
    
    for i in range(0,20):
        
        # Play audio to call up next player
        media_ctrl.play_sound(rm_define.media_custom_audio_0, wait_for_complete_flag=True)
    
        simonSays = random.randint(0,1)
        print('starting level 1')
        level = 1
        color = "yellow"
        round_time = 15
        
        if i==10:
            print("starting level 2")
            level=2
            color = "orange"
            round_time = 10
            
        if i==5:
            print("starting level 3")
            level=3
            color = "red"
            round_time = 5

        if simonSays:
            
            if level==1:
                set_led_color("white", "white", "pulsing")
                media_ctrl.play_sound(rm_define.media_custom_audio_6, wait_for_complete_flag=True)
            elif level==2:
                set_led_color("cyan", "cyan", "pulsing")
                media_ctrl.play_sound(rm_define.media_custom_audio_6, wait_for_complete_flag=True)
            elif level==3:
                set_led_color("purple", "purple", "pulsing")
                media_ctrl.play_sound(rm_define.media_custom_audio_6, wait_for_complete_flag=True)

        gf = random.randint(0,2)  
        
        # Scan for action
        set_led_color(color, color, "scanning")    

        if gf==0:  # assuming this is part of a larger conditional structure
            selected_audio = random.choice(gesture_af)
            selected_index = gesture_af.index(selected_audio)
            selected_pose = gesture[selected_index]
            media_ctrl.play_sound(selected_audio, wait_for_complete_flag=True)
            detect_gesture_vmarker(selected_pose, simonSays, round_time,True,i)
        elif gf==1:
            selected_audio = random.choice(vmarker_af)
            selected_index = vmarker_af.index(selected_audio)
            selected_marker = vmarker[selected_index]
            media_ctrl.play_sound(selected_audio, wait_for_complete_flag=True)
            detect_gesture_vmarker(selected_marker, simonSays, round_time,False,i)
        else:
            selected_audio = random.choice(claps_af)
            selected_index = claps_af.index(selected_audio)
            selected_clap = claps[selected_index]
            media_ctrl.play_sound(selected_audio, wait_for_complete_flag=True)
            detect_claps(selected_clap, simonSays, round_time,i)

        # EXIT SCENE
        if(players.count(1)==1):
            # High five function and conclusion
            print()
        
        
    
