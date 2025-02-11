# Copyright 2024 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from launch import LaunchDescription

from launch_ros.actions import Node

import launch_testing


def generate_test_description():
    entity_name = 'my_robot'
    remove = Node(package='ros_gz_sim',
                  executable='remove',
                  parameters=[{'world': 'default', 'entity_to_remove_name': entity_name}],
                  output='screen')
    test_remove = Node(package='ros_gz_sim', executable='test_remove', output='screen')
    return LaunchDescription([
        remove,
        test_remove,
        launch_testing.util.KeepAliveProc(),
        launch_testing.actions.ReadyToTest(),
    ]), locals()


class WaitForTests(unittest.TestCase):

    def test_termination(self, test_remove, proc_info):
        proc_info.assertWaitForShutdown(process=test_remove, timeout=200)


@launch_testing.post_shutdown_test()
class RemoveTest(unittest.TestCase):

    def test_output(self, entity_name, test_remove, proc_output):
        launch_testing.asserts.assertInStdout(proc_output, entity_name, test_remove)
