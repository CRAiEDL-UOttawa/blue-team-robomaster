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

pid_PIDpitch = PIDCtrl()
pid_PIDyaw = PIDCtrl()
list_PersonList = RmList()
variable_X = 0
variable_Y = 0
variable_Post = 0
variable_W = 0
variable_H = 0

# Arrays of audio files corresponding to specific actions within our game and arrays containing those actions
claps_af = [rm_define.media_custom_audio_2, rm_define.media_custom_audio_1] 
claps = ['two_clap', 'three_clap'] 

vmarker_af = [rm_define.media_custom_audio_5,rm_define.media_custom_audio_8 , rm_define.media_custom_audio_9,rm_define.media_custom_audio_7]
vmarker = [3,3,5,5]

gesture_af = [rm_define.media_custom_audio_3, rm_define.media_custom_audio_4, rm_define.media_custom_audio_0]
gesture = ['capture', 'hands_up', 'hands_down']

intro_outro_audios = ["PUT NEXT PLAYER AUDIO HERE","PUT CONLUSION AUDIO 1 HERE","PUT CONCLUSION AUDIO 2 HERE"]
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
    
def alive_sound(x): # x -> amount of times you want the sad sound to play
      media_ctrl.play_sound(rm_define.media_sound_solmization_1E)
      media_ctrl.play_sound(rm_define.media_sound_solmization_1B)
      ## need to make this more evil

def angry_sound(x): # x -> amount of times you want the sad sound to play
      media_ctrl.play_sound(rm_define.media_sound_solmization_1E)
      media_ctrl.play_sound(rm_define.media_sound_solmization_1B)
      ## need to make this more evil

def scanning_sound(x): # x -> amount of times you want the scanning sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_scanning, wait_for_complete=True)

def attacked_sound(x): # x -> amount of times you want the attacked sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_attacked, wait_for_complete=True)

def turn_90_left():
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.rotate_with_speed(rm_define.anticlockwise,90)
    time.sleep(1)

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
        
        # If vmarker is detected
        if vision_ctrl.check_condition(gestureOrvmarker_cmd):
            
            detected = True
            
            # If Simon didn't say, player loses
            if simon_says:
                # led light changes to green
                set_led_color("green", "green", "solid")
                media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
            
            else:
                set_led_color("red", "red", "solid")
                detect_and_shoot_person()
                # Find the correct player and set them to 0 (dead)
                players[round_number%5]=0
                return 0

    # Simon did say... (lose)
    if simon_says and not detected:
        set_led_color("red", "red", "solid")
        detect_and_shoot_person()
        players[round_number%5]=0
        return 0
    
    # Timer ended, no vmarker detected
    # Simon didn't say... (win)
    elif not simon_says and not detected:
        set_led_color("green", "green", "solid")
        media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
    
    tools.timer_ctrl(rm_define.timer_reset)

# Where 'clap' is one of the several keys in 'actions_dict'
def detect_claps(clap, simon_says:bool, round_time,round_number):

    clap_cmd = actions_dict.get(clap)
    print(clap_cmd)
    detected = False
    
    # timer
    tools.timer_ctrl(rm_define.timer_start)

    while tools.timer_current() < round_time:

        # If specified clap is observed
        if media_ctrl.check_condition(clap_cmd):

            detected = True
            
            # If simon did not say, player loses
            if simon_says:
                # led light changes to orange
                set_led_color("green", "green", "solid")
                media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)

            else:
                print("lose loser")
                set_led_color("red", "red", "solid")
                detect_and_shoot_person()
                # Find the correct player and set them to 0 (dead)
                players[round_number%5]=0  
                return 0           
                
    # Simon did say... (lose)
    if simon_says and not detected:
        set_led_color("red", "red", "solid")
        detect_and_shoot_person()
        # Find the correct player and set them to 0 (dead)
        players[round_number%5]=0
        return 0
    
    # Timer ended, no clap detected
    # Simon didn't say... (win)
    elif not simon_says and not detected:
        # TODO - What occurs when player doesn't react and simon didn't say
        set_led_color("green", "green", "solid")
        media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
        

    tools.timer_ctrl(rm_define.timer_reset)

# TODO - finding best camera settings for identifying things in game area

