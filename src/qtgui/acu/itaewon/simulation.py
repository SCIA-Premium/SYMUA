from pathlib import Path

from PIL import Image
import numpy as np
from traitlets.traitlets import Float, Int, Enum, default, Bool
from crowddynamics.core.vector2D import unit_vector
from crowddynamics.simulation.agents import Agents, AgentGroup, Circular, ThreeCircle

from . import fields
from crowddynamics.simulation.multiagent import MultiAgentSimulation
from crowddynamics.examples.simulations import Hallway
from crowddynamics.simulation.logic import (
    Adjusting,
    AgentAgentInteractions,
    AgentObstacleInteractions,
    Fluctuation,
    InsideDomain,
    Integrator,
    Navigation,
    Orientation,
    Reset,
)

from ..logic import DeleteDeadAgent, TooManyPeople, PanicAgent

CURRENT_DIR = Path(__file__).parent


class Itaewon(MultiAgentSimulation):
    """ShibuyaSimple."""

    size = Int(default_value=75, min=2)
    agent_type = Circular
    
    enable_panic = Bool(default_value=True)
    spread_panic_factor = Float(default_value=0.05, min=0, max=1, help="Factor of spread to neighbors when panic")

    
    def attributes1(self):
        """attributes1."""
        orientation = 0.0
        return dict(
            body_type="adult",
            orientation=orientation,
            velocity=unit_vector(orientation),
            angular_velocity=0.0,
            target_direction=unit_vector(orientation),
            target_orientation=orientation,
            target=0,
        )

    def attributes2(self):
        orientation = np.pi
        return dict(
            body_type="adult",
            orientation=orientation,
            velocity=unit_vector(orientation),
            angular_velocity=0.0,
            target_direction=unit_vector(orientation),
            target_orientation=orientation,
            target=0,
        )

    def attributes3(self):
        orientation = np.pi / 2
        return dict(
            body_type="adult",
            orientation=orientation,
            velocity=unit_vector(orientation),
            angular_velocity=0.0,
            target_direction=unit_vector(orientation),
            target_orientation=orientation,
            target=0,
        )

    @default("logic")
    def _default_logic(self):
        return (
            Reset(self)
            << DeleteDeadAgent(self)
            << InsideDomain(self)
            << (
                Integrator(self)
                << (
                    Fluctuation(self),
                    Adjusting(self)
                    << (
                        Navigation(self),
                        PanicAgent(self, spread_panic_factor=self.spread_panic_factor, enable_panic=self.enable_panic),
                        Orientation(self),
                        TooManyPeople(self, enable_panic=self.enable_panic),
                    ),
                    AgentObstacleInteractions(self),
                    AgentAgentInteractions(self),
                )
            )
        )

    @default("field")
    def _default_field(self):
        return fields.ItaewonField()

    def update(self):
        self.data["text_data"] = self.text_data()
        super().update()

    def text_data(self):
        return f"Escaped: {self.data.get('escaped_count', 0)} Died: {self.data.get('dead_count', 0)} Panicking: {self.data.get('is_panic_count', 0)}"

    @default("agents")
    def _default_agents(self):
        agents = Agents(agent_type=self.agent_type)

        group1 = AgentGroup(size=self.size, agent_type=self.agent_type, attributes=self.attributes1)
        group2 = AgentGroup(size=self.size, agent_type=self.agent_type, attributes=self.attributes2)
        group3 = AgentGroup(size=self.size, agent_type=self.agent_type, attributes=self.attributes3)

        agents.add_non_overlapping_group(group=group1, position_gen=self.field.sample_spawn(0))
        agents.add_non_overlapping_group(group=group2, position_gen=self.field.sample_spawn(1))
        agents.add_non_overlapping_group(group=group3, position_gen=self.field.sample_spawn(2))

        self.data["never_spawned"] = 3 * self.size - agents.index

        return agents
