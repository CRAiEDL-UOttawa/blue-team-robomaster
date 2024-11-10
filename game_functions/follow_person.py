pid_PIDpitch = PIDCtrl()
pid_PIDyaw = PIDCtrl()
list_PersonList = RmList()
variable_X = 0
variable_Y = 0
variable_Post = 0
def start():
    global variable_X
    global variable_Y
    global variable_Post
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 50, 0, rm_define.effect_breath)
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 50, 0, rm_define.effect_breath)
    vision_ctrl.enable_detection(rm_define.vision_detection_pose)
    vision_ctrl.enable_detection(rm_define.vision_detection_people)
    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)
    pid_PIDyaw.set_ctrl_params(200,0,10)
    pid_PIDpitch.set_ctrl_params(85,0,3)
    while True:
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 100, 0, 100, rm_define.effect_always_on)
        led_ctrl.set_top_led(rm_define.armor_top_all, 100, 0, 100, rm_define.effect_always_on)
        list_PersonList=RmList(vision_ctrl.get_people_detection_info())
        if list_PersonList[1] == 1:
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 255, 255, rm_define.effect_always_on)
            led_ctrl.set_top_led(rm_define.armor_top_all, 255, 255, 255, rm_define.effect_always_on)
            variable_X = list_PersonList[2]
            variable_Y = list_PersonList[3]
            pid_PIDyaw.set_error(variable_X - 0.5)
            pid_PIDpitch.set_error(0.5 - variable_Y)
            gimbal_ctrl.rotate_with_speed(pid_PIDyaw.get_output(),pid_PIDpitch.get_output())
            time.sleep(0.5)
            variable_Post = 0.05
            if abs(variable_X - 0.5) <= variable_Post and abs(0.5 - variable_X) <= variable_Post:
                chassis_ctrl.move(0)
                led_ctrl.gun_led_on()
                gun_ctrl.fire_once()
                media_ctrl.play_sound(rm_define.media_sound_shoot)
                led_ctrl.gun_led_off()
                time.sleep(1)
        else:
            gimbal_ctrl.rotate_with_speed(0,0)
            chassis_ctrl.stop()
            gimbal_ctrl.rotate(rm_define.gimbal_right)
            time.sleep(1)
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
def vision_recognized_pose_give_in(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    rmexit()
def vision_recognized_pose_victory(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    rmexit()
def chassis_impact_detection(msg):
    global variable_X
    global variable_Y
    global variable_Post
    global list_PersonList
    global pid_PIDpitch
    global pid_PIDyaw
    rmexit()
