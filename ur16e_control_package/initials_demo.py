#!/usr/bin/env python3

import rclpy
from threading import Thread
from ur16e_control_package.move_command import DynamicTrajectoryExecutor
import time

WAYPOINTS = [
    # "W"
    [[-0.05, 0.35, 0.15], [ 0.924, 0.383, 0, 0 ]]

]

joint_config = [
    -1.6006999999999998,  # shoulder_pan_joint
    -1.7271,              # shoulder_lift_joint
    -2.2029999999999994,  # elbow_joint
    -0.8079999999999998,  # wrist_1_joint
    1.5951,               # wrist_2_joint
    -0.030999999999999694 # wrist_3_joint
]



def generate_square_sweep_waypoints(width, height, z_height, discretize_step):
    """
    Generate waypoints for a square sweep pattern.
    
    :param width: Width of the square in meters
    :param height: Height of the square in meters
    :param z_height: Height of the sweep plane in meters
    :param discretize_step: Step size for discretization in millimeters
    :return: List of waypoints in the specified format
    """
    waypoints = []
    identity_quat = [0, 0, 0, 1]
    step = discretize_step / 1000  # Convert mm to meters

    # Calculate number of steps in each direction
    num_steps_x = int(width / step) + 1
    num_steps_y = int(height / step) + 1

    for i in range(num_steps_x):
        x = i * step
        if i % 2 == 0:  # Even rows: bottom to top
            y_range = range(num_steps_y)
        else:  # Odd rows: top to bottom
            y_range = range(num_steps_y - 1, -1, -1)
        
        for j in y_range:
            y = j * step
            
            # Add point at z_height
            waypoints.append([[x, y, z_height], identity_quat])
            
            # Add point at z=0
            waypoints.append([[x, y, 0], identity_quat])
            
            # Add point back at z_height
            waypoints.append([[x, y, z_height], identity_quat])

    return waypoints

WAYPOINTS1 = generate_square_sweep_waypoints(width=0.08, height=0.08, z_height=-0.02, discretize_step=40)

def main():
    # Initialize rclpy
    rclpy.init()

    # Create an instance of your executor
    executor = DynamicTrajectoryExecutor()


    # Start the ROS 2 spin in a separate thread
    executor_thread = Thread(target=rclpy.spin, args=(executor,), daemon=True)
    executor_thread.start()
    
    
    # execute the movements
    executor.move_to_first_waypoint(joint_config)
    executor.compute_and_execute_trajectory(WAYPOINTS, dt=0.2)
    print(WAYPOINTS1)
    #time.sleep(1)
    #print(executor.get_joint_states())

    executor.compute_and_execute_trajectory(executor.end_effector_frame_tf(WAYPOINTS1), dt=0.2)

    # Shutdown and cleanup
    rclpy.shutdown()
    executor_thread.join()
    executor.csv_file.close()

if __name__ == "__main__":
    main()