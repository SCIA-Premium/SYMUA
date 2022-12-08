from pathlib import Path

from PIL import Image
import numpy as np
from traitlets.traitlets import Float, Int, Enum, default
from crowddynamics.core.vector2D import unit_vector
from crowddynamics.simulation.agents import Agents, AgentGroup, Circular, \
    ThreeCircle

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
    size = Int(
        default_value=50,
        min=2)
    agent_type = Enum(
        default_value=Circular,
        values=(Circular, ThreeCircle),)
    body_type = Enum(
        default_value='adult',
        values=('adult',))
    width = Float(
        default_value=1369.0,
        min=0)
    height = Float(
        default_value=5.0,
        min=0)
    ratio = Float(
        default_value=1 / 3,
        min=0, max=1)

    def attributes1(self):
        orientation = 0.0
        return dict(body_type=self.body_type,
                    orientation=orientation,
                    velocity=unit_vector(orientation),
                    angular_velocity=0.0,
                    target_direction=unit_vector(orientation),
                    target_orientation=orientation,
                    target=1)

    def attributes2(self):
        orientation = np.pi
        return dict(body_type=self.body_type,
                    orientation=orientation,
                    velocity=unit_vector(orientation),
                    angular_velocity=0.0,
                    target_direction=unit_vector(orientation),
                    target_orientation=orientation,
                    target=0)
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
                    Adjusting(self) << (Navigation(self, radius=10, step=50), Orientation(self)),
                    AgentAgentInteractions(self),
                    AgentObstacleInteractions(self),
                )
            )
        )

    @default('field')
    def _default_field(self):
        return fields.ShibuyaField(
            width=self.width,
            height=self.height,
            ratio=self.ratio)

    @default('agents')
    def _default_agents(self):
        agents = Agents(agent_type=self.agent_type)

        group1 = AgentGroup(size=self.size // 2,
                            agent_type=self.agent_type,
                            attributes=self.attributes1)
        group2 = AgentGroup(size=self.size // 2,
                            agent_type=self.agent_type,
                            attributes=self.attributes2)

        agents.add_non_overlapping_group(
            group=group1,
            position_gen=self.field.sample_spawn(0))
        agents.add_non_overlapping_group(
            group=group2,
            position_gen=self.field.sample_spawn(1))

        return agents
