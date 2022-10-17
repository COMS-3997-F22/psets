from rrt import rrt
from pendulum import Pendulum
from math import pi

XMIN_MAX = pi
YMIN_MAX = 10
mode = "LQR"

XY_START = (0,0)
XY_GOAL = (3.14,0)

pend = Pendulum()
game = rrt(pend, XY_START, XY_GOAL, mode, XMIN_MAX, YMIN_MAX)
game.runGame()