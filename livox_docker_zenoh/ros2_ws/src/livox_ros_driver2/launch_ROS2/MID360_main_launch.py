import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch

def generate_launch_description():

    robot_namespace=""
    if robot_namespace=="":
        try:
            robot_namespace = os.environ['ROS_NAMESPACE']
        except:
            print("Could not find robot namespace, defaulting to leo04")
            robot_namespace = "leo04"
    
    livox_main_launch_node = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('livox_ros_driver2'), 'launch_ROS2'),
                '/MID360_launch.py'])
    )

    bringup_with_namespace = GroupAction(
            actions=[
                PushRosNamespace(robot_namespace),
                livox_main_launch_node,
                ]
    )

    return LaunchDescription([
        bringup_with_namespace
        ])
