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

def shoot_sound(x): # x -> amount of times you want the shooting sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_shoot, wait_for_complete=True)

def shoot_lazer(x): # x -> amount of times you want to shoot
    for count in range(x):
        # turn gun light on
        led_ctrl.gun_led_on()

        # fire lazer
        ir_blaster_ctrl.fire_once()

        # turn gun light off
        led_ctrl.gun_led_off()

        # play shoot sound once (audio.py)
        shoot_sound(1)

def drift_indefinitely():
    while True:
        chassis_ctrl.set_trans_speed(1.5)
        chassis_ctrl.set_rotate_speed(180)
        chassis_ctrl.move_with_time(0,0.5)
        shoot_lazer(1)
        chassis_ctrl.move_and_rotate(90, rm_define.anticlockwise)
        time.sleep(1)

def spin():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    chassis_ctrl.set_rotate_speed(500)
    gimbal_ctrl.set_rotate_speed(150)
    chassis_ctrl.rotate(rm_define.clockwise)
    for count in range(2):
        gimbal_ctrl.rotate(rm_define.gimbal_left)
        gimbal_ctrl.rotate(rm_define.gimbal_right)


def start():
    media_ctrl.play_sound(rm_define.media_custom_audio_0, wait_for_complete_flag=True)
    scanning_sound(1)
    armor_ctrl.set_hit_sensitivity(9)

    while True:
        if armor_ctrl.check_condition(rm_define.cond_armor_bottom_front_hit):
    
    
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 50, 0, rm_define.effect_always_on)
            attacked_sound(1)
            angry_sound(1)
            
            tools.timer_ctrl(rm_define.timer_start)
            
            while tools.timer_current() < 5:
                spin()
                media_ctrl.play_sound(rm_define.media_custom_audio_1, wait_for_complete_flag=True)
            

            tools.timer_ctrl(rm_define.timer_reset) 

            # movement of robot going crazy
            while tools.timer_current() < 8:
                drift_indefinitely()
