from crowddynamics.logging import setup_logging
from acu.itaewon.simulation import Itaewon

if __name__ == "__main__":
    setup_logging()
    iterations = 1000
    simulation = Itaewon()
    for i in range(iterations):
        simulation.update()
