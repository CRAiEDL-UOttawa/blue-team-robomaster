# Created functions for sound effects

def countdown_sound(x): # x -> amount of times you want the countdown sound to play
    for count in range(x):
        media_ctrl.play_sound(rm_define.media_sound_count_down, wait_for_complete=True)

def scanning_sound(x): # x -> amount of times you want the scanning sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_scanning, wait_for_complete=True)

def attacked_sound(x): # x -> amount of times you want the attacked sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_attacked, wait_for_complete=True)

def shoot_sound(x): # x -> amount of times you want the shooting sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_shoot, wait_for_complete=True)

def success_sound(x): # x -> amount of times you want the success sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)

def rotate_sound(x): # x -> amount of times you want the rotate sound to play
        for count in range(x):
            media_ctrl.play_sound(rm_define.media_sound_gimbal_rotate, wait_for_complete=True)
    
def happy_sound(x): # x -> amount of times you want the happy sound to play
      media_ctrl.play_sound(rm_define.media_sound_solmization_2G)
      media_ctrl.play_sound(rm_define.media_sound_solmization_2A)
      media_ctrl.play_sound(rm_define.media_sound_solmization_2B)
      media_ctrl.play_sound(rm_define.media_sound_solmization_3C)

def angry_sound(x): # x -> amount of times you want the sad sound to play
      media_ctrl.play_sound(rm_define.media_sound_solmization_1E)
      media_ctrl.play_sound(rm_define.media_sound_solmization_1B)

# Different level sounds in our game
def l1():
      media_ctrl.play_sound(rm_define.media_sound_solmization_2C, wait_for_complete=True)
      media_ctrl.play_sound(rm_define.media_sound_solmization_2CSharp, wait_for_complete=True)
      media_ctrl.play_sound(rm_define.media_sound_solmization_2C, wait_for_complete=True)

def l2():
      media_ctrl.play_sound(rm_define.media_sound_solmization_1G, wait_for_complete=True)
      media_ctrl.play_sound(rm_define.media_sound_solmization_2CSharp, wait_for_complete=True)
      media_ctrl.play_sound(rm_define.media_sound_solmization_1G, wait_for_complete=True)

def l3():
      media_ctrl.play_sound(rm_define.media_sound_solmization_1C, wait_for_complete=True)
      media_ctrl.play_sound(rm_define.media_sound_solmization_2CSharp, wait_for_complete=True)
      media_ctrl.play_sound(rm_define.media_sound_solmization_1C, wait_for_complete=True)