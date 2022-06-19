#!/usr/bin/env python3

import os
from ament_index_python import get_package_share_directory
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import sys

wav2vec2_dir = os.path.join(get_package_share_directory('spot_teleop'), 'wav2vec2')
sys.path.append(wav2vec2_dir)
from live_asr import LiveWav2Vec2

# model = wav2vec2_dir + '/wav2vec2-large-960h-lv60-self'
model = 'skpawar1305/wav2vec2-base-finetuned-ks'


class TeleopClass(Node):
    def __init__(self, asr):
        super().__init__('teleop_voice')
        self.create_timer(0.1, self.mytimercallback)
        spot_name = "Spot"
        self.pub_stt = self.create_publisher(String, '/' + spot_name + '/transcript', 1)
        self.movements_msg = String()
        self.asr = asr
        self.asr.start()

    def mytimercallback(self):
        text,sample_length,inference_time = self.asr.get_last_text()                        
        print(f"{sample_length:.3f}s"
                +f"\t{inference_time:.3f}s"
                +f"\t{text}")
        self.movements_msg.data = text
        self.pub_stt.publish(self.movements_msg)


def main(args=None):
    rclpy.init()
    asr = LiveWav2Vec2(model, device_name="default")
    teleop_voice = TeleopClass(asr)
    try:
        rclpy.spin(teleop_voice)
    except KeyboardInterrupt:
        asr.stop()
    teleop_voice.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
