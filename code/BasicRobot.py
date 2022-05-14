# Author: Lasse Niederkrome


# This is important for drawing the robot later
import TestDrawing


class BasicRobot:

    # Basic-Robot constructor
    def __init__(self, x, y, r, alpha):
        self.x = x                          # x-position
        self.y = y                          # y-position
        self.r = r                          # radius
        self.alpha = alpha                  # direction

    # Small function that shows all robot-info.
    def info(self):
        print(self.x)
        print(self.y)
        print(self.r)
        print(self.alpha)

#  def spawnRobot(self, x,y,r,alpha):


testRobot = BasicRobot(0, 0, 50, 0)

testRobot.info()

TestDrawing.main()