# using colours defined in dictionary
def set_led_color(top_color, bottom_color, effect):
    # get RGB values for colors
    top_rgb = RGB.get(top_color)
    bottom_rgb = RGB.get(bottom_color)
    
    effect_color = LED_Effects.get(effect)
    
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
    

def detect_person():
        # init variables
    global variable_X       # Person identified X coordinate
    global variable_Y       # Person identified Y coordinate
    global variable_Post    # Error threshold value
    global variable_W       # Person identified Width variable (not sure exactly what this means, but we can temporarily use these to manage distance)
    global variable_H       # Person identified Height variable (same as width above)
    global list_PersonList  # List - stores info regarding the person identified (this is where we extract x, y, w, h)
    global pid_PIDpitch     # PID Controller for the gimbal pitch (vertical - Y coord)
    global pid_PIDyaw       # PID Controller for the gimbal yaw (horizontal - X coord)
    pid_PIDyaw.set_ctrl_params(150,5,8)
    pid_PIDpitch.set_ctrl_params(85,5,3)
    # Set error threshold (called the Post) to 0.07
    variable_Post = 0.07
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)

    while True:
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 100, 0, 100, rm_define.effect_always_on)
        led_ctrl.set_top_led(rm_define.armor_top_all, 100, 0, 100, rm_define.effect_always_on)

        # Set identified person data to PersonList list
        list_PersonList=RmList(vision_ctrl.get_people_detection_info())
        
        # If item 1 of list is equal to 1 - person identified
        if list_PersonList[1] == 1:
            # Set color to state - person identified
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 255, 255, rm_define.effect_always_on)
            led_ctrl.set_top_led(rm_define.armor_top_all, 255, 255, 255, rm_define.effect_always_on)
            
            # Set person related data to respective variables
            variable_X = list_PersonList[2] # Set person X value
            variable_Y = list_PersonList[3] # Set person Y value

            # Set error for PID controllers
            pid_PIDyaw.set_error(variable_X - 0.5)
            pid_PIDpitch.set_error(0.5 - variable_Y)

            # Set the gimbal speed to the PID output
            gimbal_ctrl.rotate_with_speed(pid_PIDyaw.get_output(),pid_PIDpitch.get_output())
            time.sleep(0.5)

            # If the gimbal is fixed on an individual, and x,y values are within the threshold
            if abs(variable_X - 0.5) <= variable_Post and abs(0.5 - variable_Y) <= variable_Post:
                print("person detected")
                gimbal_ctrl.rotate_with_speed(0, 0)  # Stop gimbal rotation
                gimbal_ctrl.stop()  # Ensure gimbal stops moving
                chassis_ctrl.stop()  # Ensure chassis stops moving
                break
        
        # If no person is identified, gimbal will rotate right until an individual is found
        # TODO - maybe implement a more effective way to search for a person
        else:
            gimbal_ctrl.rotate_with_speed(0,0)
            chassis_ctrl.stop()
            gimbal_ctrl.rotate(rm_define.gimbal_right)
            gimbal_ctrl.stop()  
            
