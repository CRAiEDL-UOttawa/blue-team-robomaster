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
        chassis_ctrl.set_trans_speed(3.5)
        chassis_ctrl.set_rotate_speed(180)
        chassis_ctrl.move_with_time(0,0.5)
        shoot_lazer(1)
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

def set_led_color(top_color, bottom_color, effect):
    # get RGB values for colors
    top_rgb = RGB.get(top_color)
    bottom_rgb = RGB.get(bottom_color)
    
    # check if both colors exist in dictionary
    if top_rgb is None:
        raise ValueError(f"Top color '{top_color}' not found.")
    if bottom_rgb is None:
        raise ValueError(f"Bottom color '{bottom_color}' not found.")
    
    # set the top and bottom LEDs 
    led_ctrl.set_top_led(rm_define.armor_top_all, top_rgb[0], top_rgb[1], top_rgb[2], effect)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, bottom_rgb[0], bottom_rgb[1], bottom_rgb[2], effect)

def start():
    set_led_color("green", "green", rm_define.effect_breath)
    scanning_sound(1)
    media_ctrl.play_sound(rm_define.media_custom_audio_1, wait_for_complete_flag=True)
    chassis_ctrl.move_with_distance(0, 0.5)
    armor_ctrl.set_hit_sensitivity(10)

    while True:
        if armor_ctrl.check_condition(rm_define.cond_armor_bottom_front_hit):
            set_led_color("red", "red", rm_define.effect_breath)
            attacked_sound(1)
            angry_sound(2)
            
            tools.timer_ctrl(rm_define.timer_start)
            
            while tools.timer_current() < 5:
                spin()
                media_ctrl.play_sound(rm_define.media_custom_audio_2, wait_for_complete_flag=True)
            

            tools.timer_ctrl(rm_define.timer_reset) 

            # movement of robot going crazy
            while tools.timer_current() < 8: 
                drift_indefinitely()
