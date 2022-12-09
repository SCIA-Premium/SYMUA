import numpy as np
from traitlets.traitlets import Float, Int
from cell_lists import add_to_cells, neighboring_cells 
from crowddynamics.core.geometry import geom_to_linear_obstacles
from crowddynamics.core.steering.collective_motion import more_than_five_neighbors, find_nearest_neighbors
from crowddynamics.core.sensory_region import is_obstacle_between_points
from crowddynamics.simulation.logic import LogicNode
from crowddynamics.simulation.agents import BASE_OXYGEN, BASE_PANIC, START_PANIC


class DeleteDeadAgent(LogicNode):
    """Logic to delete agents marked as inactive"""

    def update(self):
        agents = self.simulation.agents.array
        self.simulation.agents.array = np.delete(agents, np.where(~agents["active"]), axis=0)
        self.simulation.agents.array = np.delete(agents, np.where(agents["oxygen"] <= 0), axis=0)
        
class PanicAgent(LogicNode):
    """Logic to make agents panic if too many people are around"""
    sight_neighbors = Float(
        default_value=10.0,
        min=0,
        help="Maximum distance between agents that are accounted as neighbours " "that can be followed.",
    )
    size_nearest_other = Int(
        default_value=5,
        min=0,
        help="Maximum number of nearest agents inside sight_herding radius " "that herding agent are following.",
    )

    def update(self):
        agents = self.simulation.agents.array
        for i, agent in enumerate(agents):
            if agent["is_panic"] and agent["panic"] < START_PANIC:
                agent["is_panic"] = False
            elif agent["is_panic"]:
                agent["target_direction"] = -agent["target_direction"]
            elif agent["panic"] > START_PANIC:
                agent["is_panic"] = True
                agent["target_direction"] = -agent["target_direction"]
                
                field = self.simulation.field
                obstacles = geom_to_linear_obstacles(field.obstacles)
                position = agents["position"]
                sight = self.sight_neighbors
                
                points_indices, cells_count, cells_offset, grid_shape = add_to_cells(agents["position"], sight)
                cell_indices = np.arange(len(cells_count))
                neigh_cells = neighboring_cells(grid_shape)
                neighbors = find_nearest_neighbors(
                    position, sight,
                    self.size_nearest_other, cell_indices, neigh_cells, points_indices,
                    cells_count, cells_offset, obstacles)
                for j in neighbors[i]:
                    agents[j]['panic'] += START_PANIC 

class TooManyPeople(LogicNode):
    """Logic to kill people that are to pack"""

    sight_follower = Float(
        default_value=10.0,
        min=0,
        help="Maximum distance between agents that are accounted as neighbours " "that can be followed.",
    )
    size_nearest_other = Int(
        default_value=5,
        min=0,
        help="Maximum number of nearest agents inside sight_herding radius " "that herding agent are following.",
    )

    def update(self):
        agents = self.simulation.agents.array
        field = self.simulation.field
        obstacles = geom_to_linear_obstacles(field.obstacles)
        position = agents["position"]
        sight = self.sight_follower
        points_indices, cells_count, cells_offset, grid_shape = add_to_cells(agents["position"], sight)
        cell_indices = np.arange(len(cells_count))
        neigh_cells = neighboring_cells(grid_shape)
        math = (
            more_than_five_neighbors(
                position,
                sight,
                self.size_nearest_other,
                cell_indices,
                neigh_cells,
                points_indices,
                cells_count,
                cells_offset,
                obstacles,
            )
            - 5
        )
        t1 = agents["panic"] + math**3
        t = agents["oxygen"] - math**3
        t1 = np.where(t1 < BASE_PANIC, BASE_PANIC, t1)
        agents["panic"] = t1
        agents["oxygen"] = np.where(t > BASE_OXYGEN, BASE_OXYGEN, t)


class Killclose(LogicNode):
    """Logic to delete agents marked as inactive"""

    def update(self):
        self.simulation.agents.array["active"] = 0
        