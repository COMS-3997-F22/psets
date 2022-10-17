import random
from math import sqrt,cos,sin,atan2,pi

class Util:
    def __init__(self, mode, robot_object):
        self.mode = mode
        self.robot_object = robot_object

    ################################################################
    #  Modified Versions of Core Functions from PS1 and new helper #
    #  functions that are already completed for you!               #
    ################################################################

    # compute the distance between two nodes
    def distance(self, current_node, desired_node, force_euclidean = False):
        if self.mode == "LQR" and not force_euclidean:
            return self.distance_LQR(current_node,desired_node)
        else:
            return self.distance_euclidean(current_node,desired_node)

    # Extend according to the mode
    def extend(self, current_node, new_point):
        """
        current_node - node from which we extend
        new_point - point in space which we are extending toward
        delta - maximum distance we extend by
        """
        control = 0
        if self.mode == "LQR":
            control = self.compute_control_LQR(current_node, new_point)
        else:
            control = self.compute_control_euclidean(current_node, new_point)
        return self.robot_object.next_state(current_node,control)

    # return either the goal or a random point
    def getNewPoint(self, XMAX_MIN, YMAX_MIN, XY_GOAL, goal_probability):
        """
        XMAX_MIN, YMAX_MIN - constants representing the max and min values in X and Y directions
        XY_GOAL - node (tuple of integers) representing the location of the goal
        goal_probability - the probability of sampling the goal
        """
        if self.sampleGoal(goal_probability):
            return  XY_GOAL;
        else:
            random_X = XMAX_MIN * (2 * (random.random()-0.5))
            random_Y = YMAX_MIN * (2 * (random.random()-0.5))
            return (random_X, random_Y)

    # return all possible valid controls
    def get_valid_controls(self):
        controls = []
        current_control = self.robot_object.control_min
        while current_control <= self.robot_object.control_max:
            controls.append(current_control)
            current_control += self.robot_object.control_step
        return controls

    ################################################################
    #  Modified Versions of Core Functions from PS1 and new helper #
    #  functions that you need to complete follow!                 #
    ################################################################

    # Compute the Euclidean Norm Distance
    def distance_euclidean(self, current_node, desired_node):
        #
        #
        # TODO
        # Calculuate the standard euclidean distance (aka the L2 norm aka see PS1)
        #
        # Hint: You may want to use the robot_object state_delta function!
        #
        delta = self.robot_object.state_delta(current_node,desired_node)
        return 0

    # Tests if the new_node is close enough to the goal to consider it a goal
    def winCondition(self, new_node, goal_node, WIN_RADIUS):
        """
        new_node - newly generated node we are checking
        goal_node - goal node
        WIN_RADIUS - constant representing how close we have to be to the goal to
            consider the new_node a 'win'
        """
        distance = self.distance(new_node,goal_node,True) # don't force_euclidean in future functions
                                                          # just doing it here for better visual comparison
                                                          # of the different modes getting equally close
        #
        #
        # TODO
        # Return True or False if we won
        #
        # Hint: What distance means you have won?
        #
        return False
    
    # Return whether or not we should sample the goal according
    # to the goal_probability.
    def sampleGoal(self, goal_probability):
        """
        goal_probability - the probability of sampling the goal
        """
        #
        # TODO
        # Return True or False if we should sample the goal
        #
        # Hint: For the autograder to work you MUST use the already imported
        #       random.random() as your random number generator.
        #
        return False

    # Find the nearest node in our list of nodes that is closest to the new_node
    def nearestNode(self, nodes, new_node):
        """
        nodes - a list of nodes in the RRT
        new_node - a node generated from getNewPoint
        """
        nearest_node = nodes[0]
        #
        # TODO
        # Return the nearest node to the new_node
        #
        # Hint: use the generic self.distance function!
        #
        return nearest_node

    # Compute the Euclidean Control
    def compute_control_euclidean(self, current_node, node_you_are_extending_towards):
        best_control = 0
        best_distance = float('inf')
        #
        # TODO
        #
        # Try all possible controls in the range [control_min, control_max]
        # with a discretization of control_step. Return the best control that
        # gets you as close as possible to the node_you_are_extending_towards.
        #
        # Hint: you may want to use the get_valid_controls and distance functions as
        #       well as the robot_object's next_state function!
        #
        return best_control

    # Compute the LQR Norm Distance
    def distance_LQR(self, current_node, desired_node):
        #
        #
        # TODO
        # Calculate the LQR distance / value / cost according to the quadratic model
        #
        # Hint: You may want to use the compute_LQR and state_delta
        #       functions in the robot_object!
        #
        return 0

    # Compute the LQR Control
    def compute_control_LQR(self, current_node, node_you_are_extending_towards):
        #
        #
        # TODO
        # Use the LQR gains to compute the optimal feedback control
        #
        # Hint: You may want to use the compute_LQR and state_delta
        #       functions in the robot_object!
        #
        #
        return 0