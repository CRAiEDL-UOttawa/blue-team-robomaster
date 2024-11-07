def shoot_lazer(x): # x -> amount of times you want the countdown sound to play
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
