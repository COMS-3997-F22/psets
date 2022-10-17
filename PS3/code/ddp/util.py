import numpy as np

class Util:
    def __init__(self, robot_object):
        self.robot_object = robot_object

    ##################################################
    #  Helper functions you need to fill out go here #
    ##################################################

    # Compute the total cost along the trajectory
    def compute_total_cost(self, x, u, nx, nu, N):
        #
        # TODO
        #
        # Hint: You may want to use the helper functions in the robot_object!
        #
        J = 0
        return J
    
    def initialize_CTG(self, x, nx, k):
        #
        # TODO
        #
        # Hint: You may want to use the helper functions in the robot_object!
        #
        Vxx = 0
        Vx = 0
        return Vxx, Vx

    def compute_approximation(self, x, u, nx, nu, k):
        #
        # TODO
        #
        # Hint: You may want to use the helper functions in the robot_object!
        #
        H = 0
        g = 0
        A = 0
        B = 0
        return A, B, H, g

    def backpropogate_CTG(self, A, B, H, g, Vxx, Vx, nx, nu, k):
        #
        # TODO
        #
        # Hint: A = fx, B = fu, H = Jww, g = Jw where w is x or u!
        # Hint2: Everything is a np.array and np.matmul may be helpful!
        #
        Hxx = 0
        Huu = 0
        Hux = 0
        gx = 0
        gu = 0
        return Hxx, Hux, Huu, gx, gu

    def compute_du_K(self, Hxx, Hux, Huu, gx, gu, HuuInv, nx, nu, N):
        #
        # TODO
        #
        # Hint: Everything is a np.array and np.matmul may be helpful!
        #
        K = 0
        du = 0
        return du, K


    def compute_new_CTG(self, Hxx, Hux, Huu, gx, gu, HuuInv, du, K, nx, nu, N):
        #
        # TODO
        #
        # Hint: Everything is a np.array and np.matmul may be helpful!
        #
        Vxx = 0
        Vx = 0
        return Vxx, Vx

    def compute_control_update(self, x, x_new, K, du, alpha, nx, nu, N):
        #
        # TODO
        #
        # Hint: You may want to use the helper functions in the robot_object!
        # Hint2: Everything is a np.array and np.matmul may be helpful!
        #
        change_in_u = 0
        return change_in_u

    