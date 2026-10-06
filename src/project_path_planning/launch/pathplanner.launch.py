from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    params_file = os.path.join(get_package_share_directory('project_path_planning'),'config','project_params.yaml')

    return LaunchDescription([
        
        Node(
            package= 'nav2_planner',
            executable= 'planner_server',
            name= 'planner_server',
            output='screen',
            parameters=[params_file]),

        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[params_file]),
        
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            parameters=[params_file],
            output='screen'),
        
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[params_file]),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_pathplanner',
            output='screen',
            parameters=[{'autostart': True},
                        {'node_names': ['planner_server',
                                        'controller_server',
                                        'behavior_server',
                                        'bt_navigator']}])
    ])
