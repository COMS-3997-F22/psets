# rrt.py
# This program runs the main RRT algorithm built on top of your util functions
# (Do not modify, but please read)
#
# Brian Plancher - Fall 2018
# Adapted from code written by Steve LaValle and Rus Tedrake

import sys, random, math, pygame
from pygame.locals import *
from util import Util

class rrt:
    def __init__(self, obstacles, start_node, goal_node, XDIM = 640, YDIM = 480, DELTA = 5.0, MAX_ITER = 100000, WIN_RADIUS = 0.25, LINE_WIDTH = 10, TEST_MODE = 0):
        self.obstacles = obstacles # Obstacles are represented by a list of points defining line segments starting from 0 to N
        self.LINE_WIDTH = LINE_WIDTH # width of obstacle lines
        self.XDIM = XDIM # board dimmension
        self.YDIM = YDIM # board dimmension
        self.DELTA = DELTA # This controls how far the RRT extends in each step. DO NOT MODIFY.
        self.MAX_ITER = MAX_ITER # total points we will allow the algorithm to try
        self.WIN_RADIUS = WIN_RADIUS # This is the convergence criterion. We will declare success when the tree reaches within
                                     # 0.25 in distanceance from the goal. DO NOT MODIFY.
        self.TEST_MODE = TEST_MODE # do not wait for user to exit and return the final result
        self.start_node = start_node
        self.goal_node = goal_node

    def runGame(self):
        # initialize and prepare screen
        pygame.init()
        screen = pygame.display.set_mode([self.XDIM, self.YDIM])
        pygame.display.set_caption('HW4 - RRT')
        white = 255, 240, 200
        black = 20, 20, 40
        red = 255, 0, 0
        blue = 0, 0, 255
        green = 0, 255, 0
        screen.fill(black)
        pygame.draw.circle(screen, blue, self.start_node, 5)
        pygame.draw.circle(screen, green, self.goal_node, 5)
        for key in self.obstacles.keys():
            pygame.draw.lines(screen, red, 0, self.obstacles[key], self.LINE_WIDTH)

        # start the list of nodes
        nodes = []
        parents = {}
        nodes.append(self.start_node)
        wastes = 0

        # init our util function object
        u = Util()

        # explore until we max out or find the goal
        for i in range(self.MAX_ITER):
            # Get a new point
            xy = u.getNewPoint(self.XDIM,self.YDIM,self.goal_node)
            # If that point is collision free then try to connect it.
            if u.isCollisionFree(self.obstacles,xy,self.LINE_WIDTH):
                # first find the "nearest" node to connect to
                nn = u.nearestNode(nodes,xy)
                # take a step in that direction
                newnode = u.extend(nn,xy,self.DELTA)
                # make sure we are still collision free
                if u.isCollisionFree(self.obstacles,newnode,self.LINE_WIDTH):
                    # if so append to the list and draw it
                    nodes.append(newnode)
                    pygame.draw.line(screen,white,nn,newnode)
                    # make sure to add it to our parents dict (represents the tree)
                    parents[newnode] = nn
                    # and check to see if we won
                    won = u.winCondition(newnode,self.goal_node,self.WIN_RADIUS)
                    if won:
                        break
                else:
                    wastes += 1
            else:
                wastes += 1
            pygame.display.update()

            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    sys.exit("Leaving because you requested it.")
        print("Winner Winner Chicken Dinner") # Do you know the movie reference?
        print("Total Iters %d" % i) # How many times did we try to extend our tree?
        print("Wastes %d" % wastes) # How many of these tries were wasted due to collisions?
        # Return the path to the goal if we are in test mode for grading
        if (self.TEST_MODE):
            path = [nodes[-1]]
            node = nodes[-1]
            while node != nodes[0]:
                node = parents[node]
                path.append(node)
            return path
        # Else wait for the user to see the solution to exit
        else:
            while(1):
                for e in pygame.event.get():
                    if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                        sys.exit("Leaving because you requested it.")

# if python says run, then we should run
if __name__ == '__main__':
    main()
