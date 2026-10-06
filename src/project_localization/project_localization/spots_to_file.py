from custom_interfaces.srv import MyServiceMessage
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
import yaml

class SpotRecorderServer(Node):
    def __init__(self):
        super().__init__('spot_recorder')

        self.srv = self.create_service(MyServiceMessage, '/save_spot', self.provide_coordinates)

        self.subscriber_ = self.create_subscription(
                PoseWithCovarianceStamped,
                '/amcl_pose',
                self.callback,10
            )
                                                    
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

        self.spots = {}
            
        self.get_logger().info('SpotRecorderServer is ready to receive requests.')

    def callback(self, msg):  # Subscriber callback ...
        
        # Position coordinates ...
        self.latest_x = msg.pose.pose.position.x
        self.latest_y = msg.pose.pose.position.y
        self.latest_z = msg.pose.pose.position.z

        # Orientation coordinates ...

        self.latest_qx = msg.pose.pose.orientation.x
        self.latest_qy = msg.pose.pose.orientation.y
        self.latest_qz = msg.pose.pose.orientation.z   
        self.latest_qw = msg.pose.pose.orientation.w

    def provide_coordinates(self, request, response):  # Service callback ...

        self.get_logger().info('Request received, capturing coordinates.')

        label = request.label

        if label == "end":
            # Write all stored spots to the text file
            try:
                
                with open("spots.txt", "w") as file:
                    yaml.safe_dump(self.spots, file, sort_keys=False)
                    
                response.navigation_successful = True
                response.message = "Spots saved successfully."

                self.get_logger().info('All spots saved to spots.txt.')

            except Exception as e:
                
                response.navigation_successful = False
                response.message = f"Failed to save spots: {e}"

        else:
            # Save the current pose under the requested label
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

            response.navigation_successful = True
            response.message = f"Spot '{label}' saved."

            self.get_logger().info(f"Spot '{label}' saved.")

        return response
        
def main(args=None):
    rclpy.init(args=args)
    node = SpotRecorderServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()