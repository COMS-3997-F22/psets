from math import sin, cos, pi
import copy

class Pendulum():
    def __init__(self, timestep = 0.15, gravity = 9.81, damping = 0.01, control_min = -5, control_max = 5, control_step = 0.25):
        self.timestep = timestep
        self.gravity = gravity
        self.damping = damping
        self.control_min = control_min
        self.control_max = control_max
        self.control_step = control_step

    def get_state_size(self):
        return 2
    def get_control_size(self):
        return 1

    def clamp(self, n, smallest, largest): 
        return max(smallest, min(n, largest))

    def wrap_angles(self, angle):
        upper_bound = pi
        lower_bound = -pi
        while (angle < lower_bound):
            angle += 2*pi
        while (angle > upper_bound):
            angle -= 2*pi
        return angle

    def state_delta(self, state1, state2):
        return [self.wrap_angles(state1[0]-state2[0]), state1[1]-state2[1]]

    def next_state(self, x, u):
        position = x[0]
        velocity = x[1]
        u = self.clamp(u, self.control_min, self.control_max) # to avoid unrealistic steps

        # compute dynamics
        acceleration = u - self.gravity*sin(position) - self.damping*velocity

        # user Euler integrator [q, qd] = [q, qd] + dt * [qd, qdd]
        new_position = self.wrap_angles(position + self.timestep*velocity)
        new_velocity = velocity + self.timestep*acceleration

        return [new_position, new_velocity]

    def next_state_gradient(self, x, u):
        position = x[0]
        velocity = x[1]

        # set up the gradient of dynamics and hessian of cost function
        dynamics_gradient = [[                          0,             1], \
                             [-self.gravity*cos(position), -self.damping]]
        A = [[1 + self.timestep*dynamics_gradient[0][0], 0 + self.timestep*dynamics_gradient[0][1]], \
             [0 + self.timestep*dynamics_gradient[1][0], 1 + self.timestep*dynamics_gradient[1][1]]] 
        B = [[0],[self.timestep]]
        return A, B

    def set_Q(self, Q):
        self.Q = Q
    def set_R(self, R):
        self.R = R
    def set_goal(self, goal):
        self.goal = goal

    def cost_value(self, x, u = None):
        cost = 0
        delta = self.state_delta(x, self.goal)
        cost += 0.5*(delta[0]*self.Q[0][0]*delta[0] + delta[0]*self.Q[0][1]*delta[1] + delta[1]*self.Q[1][0]*delta[0] + delta[1]*self.Q[1][1]*delta[1])
        if u is not None:
            cost += 0.5*u[0]*self.R[0]*u[0]
        return cost

    def gradient(self, x, u = None):
        delta = self.state_delta(x, self.goal)
        grad = [self.Q[0][0] * delta[0] + self.Q[0][1] * delta[1], self.Q[1][0] * delta[0] + self.Q[1][1] * delta[1]]
        if u is not None:
            ugrad = u[0]*self.R[0]
            grad.append(ugrad)
        return grad

    def hessian(self, x, u = None):
        if u is not None:
            H = copy.deepcopy(self.Q)
            H[0].append(0)
            H[1].append(0)
            H.append([0,0,self.R[0]])
            return H
        else:
            return self.Q

    def gradient_hessian(self, x, u = None):
        return self.hessian(x,u), self.gradient(x,u)