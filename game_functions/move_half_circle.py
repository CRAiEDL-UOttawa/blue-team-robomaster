# Should we remove this?

# Simple script for robot moving in half circle
# TODO - Have gimbal "scan" in given direction

def start():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    chassis_ctrl.set_trans_speed(0.7)
    gimbal_ctrl.rotate_with_degree(rm_define.gimbal_up,30)
    gimbal_ctrl.set_rotate_speed(30)
    while True:
        chassis_ctrl.move_with_distance(65,1.5)
        time.sleep(1)
        chassis_ctrl.move_with_distance(-115,1.5)
        time.sleep(1)
        chassis_ctrl.move_with_distance(115,1.5)
        time.sleep(1)
        chassis_ctrl.move_with_distance(-65,1.5)
