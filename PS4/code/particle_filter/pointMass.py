import numpy as np
import random, copy

class PointMass:
    def __init__(self, timestep = 0.1, control_max = 1):
        self.timestep = timestep
        self.control_max = control_max
        self.nx = 2 # x and y position
        self.nu = 2 # delta x, y command

    # no angles so nothing to wrap
    # leaving this here for easier extension to other robots later
    def wrap_angles(self, state):
        return [state[0], state[1]]

    # see note above
    def state_delta(self, state1, state2):
        return [state1[0]-state2[0], state1[1]-state2[1]]

    # see note above
    def state_distance(self, state1, state2):
        delta = self.state_delta(state1,state2)
        total = 0
        for i in range(len(delta)):
            total += delta[i]*delta[i]
        return np.sqrt(total)

    # get a random control in max/min of x and y
    def getRandomControl(self):
        n1to1 = (random.random()-0.5)*2
        xcntrl = self.control_max*n1to1
        n1to1 = (random.random()-0.5)*2
        ycntrl = self.control_max*n1to1
        return [xcntrl,ycntrl]

    # point mass takes in control of delta x and delta y
    def next_state(self, xk, uk):
        x_new = np.zeros(self.nx)
        x_new[0] = xk[0] + self.timestep*uk[0]
        x_new[1] = xk[1] + self.timestep*uk[1]
        # print(xk,uk,x_new)
        return x_new

    # dynamics derivatives
    def next_state_gradient(self, xk, uk):
        dxdx = 1.0
        dxdy = 0.0
        dxdu = self.timestep

        dydx = 0.0
        dydy = 1.0
        dydu = self.timestep

        Ak = np.array([[dxdx,dxdy],[dydx,dydy]])
        Bk = np.array([dxdu],[dydu])

        return Ak, Bk

    # compute sensor data
    # in this case just the distance from each location
    def sensorData(self, location, landmarks):
        data = []
        for landmark in landmarks:
            delta_x = location[0] - landmark[0]
            delta_y = location[1] - landmark[1]
            distance = np.sqrt(delta_x*delta_x + delta_y*delta_y)
            data.append(distance)
        return data

    # our score of sensor data is going to be the delta
    # between the real and particle sensor data
    # we then map through sigmoid like function
    # to score 0 as high and large error as low
    def scoreSensorData(self, sensorData, realSensorData):
        totalErr = 0
        for i in range(len(realSensorData)):
            totalErr += abs(sensorData[i]-realSensorData[i])
        percentOff = totalErr/sum(realSensorData) # get percent off
        score = 1 / (np.exp(percentOff) - 1) # then map through sigmoid like function
        return score

    # cost data
    def set_Q(self, Q):
        self.Q = Q
    def set_R(self, R):
        self.R = R
    def set_goal(self, goal):
        self.goal = goal

    def cost_value(self, x, u = None):
        cost = 0
        delta = np.array(self.state_delta(x, self.goal))
        cost += 0.5*np.matmul(np.matmul(delta.transpose(),self.Q),delta)
        if u is not None:
            cost += 0.5*np.matmul(np.matmul(u.transpose(),R),u)
        return cost

    def cost_gradient(self, x, u = None):
        delta = np.array(self.state_delta(x, self.goal))
        grad = np.matmul(delta.transpose(),self.Q)
        if u is not None:
            ugrad = np.matmul(u.transpose(),R)
            grad.append(ugrad)
        return grad

    # assumes Q and R are diag
    def cost_hessian(self, x, u = None):
        diag_arr = np.diag(self.Q)
        if u is not None:
            diag_arr.append(np.diag(self.R))
        return np.diag(diag_arr)

    def cost_gradient_hessian(self, x, u = None):
        return self.hessian(x,u), self.gradient(x,u)