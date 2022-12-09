from pathlib import Path

from PIL import Image
import numpy as np
from traitlets.traitlets import Float, Int, Enum, default
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

from ..logic import DeleteDeadAgent

CURRENT_DIR = Path(__file__).parent


class ShibuyaSimple(MultiAgentSimulation):
    """ShibuyaSimple."""

    size = Int(default_value=50, min=2)
    agent_type = Circular

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

    def attributes4(self):
        orientation = -np.pi / 2
        return dict(
            body_type="adult",
            orientation=orientation,
            velocity=unit_vector(orientation),
            angular_velocity=0.0,
            target_direction=unit_vector(orientation),
            target_orientation=orientation,
            target=0,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bg_image = Image.open(CURRENT_DIR / "shibuya.jpg")
        self.bg_image_data = np.asarray(bg_image)

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
                    Adjusting(self) << (Navigation(self), Orientation(self)),
                    AgentObstacleInteractions(self),
                    AgentAgentInteractions(self),
                )
            )
        )

    @default("field")
    def _default_field(self):
        return fields.ShibuyaField()

    @default("agents")
    def _default_agents(self):
        agents = Agents(agent_type=self.agent_type)

        group1 = AgentGroup(
            size=self.size // 2, agent_type=self.agent_type, attributes=self.attributes1
        )
        group2 = AgentGroup(
            size=self.size // 2, agent_type=self.agent_type, attributes=self.attributes2
        )
        group3 = AgentGroup(
            size=self.size // 2, agent_type=self.agent_type, attributes=self.attributes3
        )

        agents.add_non_overlapping_group(
            group=group1, position_gen=self.field.sample_spawn(0)
        )
        agents.add_non_overlapping_group(
            group=group2, position_gen=self.field.sample_spawn(1)
        )
        agents.add_non_overlapping_group(
            group=group3, position_gen=self.field.sample_spawn(0)
        )

        return agents
