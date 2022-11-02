from particleFilter import ParticleFilter
from pointMass import PointMass

# first setup the robot
timestep = 1
control_max = 10
robot = PointMass(timestep, control_max)

# then setup the world
XDIM = 1000
YDIM = 1000
X0 = XDIM/5
Y0 = YDIM/3
starting_location = [X0,Y0]

# then set up and run the filter
NParticles = 1000
NLandmarks = 50
pf = ParticleFilter(robot,starting_location,NParticles,NLandmarks,XDIM,YDIM)
pf.run()