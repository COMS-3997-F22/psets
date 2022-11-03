import random

class Util:
    def __init__(self, robot_object, process_noise, measurement_noise):
        self.robot_object = robot_object            # Robot Object (see pointMass.py)
        self.process_noise = process_noise          # Amount of noise on motion
        self.measurement_noise = measurement_noise  # Amount of noise on sensors

    def addProccessNoise(self, robot_state):
        #
        # TODO: add motion (process) noise to all entries in the robot state
        #
        # input: robot_state is an array of floats
        # return: updated robot_state
        #
        # Hint: random.gauss(mean,stdDev) will return a random sample from a guassian distribution
        #
        return 2*robot_state

    def addSensorNoise(self, rawSensorData):
        #
        # TODO: add sensor (measurement) noise to all entries in the rawSensorData
        #
        # input: rawSensorData is an array of floats
        # return: updated rawSensorData
        #
        # Hint: random.gauss(mean,stdDev) will return a random sample from a guassian distribution
        #
        return 2*rawSensorData

    def addResampleNoise(self, particle_location):
        #
        # TODO: add noise to the resampled states to avoid mode collapse
        #       **add the average of measurement and process noise**
        #
        # input: particle_location is an array of floats
        # return: updated location
        #
        # Hint: random.gauss(mean,stdDev) will return a random sample from a guassian distribution
        #
        return 2*particle_location

    def applyMotionModel(self, location, control_input):
        #
        # TODO: compute the next state for a particle based on its location
        #       and the control_input
        #
        # input: location is an array of floats
        #        control_input is an array of floats
        # return: updated location after application of the robot_object's
        #         physics model
        #
        #
        return location

    def computeWeight(self, sensorData, realSensorData):
        #
        # TODO: compute the weight for given sensor data based on the realSensorData
        #
        # input: sensorData is an array of floats
        #        realSensorData is an array of floats
        # return: the weight (aka score) for the sensor data
        #
        return 1

    def getNewParticles(self, particles, weights):
        #
        # TODO: resample new particles given the weights
        #
        # input: particles is an array of locations (stored as [x,y])
        #        weights is an array of floats associated the the related particle
        #           e.g., weights[0] corresponds to particles[0]
        # return: an array of new particles (stored as [x,y])
        #
        # hint: You want to return the same amount of particles as you are passed in!
        # hint 2: Python random may have a function that does weighted sampling for you!
        #
        return particles