def detect_and_shoot_person():
        # init variables
    global variable_X       # Person identified X coordinate
    global variable_Y       # Person identified Y coordinate
    global variable_Post    # Error threshold value
    global variable_W       # Person identified Width variable (not sure exactly what this means, but we can temporarily use these to manage distance)
    global variable_H       # Person identified Height variable (same as width above)
    global list_PersonList  # List - stores info regarding the person identified (this is where we extract x, y, w, h)
    global pid_PIDpitch     # PID Controller for the gimbal pitch (vertical - Y coord)
    global pid_PIDyaw       # PID Controller for the gimbal yaw (horizontal - X coord)
    pid_PIDyaw.set_ctrl_params(150,5,8)
    pid_PIDpitch.set_ctrl_params(85,5,3)
    # Set error threshold (called the Post) to 0.07
    variable_Post = 0.07
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow) 
    
    tools.timer_ctrl(rm_define.timer_reset)
    tools.timer_ctrl(rm_define.timer_start)

    while tools.timer_current() < 5:
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 100, 0, 100, rm_define.effect_always_on)
        led_ctrl.set_top_led(rm_define.armor_top_all, 100, 0, 100, rm_define.effect_always_on)

        # Set identified person data to PersonList list
        list_PersonList=RmList(vision_ctrl.get_people_detection_info())
        
        # If item 1 of list is equal to 1 - person identified
        if list_PersonList[1] == 1:
            # Set color to state - person identified
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 255, 255, rm_define.effect_always_on)
            led_ctrl.set_top_led(rm_define.armor_top_all, 255, 255, 255, rm_define.effect_always_on)
            
            # Set person related data to respective variables
            variable_X = list_PersonList[2] # Set person X value
            variable_Y = list_PersonList[3] # Set person Y value
            variable_W = list_PersonList[4] # Set person W value
            variable_H = list_PersonList[5] # Set person H value

            # Set error for PID controllers
            pid_PIDyaw.set_error(variable_X - 0.5)
            pid_PIDpitch.set_error(0.5 - variable_Y)

            # Set the gimbal speed to the PID output
            gimbal_ctrl.rotate_with_speed(pid_PIDyaw.get_output(),pid_PIDpitch.get_output())
            time.sleep(0.5)

            # If the gimbal is fixed on an individual, and x,y values are within the threshold
            if abs(variable_X - 0.5) <= variable_Post and abs(0.5 - variable_Y) <= variable_Post:
                print("person detected")
                if variable_W >= 0.1 and variable_H >= 0.8:
                    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 193, 0, rm_define.effect_always_on)
                    chassis_ctrl.stop()

                # Else, set chassis to translate to the player until the if statement above is executed
                else:
                    led_ctrl.set_top_led(rm_define.armor_top_all, 0, 127, 70, rm_define.effect_always_on)
                    chassis_ctrl.set_trans_speed(0.2) # WE SET SLOW SPEED FOR TESTING, THIS CAN BE BUMPED UP (PLEASE HAVE A BIG PLAY AREA IF YOU USE A HIGH VALUE)
                    chassis_ctrl.move(0)
                    led_ctrl.gun_led_on()
                    gun_ctrl.fire_once()
                    media_ctrl.play_sound(rm_define.media_sound_shoot)
                    led_ctrl.gun_led_off()                      
        
        # If no person is identified, gimbal will rotate right until an individual is found
        # TODO - maybe implement a more effective way to search for a person
        else:
            gimbal_ctrl.rotate_with_speed(0,0)
            chassis_ctrl.stop()
            gimbal_ctrl.rotate(rm_define.gimbal_right)  
    
    # Stop robot after shooting person
    gimbal_ctrl.rotate_with_speed(0, 0)  # Stop gimbal rotation
    gimbal_ctrl.stop()  # Ensure gimbal stops moving
    chassis_ctrl.stop()  # Ensure chassis stops moving
    tools.timer_ctrl(rm_define.timer_reset)

def intro_placement():
        # gimbal follow
        robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
        
        chassis_ctrl.set_trans_speed(0.5)
       
        # make robot 'come to life'
        # set robot pitch
        gimbal_ctrl.pitch_ctrl(5)
        alive_sound(1)
        gimbal_ctrl.pitch_ctrl(0)
        # add sound effect
        alive_sound(2)
        gimbal_ctrl.pitch_ctrl(10)
        set_led_color("magenta", "magenta", "pulsing")

        # move into game area
        chassis_ctrl.move_with_distance(0,2)

        # rotate left and move forward
        turn_90_left()
        media_ctrl.play_sound(rm_define.media_sound_solmization_1C)

        # recenter gimbal
        gimbal_ctrl.recenter()

# Outro functions
def drift_indefinitely():
    while True:
        chassis_ctrl.set_trans_speed(3.5)
        chassis_ctrl.set_rotate_speed(180)
        chassis_ctrl.move_with_time(0,0.5)
        shoot_one_lazer()
        chassis_ctrl.move_and_rotate(90, rm_define.anticlockwise)
        time.sleep(0.5)

def spin():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    chassis_ctrl.set_rotate_speed(500)
    gimbal_ctrl.set_rotate_speed(150)
    obliteration_colouring("red", "cyan", "green", "magenta", "purple", "orange")
    chassis_ctrl.rotate(rm_define.clockwise)
    for count in range(2):
        gimbal_ctrl.rotate(rm_define.gimbal_left)
        gimbal_ctrl.rotate(rm_define.gimbal_right)


