import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import GroupAction
from launch_ros.actions import PushRosNamespace


robot_namespace = None
try:
    robot_namespace = os.environ['ROS_NAMESPACE']
except Exception as e:
    print(e)
    robot_namespace = ""

def generate_launch_description():
    leorover_realsense_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('leorover_realsense'), 'launch'),
            '/d455_launch.py'])
    )

    bringup_with_namespace = GroupAction(
        actions=[
            PushRosNamespace(robot_namespace),
            leorover_realsense_node,
        ]
    )

    return LaunchDescription([
    bringup_with_namespace
    ])

