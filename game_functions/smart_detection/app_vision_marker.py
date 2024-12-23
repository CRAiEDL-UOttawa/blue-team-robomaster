"""
File: audio.py
Author: Yasin, Vanisha, Michael
Date: 10/12/2024
Description: This script contains funtions for the robot's basic audios within our game
This script contains game logic for detecting a randomly selected vision nmarker within a given time range,
when vision marker is randomly selected, make function call
"""

# Dictionary that holds vision marker object and corresponding audio (command that says to pick up corresponding card)
markers_num_dict = {
    rm_define.cond_recognized_marker_number_two: rm_define.media_custom_audio_4, 
    rm_define.cond_recognized_marker_number_three: rm_define.media_custom_audio_0, 
    rm_define.cond_recognized_marker_number_five: rm_define.media_custom_audio_3, 
}

def shoot_lazer(x): # x -> amount of times you want to shoot
    for count in range(x):
        # Turn gun light on
        led_ctrl.gun_led_on()

        # Fire lazer
        ir_blaster_ctrl.fire_once()

        # Turn gun light off
        led_ctrl.gun_led_off()

        # Play shoot sound once 
        shoot_sound(1)

def success_sound(x): # x -> amount of times you want the success sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)

def start():
    # Vision detection enabled
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 50, 0, rm_define.effect_always_on)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)

    # Max distance 
    vision_ctrl.set_marker_detection_distance(3)

    # Constantly running
    while True: 
        # Select one key in dict
        marker = random.choice(list(markers_num_dict.keys()))

        # Play corresponding audio
        audio = markers_num_dict[marker]
        media_ctrl.play_sound(audio, wait_for_complete_flag=True)

        # Timer starts
        tools.timer_ctrl(rm_define.timer_start)

        win = False

        # Player has 10 seconds to pick up vision card
        while tools.timer_current() < 10:
            
            # If the right vision marker is detected
            if vision_ctrl.check_condition(marker):
                # LED light changes to orange
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 161, 255, 69, rm_define.effect_always_on)
                success_sound(1) # Play success sound
                win = True
             
            if win == False: # Player did not pick up the right card/any card and 10 seconds are up 
                # LED light changes to red
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
                shoot_lazer(5) # Shoot 5 times

        # Reset timer
        tools.timer_ctrl(rm_define.timer_reset) 
