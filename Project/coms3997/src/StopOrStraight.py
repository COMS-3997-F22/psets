#!/usr/bin/env python3
import rospy
from duckietown_msgs.msg import WheelsCmdStamped
from std_msgs.msg import Bool


class StopOrStraight:
    def __init__(self):
        # Save the name of the node
        self.node_name = rospy.get_name()
        rospy.loginfo(f"[{self.node_name}] Initializing.")

        # Set the maximum update rate for commands
        self.rate = rospy.Rate(30)  # 30hz

        # Set up publishers and subscribers
        self.stop = None
        self.pub_wheels_cmd = rospy.Publisher("~wheels_cmd", WheelsCmdStamped, queue_size=1)
        self.sub_stop = rospy.Subscriber("~stop_sign", Bool, self.cbStop, queue_size=1) # only process the latest
        rospy.loginfo(f"[{self.node_name}] Initialzed.")

    # save down the latest data on the stop_sign channel
    def cbStop(self, data):
        self.stop = data

    def main(self):
        while not rospy.is_shutdown():
            # go forward unless we see a stop sign
            if self.stop:
                vel = 0
            else:
                vel = 0.2

            # make the object the duckiebot is looking for
            wheels_cmd_msg = WheelsCmdStamped()
            wheels_cmd_msg.header.stamp = rospy.Time.now()
            wheels_cmd_msg.vel_left = vel
            wheels_cmd_msg.vel_right = vel
            self.pub_wheels_cmd.publish(wheels_cmd_msg)

            # sleep to not send commands too often
            self.rate.sleep()

if __name__ == "__main__":
    # Initialize the node with rospy
    rospy.init_node("stop_or_straight_node", anonymous=False)

    # Create the object
    node = StopOrStraight()
    node.main()