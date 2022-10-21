import hmc5883l
from hmc5883l import  HMC5883L

class Compass():

    def TrueNorth(self):

        declination = hmc5883l.declination()
        heading = hmc5883l.heading()

        TrueNorth =



