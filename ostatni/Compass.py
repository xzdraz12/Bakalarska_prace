import hmc5883l


class Compass():

    def TrueNorth(self):

        declination = hmc5883l.declination()
        heading = hmc5883l.heading()

        TrueNorth =



