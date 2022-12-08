import numpy as np

from crowddynamics.simulation.logic import LogicNode


class DeleteDeadAgent(LogicNode):
    """Logic to delete agents marked as inactive"""

    def update(self):
        agents = self.simulation.agents.array
        self.simulation.agents.array = np.delete(agents, np.where(~agents["active"]), axis=0)
