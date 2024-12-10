"""
File: shooting.py
Author: Yasin, Vanisha, Michael
Date: 10/12/2024
Description: This script holds function for shooting lazers from the robomaster s1 gimbal 

PACKAGE_CONTENTS
    shoot_lazer(x)
    shoot_one_lazer()
"""
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

def shoot_one_lazer(): 
    # turn gun light on
    led_ctrl.gun_led_on()

    # fire lazer
    ir_blaster_ctrl.fire_once()

    # turn gun light off
    led_ctrl.gun_led_off()

    # play shoot sound once (audio.py)
    shoot_sound(1)
