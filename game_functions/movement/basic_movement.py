# Created functions for basic movements with some added light effects

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

# Method from audio.py
def shoot_sound(x): # x -> amount of times you want the shooting sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_shoot, wait_for_complete=True)

# Shoot lazer method
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

# From lights.py
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

# Make robots spin and 
def spin():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    chassis_ctrl.set_rotate_speed(500)
    gimbal_ctrl.set_rotate_speed(150)
    chassis_ctrl.rotate(rm_define.clockwise)
    time.sleep(2)
    for count in range(2):
        gimbal_ctrl.rotate(rm_define.gimbal_left)
        gimbal_ctrl.rotate(rm_define.gimbal_right)

def turn_180_right():
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.rotate_with_speed(rm_define.clockwise,180)
    time.sleep(1)

def turn_90_right():
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.rotate_with_speed(rm_define.clockwise,90)
    time.sleep(1)

def turn_180_left():
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.rotate_with_speed(rm_define.anticlockwise,180)
    time.sleep(1)

def back_and_forth_pacing():
        # gimbal follow
        robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
        
        chassis_ctrl.set_trans_speed(0.5)
       
        # make robot 'come to life'
        set_led_color("magenta", "magenta", rm_define.effect_breath) #check this to fix it

        # move into game area
        chassis_ctrl.move_with_distance(0,1)

        # rotate right and move forward
        turn_180_right()
        media_ctrl.play_sound(rm_define.media_custom_audio_0)
        chassis_ctrl.move_with_time(0,3)

        # recenter gimbal
        gimbal_ctrl.recenter()

        # rotate left and move forward 
        turn_180_left()
        chassis_ctrl.move_with_time(0,3)

        # rotate right and move forward 
        turn_180_right()
        set_led_color("red", "red", rm_define.effect_always_on) 
        chassis_ctrl.move_with_time(0,3)

        time.sleep(1)

        turn_180_left()
        shoot_lazer(1)
        turn_90_right()
        set_led_color("magenta", "magenta", rm_define.effect_breath)
        chassis_ctrl.move_with_time(0,2)

        turn_90_right()
        set_led_color("red", "red", rm_define.effect_always_on) 
        turn_90_right()
        
def start():
    # Start timer
    tools.timer_ctrl(rm_define.timer_start)
    back_and_forth_pacing()
    spin()
        
