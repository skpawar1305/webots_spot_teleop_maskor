#!/usr/bin/env python3

import os
from ament_index_python import get_package_share_directory
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import sys

coqui_dir = os.path.join(get_package_share_directory('spot_teleop'), 'coqui_model')
sys.path.append(coqui_dir)
from transcribe import STT


class TeleopClass(Node):
    def __init__(self):
        super().__init__('teleop_voice')
        self.create_timer(0.1, self.mytimercallback)
        self.stt = STT(coqui_dir)
        spot_name = "Spot"
        self.pub_stt = self.create_publisher(String, '/' + spot_name + '/transcript', 1)
        self.movements_msg = String()
        self.listen = False

    def mytimercallback(self):
        text = self.stt.listen()
        print('Text:', text)
        self.movements_msg.data = text
        self.pub_stt.publish(self.movements_msg)


def main(args=None):
    rclpy.init()
    teleop_voice = TeleopClass()
    try:
        rclpy.spin(teleop_voice)
    except KeyboardInterrupt:
        pass
    teleop_voice.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
