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


def alive_sound(x): # x -> amount of times you want the sad sound to play
      media_ctrl.play_sound(rm_define.media_sound_solmization_1E)
      media_ctrl.play_sound(rm_define.media_sound_solmization_1B)
      ## need to make this more evil

def turn_90_left():
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.rotate_with_speed(rm_define.anticlockwise,90)
    time.sleep(1)


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
        set_led_color("magenta", "magenta", rm_define.effect_breath) #check this to fix it

        # move into game area
        chassis_ctrl.move_with_distance(0,2)

        # rotate left and move forward
        turn_90_left()
        media_ctrl.play_sound(rm_define.media_sound_solmization_1C)

        # recenter gimbal
        gimbal_ctrl.recenter()
        
def start():
    intro_placement()
        
