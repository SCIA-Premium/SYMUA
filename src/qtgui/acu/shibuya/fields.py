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
        return LineString([(434, 238), (584, 238)]) | \
            LineString([(437, 333), (610, 324)]) | \
            LineString([(584, 238), (574, 0)]) | \
            LineString([(434, 238), (434, 0)]) | \
            LineString([(610, 324), (615, 338)]) | \
            LineString([(323, 390), (318, 550)]) | \
            LineString([(318, 550), (0, 520)]) | \
            LineString([(615, 338), (400, 553)]) | \
            LineString([(400, 553), (416, 370)]) | \
            LineString([(416, 370), (437, 333)]) | \
            LineString([(762, 626),(465, 634) ]) | \
            LineString([(465, 634), (462, 628)]) | \
            LineString([(462, 628), (705, 386)])|\
            LineString([(815, 580), (762, 626)])|\
            LineString([(705, 386), (744, 378)])|\
            LineString([(744, 378), (802, 286)])| \
            LineString([(802, 286), (1212, 0)])|\
            LineString([(1260, 0), (832, 312)])|\
            LineString([(832, 312), (798, 363)])|\
            LineString([(798, 363), (814, 404)])|\
            LineString([(814, 404), (815, 580)])|\
            LineString([(323, 390), (120, 390)])|\
            LineString([(120, 390), (120, 0)])|\
            LineString([(474, 700), (510, 982)])|\
            LineString([(474, 700), (746, 688)])|\
            LineString([(746, 688), (764, 982)])|\
            LineString([(877, 580), (1136, 600)])|\
            LineString([(1136, 600), (1369, 662)])|\
            LineString([(877, 580), (878, 414)])|\
            LineString([(878, 414), (1136, 438)])|\
            LineString([(1136, 438), (1369, 492)])

    @default('targets')
    def _default_targets(self):
        return [LineString([(0, 520), (510, 982)]),
                # LineString([(764, 982), (1025, 591)]),
                # LineString([(878, 414), (814, 404)]),
                # LineString([(744, 378), (584, 238)]),
                LineString([(434, 238), (323, 390)]),
            ]

    @default('spawns')
    def _default_spawns(self):
        return [Polygon([(318, 550), (400, 553), (462, 628), (474, 700)])]

    @default('domain')
    def _default_domain(self):
        return self.convex_hull()
