#!/usr/bin/env python3
import cv2
import numpy as np
import rospy

from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import Bool


class AlwaysNoSign:
    def __init__(self):
        # Save the name of the node
        self.node_name = rospy.get_name()
        rospy.loginfo(f"[{self.node_name}] Initializing.")

        # subscribe to the raw compressed image
        self.sub_image = rospy.Subscriber("~image_compressed", CompressedImage, self.processImage, buff_size=921600, queue_size=1)

        # publish on the stop_sign topic if we see one or not!
        self.pub_sign = rospy.Publisher("~stop_sign", Bool, queue_size=1)

    def processImage(self, image_msg):
        # get an openCV version of the image
        np_arr = np.fromstring(image_msg.data, np.uint8)
        image_cv = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # TODO CV goes here!

        # publish no sign (you might want to update this)
        self.pub_sign.publish(Bool(data=False))


if __name__ == "__main__":
    # Initialize the node with rospy
    rospy.init_node("always_no_sign_node", anonymous=False)

    # Create the object
    node = StopOrStraight()

    # Since we don't have a main that runs forever and instead just process images
    # we need to put this spin here so it runs forever
    rospy.spin()