# move to lights file as well
def obliteration_colouring(x1, x2, x3, x4, x5, x6):
    c1 = RGB.get(x1)
    c2 = RGB.get(x2)
    c3 = RGB.get(x3)
    c4 = RGB.get(x4)
    c5 = RGB.get(x5)
    c6 = RGB.get(x6)
    led_ctrl.set_top_led(rm_define.armor_top_left, c1[0], c1[1], c1[2], rm_define.effect_flash) # left gimbal
    led_ctrl.set_top_led(rm_define.armor_top_right, c2[0], c2[1], c2[2], rm_define.effect_flash)  # right gimbal

    led_ctrl.set_bottom_led(rm_define.armor_bottom_front, c3[0], c3[1], c3[2], rm_define.effect_flash) # front chassis
    led_ctrl.set_bottom_led(rm_define.armor_bottom_back, c4[0], c4[1], c4[2], rm_define.effect_flash) # rear chassis
    led_ctrl.set_bottom_led(rm_define.armor_bottom_left, c5[0], c5[1], c5[2], rm_define.effect_flash) # left chassis
    led_ctrl.set_bottom_led(rm_define.armor_bottom_right, c6[0], c6[1], c6[2], rm_define.effect_flash) # right chassis

def start():
    #(INTRO ADDED YESTERDAY)
    intro_placement()
    print('game start')
    # INTRO SCENE

    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)
    vision_ctrl.enable_detection(rm_define.vision_detection_pose)
    vision_ctrl.enable_detection(rm_define.vision_detection_people)
    gimbal_ctrl.rotate(rm_define.gimbal_up)


    print('begin game')
    # GAME LOOP
    
    
    for i in range(0,20):
        # Ask person to come forward
        # Currently playing note C
        
        # Change this to intro_outro_audios[0]
        media_ctrl.play_sound(rm_define.media_sound_solmization_1C)
        
        # Sleep for 5 seconds after asking for next player
        time.sleep(5)
        
        print(players)
        
        # Use camera to detect person and aim at them
        detect_person()
        # Stop gimbal and chassis from adjusting after detection
        gimbal_ctrl.stop()
        chassis_ctrl.stop()

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
            
        if i==15:
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

        gf = random.randint(0,1)  
        
        # Scan for action
        set_led_color(color, color, "scanning")    

        if gf==0:  # assuming this is part of a larger conditional structure
            selected_audio = random.choice(gesture_af)
            selected_index = gesture_af.index(selected_audio)
            selected_pose = gesture[selected_index]
            media_ctrl.play_sound(selected_audio, wait_for_complete_flag=True)
            detect_gesture_vmarker(selected_pose, simonSays, round_time,True,i)
        elif gf==2:
            selected_audio = random.choice(vmarker_af)
            selected_index = vmarker_af.index(selected_audio)
            selected_marker = vmarker[selected_index]
            media_ctrl.play_sound(selected_audio, wait_for_complete_flag=True)
            detect_gesture_vmarker(selected_marker, simonSays, round_time,False,i)
        elif gf==1:
            selected_audio = random.choice(claps_af)
            selected_index = claps_af.index(selected_audio)
            selected_clap = claps[selected_index]
            media_ctrl.play_sound(selected_audio, wait_for_complete_flag=True)
            detect_claps(selected_clap, simonSays, round_time,i)

        # EXIT SCENE (OUTRO ADDED YESTERDAY)
        if(players.count(1)==1):
            set_led_color("green", "green", "pulsing")
            scanning_sound(1)
            # Change this to intro_outro_audios[1]
            media_ctrl.play_sound(rm_define.media_custom_audio_1, wait_for_complete_flag=True)
            chassis_ctrl.move_with_distance(0, 0.5)
            armor_ctrl.set_hit_sensitivity(10)
            while True:
                if armor_ctrl.check_condition(rm_define.cond_armor_bottom_front_hit):
                    set_led_color("red", "red", "pulsing")
                    attacked_sound(1)
                    angry_sound(2)
                    tools.timer_ctrl(rm_define.timer_start)
                    while tools.timer_current() < 5:
                        spin()
                        # Change this to intro_outro_audios[2]
                        media_ctrl.play_sound(rm_define.media_custom_audio_2, wait_for_complete_flag=True)
                    tools.timer_ctrl(rm_define.timer_reset) 
                    while tools.timer_current() < 8: 
                        drift_indefinitely()
            

			
    
        
        
    
