# initialize variables
pid_PIDpitch = PIDCtrl()    # PID controller for gimbal pitch
pid_PIDyaw = PIDCtrl()      # PID contorller for gimbal yaw
list_PersonList = RmList()  # Person identification list    
variable_X = 0              # X value in gimbal cartesian view
variable_Y = 0              # Y value in gimbal cartesian view 
variable_Post = 0           # Maximum error

def start():
    global variable_X
    global variable_Y
    global variable_Post
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw

    # Initialize chassis follow
    # Gimbal leads by identifying
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)

    # Initialize gesture detections for testing
    vision_ctrl.enable_detection(rm_define.vision_detection_pose)
    vision_ctrl.enable_detection(rm_define.vision_detection_people)
    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)

    # Colors to identify robot just started
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 50, 0, rm_define.effect_breath)
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 50, 0, rm_define.effect_breath)

    # Initializing PID paramters (Kp, Ki, Kd)
    # TODO - Looking to refine these params to create a more accurate reading
    pid_PIDyaw.set_ctrl_params(200,0,10)        # 200 Kp, 0 Ki, 10 Kd
    pid_PIDpitch.set_ctrl_params(85,0,3)        # 85 Kp, 0 Ki, 3 Kd

    while True:
        # Robot hasn't identified an individual, in the loop
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 100, 0, 100, rm_define.effect_always_on)
        led_ctrl.set_top_led(rm_define.armor_top_all, 100, 0, 100, rm_define.effect_always_on)

        # When person is detected, store vision info in list
        list_PersonList=RmList(vision_ctrl.get_people_detection_info())
        print(list_PersonList)
        if list_PersonList[1] == 1:
            # Robot has identified an individual
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 255, 255, rm_define.effect_always_on)
            led_ctrl.set_top_led(rm_define.armor_top_all, 255, 255, 255, rm_define.effect_always_on)

            # Variable X is stored as the 3rd index in PersonList
            variable_X = list_PersonList[2]

            # Variable Y is stored as the 4th index in PersonList
            variable_Y = list_PersonList[3]

            # Set PID yaw error
            pid_PIDyaw.set_error(variable_X - 0.5)

            # Set PID pitch error
            pid_PIDpitch.set_error(0.5 - variable_Y)

            # Adjust gimbal based on PID adjusted outputs
            gimbal_ctrl.rotate_with_speed(pid_PIDyaw.get_output(),pid_PIDpitch.get_output())
            time.sleep(0.5)

            # Set adjusted error
            variable_Post = 0.05

            # When Person is identified, and vision is within error, move towards person
            if abs(variable_X - 0.5) <= variable_Post and abs(0.5 - variable_Y) <= variable_Post:
                chassis_ctrl.move(0)
                led_ctrl.gun_led_on()
                gun_ctrl.fire_once()
                media_ctrl.play_sound(rm_define.media_sound_shoot)
                led_ctrl.gun_led_off()
                time.sleep(1)
        
        # If no person identified, don't move and rotate gimbal around until it finds someone
        else:
            gimbal_ctrl.rotate_with_speed(0,0)
            chassis_ctrl.stop()
            gimbal_ctrl.rotate(rm_define.gimbal_right)
            time.sleep(1)

# If person claps twice, end program (FOR TESTING)
def sound_recognized_applause_twice(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 0, rm_define.effect_always_on)
    rmexit()

# If person does inverted V, end program (FOR TESTING)
def vision_recognized_pose_give_in(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    rmexit()

# If person does V, end program (FOR TESTING)
def vision_recognized_pose_victory(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    rmexit()

# If chasis bumps into something, end program (FOR TESTING)
def chassis_impact_detection(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    rmexit()
