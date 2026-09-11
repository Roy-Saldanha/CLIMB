import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class SensorPublisher(Node):
    def __init__(self):
        super().__init__('sensor_publisher')
        self.publisher_ = self.create_publisher(String, 'sensor_data', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        ut = round(random.uniform(5.0, 10.0), 2)
        odom = round(random.uniform(0.0, 100.0), 1)
        msg = String()
        msg.data = f'UT: {ut}mm | Odom: {odom}m'
        self.publisher_.publish(msg)

def main():
    rclpy.init()
    node = SensorPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
