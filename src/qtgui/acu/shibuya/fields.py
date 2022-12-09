from crowddynamics.examples import fields

from shapely.geometry import Polygon, LineString, Point
from shapely.geometry.base import BaseGeometry
from traitlets.traitlets import Float, observe, default, Enum

from crowddynamics.simulation.field import Field


def rectangle(x, y, width, height):
    return Polygon([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])


class ShibuyaField(Field):
    width = 30
    height = 20
    out_size = 5
    left = 4

    @default("obstacles")
    def _default_obstacles(self):
        return (
            LineString([(0, self.height), (self.left, self.height)])
            | LineString([(self.left + self.out_size, self.height), (self.width, self.height)])
            | LineString([(0, self.height - self.out_size), (self.left, self.height - self.out_size)])
            | LineString(
                [
                    (self.left + self.out_size, self.height - self.out_size),
                    (self.width, self.height - self.out_size),
                ]
            )
            | LineString([(self.left, 0), (self.left, self.height - self.out_size)])
            | LineString([(self.left + self.out_size, 0), (self.left + self.out_size, self.height - self.out_size)])
        )

    @default("targets")
    def _default_targets(self):
        return [LineString([(self.left, self.height), (self.left + self.out_size, self.height)])]

    @default("spawns")
    def _default_spawns(self):
        return [
            rectangle(0, self.height - self.out_size, self.left, self.out_size),
            rectangle(self.left, 0, self.out_size, self.height - 2 * self.out_size),
            rectangle(self.left + self.out_size, self.height - self.out_size, self.width - self.out_size self.left, self.out_size),
        ]

    @default("domain")
    def _default_domain(self):
        return rectangle(0, 0, self.width, self.height)
