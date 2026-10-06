import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
import yaml
from pathlib import Path

class SpotRecorderNode(Node):
    def __init__(self):
        super().__init__('spot_recorder')

        self.subscriber_ = self.create_subscription(
                PoseWithCovarianceStamped,
                '/initialpose',
                self.callback,10
            )

        self.pose_received = False
        self.spots = {}
        
        self.get_logger().info('SpotRecorderNode is ready to receive requests.')

    # Variables ...

        # Position-coordinates ...
        self.latest_x = None
        self.latest_y = None
        self.latest_z = None

        # Orientation-coordinates ...

        self.latest_qx = None
        self.latest_qy = None
        self.latest_qz = None
        self.latest_qw = None
    
    
    def callback(self, msg):

        # Position coordinates ...
        self.latest_x = msg.pose.pose.position.x
        self.latest_y = msg.pose.pose.position.y
        self.latest_z = msg.pose.pose.position.z

    
    # Orientation coordinates ...

        self.latest_qx = msg.pose.pose.orientation.x
        self.latest_qy = msg.pose.pose.orientation.y
        self.latest_qz = msg.pose.pose.orientation.z   
        self.latest_qw = msg.pose.pose.orientation.w

        self.pose_received = True


    def record_spot(self):
    
        
        while not self.pose_received:
            
            rclpy.spin_once(self)   # give ROS one opportunity to process /initialpose
                                    # Process ROS callbacks/events once, then give control back to my Python code.
        

        label = input("Please Enter label: ")

        self.spots[label] = {
                "position": {
                    "x": self.latest_x,
                    "y": self.latest_y,
                    "z": self.latest_z
                },
                "orientation": {
                    "x": self.latest_qx,
                    "y": self.latest_qy,
                    "z": self.latest_qz,
                    "w": self.latest_qw
                }
            }

        self.get_logger().info("Pose recorded")

    
    def save_to_yaml(self):

        file_path = "spots.yaml"

        try:
            with open(file_path, "r") as file:   # if file already exists 
                existing_spots = yaml.safe_load(file) or {}
        except FileNotFoundError:
            existing_spots = {}     # if no file exists, dont crash, instead start with a simple dictionary.

        existing_spots.update(self.spots)  # keep updating data to the dictionary.

        with open(file_path, "w") as file:  # open the file in read mode, if no file exists, create it ...
            yaml.safe_dump(existing_spots, file, sort_keys=False)

        self.get_logger().info("Spot saved to YAML.")

def main(args=None):
    rclpy.init(args=args)
    node = SpotRecorderNode()
    try:
        node.record_spot()
        node.save_to_yaml()  
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node() 
        rclpy.shutdown()


if __name__ == '__main__':
    main()