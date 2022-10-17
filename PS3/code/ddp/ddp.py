# ddp.py
# This program runs the main DDP algorithm built on top of your util functions
# (Do not modify, but please read)
#
# Brian Plancher - Fall 2022
# Adapted from code written by Rus Tedrake and Scott Kuindersma

import sys, math, pygame, copy
from pygame.locals import *
from time import sleep
import numpy as np
from util import Util
np.set_printoptions(precision=3) # so things print nicer

class DDP:
    def __init__(self, robot_object, start_node, goal_node, N, XMAX_MIN, YMAX_MIN, MAX_ITER = 100, EXIT_TOL = 1e-3):
        self.robot_object = robot_object # the robot_object with physics and cost functions
        self.MAX_ITER = MAX_ITER         # total ddp loops to try
        self.EXIT_TOL = EXIT_TOL         # This is the convergence criterion. We will declare success when the trajectory
                                         # is updated by a norm of less that 1e-4. DO NOT MODIFY.
        self.N = N                       # Number of nodes in a trajectory
        self.start_node = start_node
        self.goal_node = goal_node
        self.util = Util(self.robot_object)
        self.XMAX_MIN = XMAX_MIN         # max for drawing locically
        self.YMAX_MIN = YMAX_MIN         # max for drawing locically
        self.canvas_max = 640            # max for drawing pixels

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

    def init_screen(self):
        # initialize and prepare screen
        pygame.init()
        self.screen = pygame.display.set_mode((self.canvas_max,self.canvas_max))
        pygame.display.set_caption('PS3 - RRT')
        black = 20, 20, 40
        blue = 0, 0, 255
        green = 0, 255, 0
        self.screen.fill(black)
        self.draw_circle(self.start_node, 5, blue)
        self.draw_circle(self.goal_node, 5, green)
        pygame.display.update()

    def draw_trajectory(self, x):
        white = 255, 240, 200
        red = 255, 0, 0
        self.draw_circle(x[:,0], 2, white)
        for k in range(1,self.N):
            self.draw_circle(x[:,k], 2, white)
            self.draw_line(x[:,k-1], x[:,k], red)
        pygame.display.update()
        sleep(0.1)

    def wait_to_exit(self, x, u, K, DISPLAY_MODE = True):
        # if in test mode return the path and the iters
        if not DISPLAY_MODE:
            return x, u, K
        # Else wait for the user to see the solution to exit
        else:
            while(1):
                for e in pygame.event.get():
                    if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                        sys.exit("Leaving because you requested it.")


    def iLQR(self, x, u, N, DISPLAY_MODE = False):
        # start up the graphics
        self.init_screen()
        
        # allocate memory for things we will compute
        nx = self.robot_object.get_state_size()
        nu = self.robot_object.get_control_size()
        du = np.zeros([nu,N-1])     # control updates
        K = np.zeros((nu,nx,N-1))   # feedback gains

        # set line search parameters
        alpha_factor = 0.5          # how much to reduce alpha by each deeper search
        alpha_min = 1e-4            # minimum alpha to try

        # compute initial cost
        J = self.util.compute_total_cost(x, u, nx, nu, N)
        delta_J = 0
        if DISPLAY_MODE:
            print("Initial Cost: ", J)

        # start the main loop
        iteration = 0
        while 1:

            # Do backwards pass to compute new control update and feedback gains: du and K
            # start by initializing the cost to go
            Vxx, Vx = self.util.initialize_CTG(x[:,N-1], nx, N) 
            for k in range(N-2,-1,-1):
                A, B, H, g = self.util.compute_approximation(x[:,k], u[:,k], nx, nu, k)
                # treating things as np arrays for the rest of this loop will make your life easier!
                A = np.array(A)
                B = np.array(B)
                H = np.array(H)
                g = np.array(g)
                Vxx = np.array(Vxx)
                Vx = np.array(Vx)

                # Backpropogate the CTG through the dynamics
                Hxx, Hux, Huu, gx, gu = self.util.backpropogate_CTG(A, B, H, g, Vxx, Vx, nx, nu, k)

                # Invert Huu block
                HuuInv = np.linalg.inv(Huu)

                # Compute feedback and next CTG
                duk, Kk = self.util.compute_du_K(Hxx, Hux, Huu, gx, gu, HuuInv, nx, nu, k)
                Vxx, Vx = self.util.compute_new_CTG(Hxx, Hux, Huu, gx, gu, HuuInv, duk, Kk, nx, nu, k)

                # save du and K for forward pass
                du[:,k] = duk.tolist()
                K[:,:,k] = Kk.tolist()

            # Do forwards pass to compute new x, u, J (with line search)
            alpha = 1
            while 1:
                # rollout new trajectory
                x_new = copy.deepcopy(x)
                u_new = copy.deepcopy(u)
                for k in range(N-1):
                    u_new[:,k] = u[:,k] + self.util.compute_control_update(x[:,k], x_new[:,k], K[:,:,k], du[:,k], alpha, nx, nu, k)
                    x_new[:,k+1] = self.robot_object.next_state(x_new[:,k], u_new[:,k])
                    
                # compute new cost
                J_new = self.util.compute_total_cost(x_new, u_new, nx, nu, N)
                delta_J = J - J_new
                
                # if a good new trajectory accept it
                if delta_J > 0:
                    x = x_new
                    u = u_new
                    J = J_new
                    if DISPLAY_MODE:
                        print("Iteration[", iteration, "] with cost[", round(J,4), "] and x final:")
                        print(x[:,N-1])
                        self.draw_trajectory(x)
                    break

                # failed try to continue the line search
                elif alpha > alpha_min:
                    alpha *= alpha_factor
                    if DISPLAY_MODE:
                        print("Deepening the line search")
                
                # failed line search
                else:
                    if DISPLAY_MODE:
                        print("Line search failed")
                    delta_J = 0 # note that we failed
                    break

            # Check for exit (or error)
            if delta_J < self.EXIT_TOL:
                if DISPLAY_MODE:
                    print("Exiting for exit_tolerance")
                break
            
            if iteration == self.MAX_ITER - 1:
                if DISPLAY_MODE:
                    print("Exiting for max_iter")
                break
            else:
                iteration += 1

        if DISPLAY_MODE:
            print("Final Trajectory")
            print(x)
            print(u)

        self.wait_to_exit(x, u, K, DISPLAY_MODE)