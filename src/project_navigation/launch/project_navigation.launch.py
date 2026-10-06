import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Package directories
    navigation_dir = get_package_share_directory('project_navigation')
    localization_dir = get_package_share_directory('project_localization')
    mapping_dir = get_package_share_directory('project_mapping')
    path_planning_dir = get_package_share_directory('project_path_planning')

    # Configuration files
    amcl_yaml = os.path.join(
        localization_dir,
        'config',
        'amcl_config.yaml'
    )

    nav2_yaml = os.path.join(
        path_planning_dir,
        'config',
        'project_params.yaml'
    )

    # Saved map
    map_file = os.path.join(
        mapping_dir,
        'maps',
        'my_map.yaml'
    )

    # RViz configuration
    rviz_config = os.path.join(
        navigation_dir,
        'rviz',
        'project_navigation.rviz'
    )

    return LaunchDescription([

        # ---------------------------------------------------------
        # MAP SERVER
        # ---------------------------------------------------------
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[
                {
                    'yaml_filename': map_file,
                    'use_sim_time': True
                }
            ]
        ),

        # ---------------------------------------------------------
        # AMCL LOCALIZATION
        # ---------------------------------------------------------
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[
                amcl_yaml
            ]
        ),

        # ---------------------------------------------------------
        # PLANNER SERVER
        # ---------------------------------------------------------
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[
                nav2_yaml
            ]
        ),

        # ---------------------------------------------------------
        # CONTROLLER SERVER
        # ---------------------------------------------------------
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[
                nav2_yaml
            ]
        ),

        # ---------------------------------------------------------
        # BEHAVIOR SERVER
        # ---------------------------------------------------------
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            output='screen',
            parameters=[
                nav2_yaml
            ]
        ),

        # ---------------------------------------------------------
        # BT NAVIGATOR
        # ---------------------------------------------------------
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[
                nav2_yaml
            ]
        ),

        # ---------------------------------------------------------
        # SINGLE LIFECYCLE MANAGER
        # ---------------------------------------------------------
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[
                {
                    'use_sim_time': True,
                    'autostart': True,
                    'node_names': [
                        'map_server',
                        'amcl',
                        'planner_server',
                        'controller_server',
                        'behavior_server',
                        'bt_navigator'
                    ]
                }
            ]
        ),

        # ---------------------------------------------------------
        # RVIZ2
        # ---------------------------------------------------------
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=[
                '-d',
                rviz_config
            ]
        )
    ])