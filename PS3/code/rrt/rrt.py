# rrt.py
# This program runs the main RRT algorithm built on top of your util functions
# (Do not modify, but please read)
#
# Brian Plancher - Fall 2022
# Adapted from code written by Steve LaValle, Rus Tedrake, and Scott Kuindersma

import sys, random, math, pygame
from pygame.locals import *
from util import Util

class rrt:
    def __init__(self, robot_object, start_node, goal_node, mode = "euclidean",\
                 XMAX_MIN = math.pi, YMAX_MIN = 10, MAX_ITER = 100000, WIN_RADIUS = 0.15, \
                 GOAL_PROB = 0.1, TEST_MODE = 0):
        # min and max of plot
        self.XMAX_MIN = XMAX_MIN
        self.YMAX_MIN = YMAX_MIN
        self.robot_object = robot_object # the robot_object with physics
        self.mode = mode # what kind of distance / extend functions
        self.MAX_ITER = MAX_ITER # total points we will allow the algorithm to try
        self.WIN_RADIUS = WIN_RADIUS # This is the convergence criterion. We will declare success when the tree reaches within
                                     # 0.15 in distanceance from the goal. DO NOT MODIFY.
        self.TEST_MODE = TEST_MODE # do not wait for user to exit and return the final result
        self.GOAL_PROB = GOAL_PROB # how often to bias to the goal
        self.start_node = start_node
        self.goal_node = goal_node
        self.canvas_max = 640

    def draw_circle(self, node, size, color):
        percent_x = (node[0] + self.XMAX_MIN) / 2 / self.XMAX_MIN
        percent_y = (node[1] + self.YMAX_MIN) / 2 / self.YMAX_MIN
    
        scaled_x = int(self.canvas_max*percent_x)
        scaled_y = int(self.canvas_max*percent_y)    

        pygame.draw.circle(self.screen, color, (scaled_x, scaled_y), size)

    def draw_line(self, node1, node2, color):
        percent_x1 = (node1[0] + self.XMAX_MIN) / 2 / self.XMAX_MIN
        percent_y1 = (node1[1] + self.YMAX_MIN) / 2 / self.YMAX_MIN
        percent_x2 = (node2[0] + self.XMAX_MIN) / 2 / self.XMAX_MIN
        percent_y2 = (node2[1] + self.YMAX_MIN) / 2 / self.YMAX_MIN
    
        scaled_x1 = int(self.canvas_max*percent_x1)
        scaled_y1 = int(self.canvas_max*percent_y1)
        scaled_x2 = int(self.canvas_max*percent_x2)
        scaled_y2 = int(self.canvas_max*percent_y2)

        # check if angle wrapping (and don't draw lines across the screen)
        if node1[0] - node2[0] > math.pi:
            pass
        elif node1[0] - node2[0] < -math.pi:
            pass
        else:
            pygame.draw.line(self.screen, color, (scaled_x2, scaled_y2), (scaled_x1, scaled_y1))

    def runGame(self):
        # initialize and prepare screen
        pygame.init()
        self.screen = pygame.display.set_mode((self.canvas_max,self.canvas_max))
        pygame.display.set_caption('PS3 - RRT')
        white = 255, 240, 200
        black = 20, 20, 40
        red = 255, 0, 0
        blue = 0, 0, 255
        green = 0, 255, 0
        self.screen.fill(black)
        self.draw_circle(self.start_node, 5, blue)
        self.draw_circle(self.goal_node, 5, green)
        
        # start the list of nodes
        nodes = []
        parents = {}
        nodes.append(self.start_node)

        # init our util function object
        u = Util(self.mode, self.robot_object)

        # explore until we max out or find the goal
        for i in range(self.MAX_ITER):
            # Get a new point
            random_point = u.getNewPoint(self.XMAX_MIN,self.YMAX_MIN,self.goal_node,self.GOAL_PROB)
            # self.draw_circle(random_point, 1, red)
            # No obstacles in this pset so try to find nearest node to connect with
            nearest_node = u.nearestNode(nodes,random_point)
            # take a step in that direction
            new_node = u.extend(nearest_node,random_point)
            # again assuming collision free append to list and draw
            nodes.append(new_node)
            self.draw_circle(new_node, 2, white)
            # self.draw_line(new_node, nearest_node, white)
            # make sure to add it to our parents dict (represents the tree)
            parents[new_node] = nearest_node
            # and check to see if we won
            won = u.winCondition(new_node,self.goal_node,self.WIN_RADIUS)
            if won:
                break
            pygame.display.update()

            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    sys.exit("Leaving because you requested it.")
        # reconstruct path to goal
        path = [nodes[-1]]
        node = nodes[-1]
        while node != nodes[0]:
            node = parents[node]
            path.append(node)
        print("Winner Winner Chicken Dinner") # Do you know the movie reference?
        print("Total Iters %d" % i) # How many times did we try to extend our tree?
        # Plot the path to the goal
        for i in range(len(path)-1):
            self.draw_line(path[i], path[i+1], red)
        pygame.display.update()
        
        # if in test mode return the path and the iters
        if self.TEST_MODE:
            return (path, i)
        # Else wait for the user to see the solution to exit
        else:
            while(1):
                for e in pygame.event.get():
                    if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                        sys.exit("Leaving because you requested it.")

# if python says run, then we should run
if __name__ == '__main__':
    main()
