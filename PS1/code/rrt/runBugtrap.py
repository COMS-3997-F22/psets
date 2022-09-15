from rrt import rrt

XDIM = 640
YDIM = 480
w = 100
w2 = 25
h = 150
h2 = 60
X0 = XDIM/5
Y0 = YDIM/3
X1 = 4*XDIM/5
Y1 = 2*YDIM/3
Obs = {}
Obs[0] = [(X0 + w2, Y0 + h2), (X0, Y0 + h2/2), (X0, Y0), (X0 + w, Y0), (X0 + w, Y0 + h), (X0, Y0 + h), (X0, Y0 + h - h2/2), (X0 + w2, Y0 + h - h2)]

XY_START = (X0+w/2,Y0+3*h/4) # Start in the trap
XY_GOAL = (4*XDIM/5,5*YDIM/6)

game = rrt(Obs, XY_START, XY_GOAL, XDIM, YDIM)
game.runGame()