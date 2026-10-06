import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
import yaml
from action_msgs.msg import GoalStatus

class MoveToSpotNode(Node):
    def __init__(self):
        super().__init__('move_to_spot')

        self.declare_parameter('spot_name', '')
        self.spot_name = self.get_parameter('spot_name').value


        # create an action client to send request to Nav2 server later...
        self.client = ActionClient(self,NavigateToPose,'navigate_to_pose')


    # Create a function to read data from yaml file.

    def get_data_from_yaml(self):

        file_path = "spot-list.yaml"
        
        with open(file_path, "r") as file:   # if file already exists 
            existing_spots = yaml.safe_load(file) or {}

        
        spot_to_go = existing_spots["move_to_spot"]["ros__parameters"][self.spot_name]

        return spot_to_go
    
    # create a function to send data to the nav2 server.

    def send_data_to_nav2(self):

        self.spot_to_go = self.get_data_from_yaml()
        
        # assign coordinates from the spots file to the nav2 goal...

        goal_msg = NavigateToPose.Goal()
        
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        # assigning coordinates...

        # position coordinates..
        goal_msg.pose.pose.position.x = self.spot_to_go["position"]["x"]
        goal_msg.pose.pose.position.y = self.spot_to_go["position"]["y"]
        goal_msg.pose.pose.position.z = self.spot_to_go["position"]["z"]

        # orientation coordinates ...
        goal_msg.pose.pose.orientation.x = self.spot_to_go["orientation"]["x"]
        goal_msg.pose.pose.orientation.y = self.spot_to_go["orientation"]["y"]
        goal_msg.pose.pose.orientation.z = self.spot_to_go["orientation"]["z"]
        goal_msg.pose.pose.orientation.w = self.spot_to_go["orientation"]["w"]

        
        # wait for action server, don't send goal unless server is available
        self.client.wait_for_server()
        
        
        # Here is my navigation goal. Please send it to the action server.
        self._send_goal_future = self.client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)

        # When the server has responded to my goal request, call goal_response_callback()
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        # get the result now as goal was accepted ..
        self._get_result_future = goal_handle.get_result_async()   #Now give me the result when Nav2 has finished processing this navigation goal.
        self._get_result_future.add_done_callback(self.get_result_callback)

    # When navigation finishes, call get_result_callback()
    def get_result_callback(self, future):
        result = future.result()

        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Navigation succeeded!')
        else:
            self.get_logger().info(
                f'Navigation failed with status: {result.status}'
            )

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
            

def main(args=None):
    rclpy.init(args=args)
    node = MoveToSpotNode()
    node.send_data_to_nav2()
    try:
        rclpy.spin(node)   
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node() 
        rclpy.shutdown()


if __name__ == '__main__':
    main()





    
