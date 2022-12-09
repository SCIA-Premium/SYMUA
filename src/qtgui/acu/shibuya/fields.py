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
    out_size = 2
    left = 4

    @default("obstacles")
    def _default_obstacles(self):
        return (
            LineString([(0, self.height), (self.left, self.height)])
            | LineString([(self.left + self.out_size, self.height), (self.width, self.height)])
            | LineString([(0, self.height - self.left), (self.left, self.height - self.left)])
            | LineString(
                [
                    (self.left + self.left, self.height - self.left),
                    (self.width, self.height - self.left),
                ]
            )
            | LineString([(self.left, 0), (self.left, self.height - self.left)])
            | LineString([(self.left + self.left, 0), (self.left + self.left, self.height - self.left)])
        )

    @default("targets")
    def _default_targets(self):
        return [LineString([(self.left, self.height), (self.left + self.out_size, self.height)])]

    @default("spawns")
    def _default_spawns(self):
        return [
            rectangle(0, self.height - self.left, self.left, self.left),
            rectangle(self.left, 0, self.left, self.height - self.left),
            rectangle(
                self.left + self.out_size,
                self.height - self.left,
                self.width - self.out_size - self.left,
                self.left,
            ),
        ]

    @default("domain")
    def _default_domain(self):
        return rectangle(0, 0, self.width, self.height)
