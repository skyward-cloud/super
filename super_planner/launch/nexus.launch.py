import os.path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition

from launch_ros.actions import Node


def generate_launch_description():
    package_path = get_package_share_directory('super_planner')

    default_rviz_config_path = os.path.join(
        package_path, 'rviz', 'fpv.rviz')

    super_config_name = 'nexus.yaml'

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time', default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    super_config_name_cmd = DeclareLaunchArgument(
        'config_name', default_value=super_config_name,
        description='Yaml config file path'
    )

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(super_config_name_cmd)

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_config_path],
        output='screen'
    )
    # ld.add_action(rviz_node)

    SUPER = Node(
        package='super_planner',
        executable='fsm_node',
        output='screen',
        parameters=[{
            'config_name': super_config_name,
        }]
    )

    ld.add_action(SUPER)

    return ld
