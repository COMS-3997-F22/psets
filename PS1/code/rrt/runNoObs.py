from rrt import rrt

XDIM = 640
YDIM = 480
Obs = {}

XY_START = (XDIM/3,YDIM/6)
XY_GOAL = (4*XDIM/5,5*YDIM/6)

game = rrt(Obs, XY_START, XY_GOAL, XDIM, YDIM)
game.runGame()