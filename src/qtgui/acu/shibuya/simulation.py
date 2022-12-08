from pathlib import Path

from PIL import Image
import numpy as np
from traitlets.traitlets import default

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


class ShibuyaSimple(Hallway):
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
                    AgentAgentInteractions(self),
                    AgentObstacleInteractions(self),
                )
            )
        )
