# November 17th, 2024
# Yasin Vanisha Michael workshopped the previous existing follow_person code
# Made adjustments to code for better PID params
# Also leveraged width/height variables for robot to stop at a fairly good distance between identified person
# Looking to outfit this code using vision markers to test for accuracy...

pid_PIDpitch = PIDCtrl()
pid_PIDyaw = PIDCtrl()
list_PersonList = RmList()
variable_X = 0
variable_Y = 0
variable_Post = 0
variable_W = 0
variable_H = 0
def start():
    # init variables
    global variable_X       # Person identified X coordinate
    global variable_Y       # Person identified Y coordinate
    global variable_Post    # Error threshold value
    global variable_W       # Person identified Width variable (not sure exactly what this means, but we can temporarily use these to manage distance)
    global variable_H       # Person identified Height variable (same as width above)
    global list_PersonList  # List - stores info regarding the person identified (this is where we extract x, y, w, h)
    global pid_PIDpitch     # PID Controller for the gimbal pitch (vertical - Y coord)
    global pid_PIDyaw       # PID Controller for the gimbal yaw (horizontal - X coord)

    # Init robot state
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)            # Gimbal lead mode
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.enable_detection(rm_define.vision_detection_pose)          
    vision_ctrl.enable_detection(rm_define.vision_detection_people)
    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)

    # Debug colors - identifies which state we're in (robot hasn't identified anyone)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 50, 0, rm_define.effect_breath)
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 50, 0, rm_define.effect_breath)

    # Setting PID controller parameters for the pitch and Yaw
    # TODO - Need to continue playing with these coefficients to find something that works best

    # Set YAW PID Controller coefficients to: 150 kP, 5 kI (may not be neccessary, still investigating), 8 kD
    pid_PIDyaw.set_ctrl_params(150,5,8)

    # Set Pitch PID Controller coefficients to: 85 kP, 5 kI (may not be necessary, still investigating), 3 kD
    pid_PIDpitch.set_ctrl_params(85,5,3)

    # TODO - play around with a threshold value that has good results
    # So far, values in the range 0.05-0.07 have proven effective

    # Set error threshold (called the Post) to 0.07
    variable_Post = 0.07

    while True:
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 100, 0, 100, rm_define.effect_always_on)
        led_ctrl.set_top_led(rm_define.armor_top_all, 100, 0, 100, rm_define.effect_always_on)

        # Set identified person data to PersonList list
        list_PersonList=RmList(vision_ctrl.get_marker_detection_info())

        # If item 1 of list is equal to 1 - person identified
        if list_PersonList[1] == 1:
            # Set color to state - person identified
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 255, 255, rm_define.effect_always_on)
            led_ctrl.set_top_led(rm_define.armor_top_all, 255, 255, 255, rm_define.effect_always_on)
            
            # Set person related data to respective variables
            variable_X = list_PersonList[3] # Set person X value
            variable_Y = list_PersonList[4] # Set person Y value
            variable_W = list_PersonList[5] # Set person W value
            variable_H = list_PersonList[6] # Set person H value

            # Set error for PID controllers
            pid_PIDyaw.set_error(variable_X - 0.5)
            pid_PIDpitch.set_error(0.5 - variable_Y)

            # Set the gimbal speed to the PID output
            gimbal_ctrl.rotate_with_speed(pid_PIDyaw.get_output(),pid_PIDpitch.get_output())
            time.sleep(0.5)

            # If the gimbal is fixed on an individual, and x,y values are within the threshold
            if abs(variable_X - 0.5) <= variable_Post and abs(0.5 - variable_Y) <= variable_Post:

                # If the person identified has a width value of 0.1 and height value of 0.65, stop the robot from translating
                if variable_W >= 0.1 and variable_H >= 0.65:
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
                    time.sleep(1)
        
        # If no person is identified, gimbal will rotate right until an individual is found
        # TODO - maybe implement a more effective way to search for a person
        else:
            gimbal_ctrl.rotate_with_speed(0,0)
            chassis_ctrl.stop()
            gimbal_ctrl.rotate(rm_define.gimbal_right)


### Helper functions - These terminate the program once they're executed
def sound_recognized_applause_twice(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global variable_W
    global variable_H
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 0, rm_define.effect_always_on)
    rmexit()

def vision_recognized_pose_give_in(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global variable_W
    global variable_H
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    rmexit()

def vision_recognized_pose_victory(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global variable_W
    global variable_H
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    rmexit()

def chassis_impact_detection(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global variable_W
    global variable_H
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    rmexit()
