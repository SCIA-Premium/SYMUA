from crowddynamics.logging import setup_logging
from acu.itaewon.simulation import Itaewon

if __name__ == "__main__":
    setup_logging()
    iterations = 1000
    simulation = Hallway(agent_type=Circular)
    for i in range(iterations):
        simulation.update()
