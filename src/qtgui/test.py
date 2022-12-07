from crowddynamics.examples.simulations import Hallway
from crowddynamics.simulation.agents import Circular
from crowddynamics.logging import setup_logging

if __name__ == '__main__':
    setup_logging()
    iterations = 1000
    simulation = Hallway(agent_type=Circular)
    for i in range(iterations):
        simulation.update()