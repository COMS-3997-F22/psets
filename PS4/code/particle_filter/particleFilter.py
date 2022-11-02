import sys, random, math, pygame, time
from pygame.locals import *
import numpy as np
from functools import reduce
from util import Util

class ParticleFilter:
    def __init__(self, robot_object, starting_location, NParticles, NLandmarks, XDIM = 640, YDIM = 480, \
                       LINE_WIDTH = 10, process_noise = 0.1, measurement_noise = 0.1, DEBUG_MODE = False):
        self.ut = Util(robot_object, process_noise, measurement_noise)
        self.robot_object = robot_object            # Robot Object (see ackermannCar.py)
        self.NParticles = NParticles                # Number of Particles
        self.NLandmarks = NLandmarks                # Number of Landmarks
        self.process_noise = process_noise          # Amount of noise on motion
        self.measurement_noise = measurement_noise  # Amount of noise on sensors
        self.XDIM = XDIM                            # board dimmension
        self.YDIM = YDIM                            # board dimmension
        self.LINE_WIDTH = LINE_WIDTH                # width of obstacle lines
        self.real_location = starting_location
        self.estimated_state = None
        self.DEBUG_MODE = DEBUG_MODE
        self.particles = []
        self.landmarks = []
        
        # initialize and prepare screen
        pygame.init()
        self.screen = pygame.display.set_mode([self.XDIM, self.YDIM])
        self.white = 255, 240, 200
        self.black = 20, 20, 40
        self.red = 255, 0, 0
        self.blue = 0, 0, 255
        self.green = 0, 255, 0
        pygame.display.set_caption('HW4 - Particle Filter')

        # draw initial point, particles, and landmarks (sample randomly)
        for i in range(self.NParticles):
            self.particles.append(self.getRandomLocation())
        for i in range(self.NLandmarks):
            self.landmarks.append(self.getRandomLocation())
        self.redrawScreen()
        time.sleep(0.5)

    # get a random x,y,theta in the board
    def getRandomLocation(self):
        x = random.randrange(self.XDIM)
        y = random.randrange(self.YDIM)
        return [x,y]

    # turn list to tuple for pygame plotting
    def listToTuple(self, a):
        return (a[0], a[1])

    # update the whole screen
    def redrawScreen(self, weights = None):
        # draw black screen
        self.screen.fill(self.black)
        # draw landmarks
        for landmark in self.landmarks:
            pygame.draw.circle(self.screen, self.red, landmark, 5)
        # draw true location
        pygame.draw.circle(self.screen, self.blue, self.listToTuple(self.real_location), 5)
        # draw particles
        if weights == None:
            for particle in self.particles:
                pygame.draw.circle(self.screen, self.white, self.listToTuple(particle), 3)
        else:
            # change size based on weights
            sizes = [int(10 * a / max(weights)) for a in weights]
            for i in range(len(self.particles)):
                pygame.draw.circle(self.screen, self.white, self.listToTuple(self.particles[i]), sizes[i])

        # make the changes visible
        pygame.display.update()
        time.sleep(0.5)

    # apply the motion model to a particle
    def motionModel(self, particle_location, control_input, noNoise = False):
        # compute the new location
        updated_location = self.ut.applyMotionModel(particle_location, control_input)
        if noNoise:
            return updated_location
        # add process noise
        updated_location = self.ut.addProccessNoise(updated_location)
        # wrap angles incase we need it
        return self.robot_object.wrap_angles(updated_location)

    # compute sensor data
    def sensorModel(self, particle_location, landmarks):
        # use real model
        rawSensorData = self.robot_object.sensorData(particle_location, landmarks)
        return self.ut.addSensorNoise(rawSensorData)

    # make sure a particle doesn't move out of the bounds
    def correctForWorldBounds(self, particle_location, XDIM, YDIM):
        particle_location[0] = min(max(particle_location[0],0),XDIM)
        particle_location[1] = min(max(particle_location[1],0),YDIM)
        return particle_location

    # resample from the weighted particle distribution
    def resampleParticles(self, weights, XDIM, YDIM):
        new_particles = self.ut.getNewParticles(self.particles, weights)
        for i in range(len(new_particles)):
            particle = new_particles[i]
            particle = self.ut.addResampleNoise(particle) # avoid mode collapse
            particle = self.robot_object.wrap_angles(particle)
            particle = self.correctForWorldBounds(particle,XDIM,YDIM)
            new_particles[i] = particle
        self.particles = new_particles

    # estimate the state based on the particles
    def computeEstimatedState(self):
        total = reduce(lambda a, b: [a[0]+b[0], a[1]+b[1]], self.particles)
        count = len(self.particles)
        self.estimated_state = [total[0] / count, total[1] / count]

    # run the particle filter
    def run(self):
        # run forever
        while(1):
            # get a random control input
            control = self.robot_object.getRandomControl()
            
            # apply motion model to all particles and the real location
            self.real_location = self.motionModel(self.real_location, control, noNoise = True)
            for i in range(len(self.particles)):
                new_location = self.motionModel(self.particles[i], control)
                self.particles[i] = self.correctForWorldBounds(new_location, self.XDIM, self.YDIM)

            print("drawing after motionModel")
            self.redrawScreen()
            if(self.DEBUG_MODE):
                print("----------------")
                for particle in self.particles:
                    print(particle)
                print("----------------")

            #compute particle weights
            weights = []
            realSensorData = self.sensorModel(self.real_location, self.landmarks)
            for i in range(len(self.particles)):
                current_location = self.particles[i]
                # get sensor data
                particleSensorData = self.sensorModel(current_location, self.landmarks)
                # compute and save weight
                weights.append(self.ut.computeWeight(particleSensorData,realSensorData))

            print("drawing after sensor evidence")
            self.redrawScreen(weights)
            if(self.DEBUG_MODE):
                print(self.real_location)
                print("----------------")
                for i in range(len(self.particles)):
                    print(self.particles[i],weights[i])
                print("----------------")
            
            # re-sample particles and update the estimated state
            self.resampleParticles(weights, self.XDIM, self.YDIM)
            self.computeEstimatedState()

            # re-plot
            print("drawing after resample")
            self.redrawScreen()
            print("True State at: ", self.real_location)
            print("Estimated State at: ", self.estimated_state)
            print("State Error at: ", self.robot_object.state_distance(self.real_location,self.estimated_state))
            if(self.DEBUG_MODE):
                print("----------------")
                for particle in self.particles:
                    print(particle)
                print("----------------")

            # listen for exit
            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    sys.exit("Leaving because you requested it.")