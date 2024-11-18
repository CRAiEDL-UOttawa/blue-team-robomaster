pid_PIDpitch = PIDCtrl()
pid_PIDyaw = PIDCtrl()
list_PersonList = RmList()
variable_X = 0
variable_Y = 0
variable_Post = 0
variable_W = 0
variable_H = 0

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
    
    vision_ctrl.enable_detection(rm_define.vision_detection_people)
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
                return True
        
        # If no person is identified, gimbal will rotate right until an individual is found
        # TODO - maybe implement a more effective way to search for a person
        else:
            gimbal_ctrl.rotate_with_speed(0,0)
            chassis_ctrl.stop()
            gimbal_ctrl.rotate(rm_define.gimbal_right) 

def start():
    detect_person()