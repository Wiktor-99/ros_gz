"""Launch remove models in gz sim."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node


def generate_launch_description():

    world = LaunchConfiguration('world')
    entity_to_remove_name = LaunchConfiguration('entity_to_remove_name')

    declare_world_cmd = DeclareLaunchArgument(
        'world', default_value=TextSubstitution(text=''),
        description='World name')
    declare_entity_to_remove_name_cmd = DeclareLaunchArgument(
        'entity_to_remove_name', default_value=TextSubstitution(text=''),
        description='SDF filename')

    remove = Node(
        package='ros_gz_sim',
        executable='remove',
        output='screen',
        parameters=[{'world': world, 'entity_to_remove_name': entity_to_remove_name}],
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_entity_to_remove_name_cmd)
    ld.add_action(remove)

    return ld
