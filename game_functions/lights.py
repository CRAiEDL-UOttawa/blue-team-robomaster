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

# using colours defined in dictionary
def set_led_color(top_color, bottom_color):
    # get RGB values for colors
    top_rgb = RGB.get(top_color)
    bottom_rgb = RGB.get(bottom_color)
    
    # check if both colors exist in dictionary
    if top_rgb is None:
        raise ValueError(f"Top color '{top_color}' not found.")
    if bottom_rgb is None:
        raise ValueError(f"Bottom color '{bottom_color}' not found.")
    
    # set the top and bottom LEDs 
    led_ctrl.set_top_led(rm_define.armor_top_all, top_rgb[0], top_rgb[1], top_rgb[2], rm_define.effect_always_on)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, bottom_rgb[0], bottom_rgb[1], bottom_rgb[2], rm_define.effect_always_on)


# using user's 1 array
def set_led_color(rgb_values):
    # check array has three values
    if len(rgb_values) != 3:
        raise ValueError("Array should contain exactly three elements: [x1, x2, x3]")
    
    x1, x2, x3 = rgb_values

    led_ctrl.set_top_led(rm_define.armor_top_all, x1, x2, x3, rm_define.effect_always_on)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, x1, x2, x3, rm_define.effect_always_on)


# using user's 2 arrays
def set_led_colors_dif(top_rgb, bottom_rgb):
    # check each array has three values
    if len(top_rgb) != 3 or len(bottom_rgb) != 3:
        raise ValueError("Each array should contain exactly three elements: [x1, x2, x3]")
    
    top_x1, top_x2, top_x3 = top_rgb
    bottom_x1, bottom_x2, bottom_x3 = bottom_rgb
    
    led_ctrl.set_top_led(rm_define.armor_top_all, top_x1, top_x2, top_x3, rm_define.effect_always_on)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, bottom_x1, bottom_x2, bottom_x3, rm_define.effect_always_on)