# Code done to test vision markers

# Shoot lazer method
def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)

def start():
    # Clap detection enabled
    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)
    while True:
        # Clap command audio
        media_ctrl.play_sound(audio, wait_for_complete_flag=True)

        # Timer
        tools.timer_ctrl(rm_define.timer_start)
        
        # If player clapping 3 times is detected
        if media_ctrl.check_condition(rm_define.cond_sound_recognized_applause_thrice):
            # LED light changes to orange
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 161, 255, 69, rm_define.effect_always_on)
            media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
            
            # Robot moves forward by 1 meter
            chassis_ctrl.move_with_distance(0,1)

        else:
            if tools.timer_current() > 10: # Player did not clap correctly/not detected and 10 seconds are up 
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
            for count in range(5):
                shoot_one_lazer() # Shoot 5 times
            rmexit()