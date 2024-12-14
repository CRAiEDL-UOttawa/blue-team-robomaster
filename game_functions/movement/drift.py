# Simple function to have the robot drift

variable_V = 0
variable_W = 0
variable_R = 0

def drift_once():
    chassis_ctrl.set_trans_speed(1.5)
    chassis_ctrl.set_rotate_speed(variable_W)
    chassis_ctrl.move_with_time(0,0.5)
    chassis_ctrl.move_and_rotate(90, rm_define.anticlockwise)
    time.sleep(1)

def drift_indefinitely():
    while True:
        chassis_ctrl.set_trans_speed(1.5)
        chassis_ctrl.set_rotate_speed(variable_W)
        chassis_ctrl.move_with_time(0,0.5)
        chassis_ctrl.move_and_rotate(90, rm_define.anticlockwise)
        time.sleep(1)

def start():
    global variable_V
    global variable_W
    global variable_R
    variable_R = 0.3
    variable_W = 180
    variable_V = (variable_W * variable_R) * (3.14 / 180)
    drift_once()
    drift_indefinitely()

start()