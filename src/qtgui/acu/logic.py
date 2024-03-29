import numpy as np
from traitlets.traitlets import Float, Int, Bool
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
        done = int((~agents["active"]).sum())
        deads = int((agents["oxygen"] <= 0).sum())
        if done or deads:
            self.simulation.data["dead_count"] = (
                self.simulation.data.get("dead_count", -self.simulation.data.get("never_spawned", 0)) + deads
            )
            self.simulation.data["escaped_count"] = (
                self.simulation.data.get("escaped_count", -self.simulation.data.get("never_spawned", 0)) + done
            )
        self.simulation.agents.array = np.delete(
            agents, np.where((~agents["active"]) | (agents["oxygen"] <= 0)), axis=0
        )


class PanicAgent(LogicNode):
    """Logic to make agents panic if too many people are around"""
    
    enable_panic = Bool(default_value=True)

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

    spread_panic_factor = Float(default_value=0.05, min=0, max=1, help="Factor of spread to neighbors when panic")
    
    def update(self):
        if not self.enable_panic:
            return
        agents = self.simulation.agents.array

        no_panic = np.where((agents["is_panic"] == True) & (agents["panic"] < START_PANIC))
        agents["is_panic"][no_panic] = False
        agents["panic"][no_panic] = BASE_PANIC
        agents["target_direction"][agents["is_panic"] == True] = -agents["target_direction"][agents["is_panic"] == True]
        new_panic = np.where((~agents["is_panic"]) & (agents["panic"] > START_PANIC))
        agents["is_panic"][new_panic] = True
        agents["target_direction"][new_panic] = True

        delta_panic = np.zeros(agents.size, dtype=np.int64)

        field = self.simulation.field
        obstacles = geom_to_linear_obstacles(field.obstacles)
        position = agents["position"]
        sight = self.sight_neighbors

        points_indices, cells_count, cells_offset, grid_shape = add_to_cells(agents["position"], sight)
        cell_indices = np.arange(len(cells_count))
        neigh_cells = neighboring_cells(grid_shape)
        neighbors = find_nearest_neighbors(
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

        for i in np.where(agents[agents["is_panic"]]):
            for j in neighbors[i]:
                delta_panic[j] = (~agents[j]["is_panic"]).astype(np.int64) * np.ceil(self.spread_panic_factor * START_PANIC)

        agents["panic"] += delta_panic
        self.simulation.data["is_panic_count"] = int(agents["is_panic"].sum())


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

    enable_panic = Bool(default_value=True)

    def update(self):
        agents = self.simulation.agents.array
        field = self.simulation.field
        obstacles = geom_to_linear_obstacles(field.obstacles)
        position = agents["position"]
        sight = self.sight_follower
        points_indices, cells_count, cells_offset, grid_shape = add_to_cells(agents["position"], sight)
        cell_indices = np.arange(len(cells_count))
        neigh_cells = neighboring_cells(grid_shape)
        nb_neighbours = (
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
        is_oxygen_low = agents["oxygen"] < BASE_OXYGEN / 2
        delta_p = nb_neighbours * 2 + np.random.uniform(-2, 2, size=nb_neighbours.size)
        delta_panic = agents["panic"] + delta_p + is_oxygen_low * 2
        new_oxygen = agents["oxygen"] - nb_neighbours**3
        if self.enable_panic:
            agents["panic"] = np.where(delta_panic < BASE_PANIC, BASE_PANIC, delta_panic)
        agents["oxygen"] = np.where(new_oxygen > BASE_OXYGEN, BASE_OXYGEN, new_oxygen)
