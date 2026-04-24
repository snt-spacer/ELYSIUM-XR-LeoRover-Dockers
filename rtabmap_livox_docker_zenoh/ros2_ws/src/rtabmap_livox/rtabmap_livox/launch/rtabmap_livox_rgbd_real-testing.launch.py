
# Example:
#   $ ros2 launch velodyne_driver velodyne_driver_node-VLP16-launch.py
#   $ ros2 launch velodyne_pointcloud velodyne_transform_node-VLP16-launch.py
#
#   SLAM:
#   $ ros2 launch rtabmap_examples vlp16.launch.py


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.actions import SetParameter

def generate_launch_description():
    
    robot_namespace="leo04"

    use_sim_time = LaunchConfiguration('use_sim_time')
    deskewing = LaunchConfiguration('deskewing')

    return LaunchDescription([

        # Launch arguments
        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        
        DeclareLaunchArgument(
            'deskewing', default_value='false',
            description='Enable lidar deskewing'),
        
        SetParameter(name='use_sim_time', value=LaunchConfiguration('use_sim_time')),
        
        # Nodes to launch
        Node(
            package='rtabmap_sync', executable='rgbd_sync', output='screen',
            parameters=[{
              'approx_sync':False
            }],
            remappings=[
              ('/depth/image', f'{robot_namespace}/realsense_camera_leo04/realsense_camera_leo04/aligned_depth_to_color/image_raw'),
              ('/rgb/camera_info' , f'{robot_namespace}/realsense_camera_leo04/realsense_camera_leo04/color/camera_info'),
              ('/rgb/image', f'{robot_namespace}/realsense_camera_leo04/realsense_camera_leo04/color/image_raw'),
              ('rgbd_image', 'rgbd_image'),
            ]),

        Node(
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[{
              'frame_id':f'{robot_namespace}/base_footprint',
              'subscribe_scan_cloud':True,
              'subscribe_rgbd':True,
              'approx_sync':True,
              'wait_for_transform':0.2,
              'odom_sensor_sync':True,
              # RTAB-Map's internal parameters are strings:
              'RGBD/ProximityMaxGraphDepth': '0',
              'RGBD/ProximityPathMaxNeighbors': '1',
              'RGBD/AngularUpdate': '0.05',
              'RGBD/LinearUpdate': '0.05',
              'RGBD/NeighborLinkRefinning':'true',
              'Mem/NotLinkedNodesKept': 'false',
              'Mem/STMSize': '30',
              'Mem/LaserScanNormalK': '20',
              'Reg/Strategy': '1',
              'RGBD/CreateOccupancyGrid': 'true',
              'Grid/Sensor': '2',
              #'Grid/FromDepth': 'true',
            }],
            remappings=[
              ('scan_cloud', 'assembled_cloud')
            ],
            arguments=[
              '-d' # This will delete the previous database (~/.ros/rtabmap.db)
            ]), 

        Node(
            package='rtabmap_odom', executable='icp_odometry', output='screen',
            parameters=[{
              'frame_id':f'{robot_namespace}/base_footprint',
              'odom_frame_id':'odom',
              'wait_for_transform':0.2,
              'expected_update_rate':15.0,
              'deskewing':deskewing,
              'scan_cloud_max_points': 1000,
              'scan_downsampling_setp': 5,
              # RTAB-Map's internal parameters are strings:
              'Icp/CCSamplingLimit':'10000',
              'Icp/CCFIlterOutFarthestPoints':'true',
              'Icp/PointToPlane': 'true',
              'Icp/Iterations': '10',
              'Icp/VoxelSize': '0.05',
              'Icp/Epsilon': '0.001',
              'Icp/PointToPlaneK': '20',
              'Icp/PointToPlaneRadius': '0',
              'Icp/MaxTranslation': '2',
              'Icp/MaxCorrespondenceDistance': '0.1',
              'Icp/RangeMin': '0.3', # Ignore laser scan points on the robot itself
              'Icp/RangeMax': '3.5',
              'Icp/Strategy': '1',
              'Icp/OutlierRatio': '0.7',
              'Icp/CorrespondenceRatio': '0.01',
              'Odom/ScanKeyFrameThr': '0.4',
              'OdomF2M/ScanSubtractRadius': '0.1',
              'OdomF2M/ScanMaxSize': '15000',
              'OdomF2M/BundleAdjustment': 'false',
            }],
            remappings=[
              ('scan_cloud', f'{robot_namespace}/livox/lidar'),
              ('imu', f'{robot_namespace}/imu/data_raw'),
            ]),

        Node(
            package='rtabmap_util', executable='point_cloud_assembler', output='screen',
            parameters=[{
              'max_clouds':10,
              'fixed_frame_id':'',
              'use_sim_time':use_sim_time,
            }],
            remappings=[
              ('cloud', 'odom_filtered_input_scan')
            ]),
        
       # Node(
       #     package='rtabmap_util', executable='point_cloud_aggregator', output='screen',
       #     parameters=[{
       #         'fixed_frame_id':f'{robot_namespace}/base_footprint',
       #         'frame_id':f'{robot_namespace}/base_footprint',
       #         'approx_sync':True,
       #         'count':2,
       #         'wait_for_transform_duration':0.2,
       #         'xyz_output':True,
       #     }],
       #     remappings=[
       #         ('cloud1', f'{robot_namespace}/realsense_camera_leo04/realsense_camera_leo04/depth/color/points'),
       #         ('cloud2', f'{robot_namespace}/livox/lidar')
       #     ],
       # ),

        # Node(
          #  package='rtabmap_viz', executable='rtabmap_viz', output='screen',
           # parameters=[{
            #  'frame_id':f'{robot_namespace}/base_footprint',
            #  'odom_frame_id':'odom',
            #  'subscribe_rgbd':True,
            #  'subscribe_odom_info':True,
            #  'subscribe_scan_cloud':True,
            #  'approx_sync':True
           # }],
           # remappings=[
           #    ('scan_cloud', 'odom_filtered_input_scan')
           # ]),
    ])
