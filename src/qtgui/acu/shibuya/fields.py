from crowddynamics.examples import fields

from shapely.geometry import Polygon, LineString, Point
from shapely.geometry.base import BaseGeometry
from traitlets.traitlets import Float, observe, default, Enum

from crowddynamics.simulation.field import Field


def rectangle(x, y, width, height):
    return Polygon(
        [(x, y), (x + width, y), (x + width, y + height), (x, y + height)])

class ShibuyaField(Field):
    width = 1369.0
    height = 982.0
    ratio = Float(
        default_value=1 / 3,
        min=0, max=1)

    @default('obstacles')
    def _default_obstacles(self):
        return Polygon([(400,553), (416, 370), (437, 333), (610, 324), (615, 338)]) | \
            Polygon([(434, 238), (584, 238), (574, 0), (434, 0) ]) | \
            Polygon([(323, 390), (318, 550), (0, 520), (0, 0), (120, 0), ]) | \
            Polygon([(832, 312), (798, 363), (814, 404), (815, 580), (762, 626), (465, 634), (462, 628), (705, 386), (744, 378), (802, 286), (1212, 0), (1260, 0) ]) | \
            Polygon([(764, 982), (746, 688), (474, 700), (510, 982)])|\
            Polygon([(1369, 492), (1136, 438), (878, 414), (877, 580), (1136, 600), (1369, 662) ])

    @default('targets')
    def _default_targets(self):
        return [LineString([(0, 520), (510, 982)]),
                LineString([(764, 982), (1025, 591)]),
                LineString([(878, 414), (814, 404)]),
                LineString([(744, 378), (584, 238)]),
                LineString([(434, 238), (323, 390)]),
            ]

    @default('spawns')
    def _default_spawns(self):
        return [Polygon([(318, 550), (400, 553), (462, 628), (474, 700)]),
                Polygon([(584, 238), (610, 324), (615, 338), (705, 386)])
        ]

    @default('domain')
    def _default_domain(self):
        return self.convex_hull()

    @observe('width', 'height', 'ratio')
    def _observe_field(self, change):
        obstacles = LineString([(0, 0), (self.width, 0)]) | \
                    LineString([(0, self.height), (self.width, self.height)])
        spawn0 = rectangle(0, 0, self.ratio * self.width, self.height)
        spawn1 = rectangle((1 - self.ratio) * self.width, 0, self.ratio *
                           self.width, self.height)

        target0 = LineString([(0, 0), (0, self.height)])
        target1 = LineString([(self.width, 0), (self.width, self.height)])

        self.obstacles = obstacles
        self.spawns = [spawn0, spawn1]
        self.targets = [target0, target1]
        self.domain = self.convex_hull()