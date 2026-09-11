import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np

class MockCameraNode(Node):
    def __init__(self):
        super().__init__('mock_cam')
        
        # 1. Declare parameters so ROS 2 knows they can be changed externally
        self.declare_parameter('show_odom', True)
        self.declare_parameter('show_ut', True)

        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.subscription = self.create_subscription(String, 'sensor_data', self.sensor_callback, 10)
        self.bridge = CvBridge()
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.latest_sensor_data = "Waiting for sensors..."

    def sensor_callback(self, msg):
        self.latest_sensor_data = msg.data

    def timer_callback(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # 2. Grab the current state of the toggles on every frame
        show_odom = self.get_parameter('show_odom').value
        show_ut = self.get_parameter('show_ut').value

        # 3. Conditionally draw Odom
        if show_odom:
            cv2.putText(frame, f"Odom: {self.latest_sensor_data}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
        # 4. Conditionally draw UT
        if show_ut:
            cv2.putText(frame, "UT: Active", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.putText(frame, 'BASE STATION LIVE', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        
        msg = self.bridge.cv2_to_imgmsg(frame, "bgr8")
        self.publisher_.publish(msg)

def main():
    rclpy.init()
    node = MockCameraNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
