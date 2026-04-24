from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import SetRemap
import os

def generate_launch_description():
    # Where nav2_bringup's main launch lives
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    nav2_launch_file = os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')

    # Launch-time args (editable when you ros2 launch)
    params_file = LaunchConfiguration('params_file')
    cmd_vel_out = LaunchConfiguration('cmd_vel_out')

    return LaunchDescription([
        # Defaults: change these paths/topics as you like
        DeclareLaunchArgument(
            'params_file',
            default_value='/home/spacer/nav2_config/nav2_params.yaml'
        ),
        DeclareLaunchArgument(
            'cmd_vel_out',
            default_value='/leo04/cmd_vel'
        ),

        # Global remaps: everything launched after this will inherit these
        SetRemap(src='cmd_vel', dst=cmd_vel_out),
        SetRemap(src='/cmd_vel', dst=cmd_vel_out),

        # Bring up Nav2 with your params
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch_file),
            launch_arguments={'params_file': params_file}.items(),
        ),
    ])

