from crowddynamics.examples import fields

from shapely.geometry import Polygon, LineString, Point
from shapely.geometry.base import BaseGeometry
from traitlets.traitlets import Float, observe, default, Enum

from crowddynamics.simulation.field import Field


def rectangle(x, y, width, height):
    return Polygon([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])


class ItaewonField(Field):
    width = 30
    height = 20
    out_size = 2
    left = 4
    offset: float = 0.3

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
            rectangle(
                self.offset,
                self.height - self.left + self.offset,
                self.left - 2 * self.offset,
                self.left - 2 * self.offset,
            ),
            rectangle(
                self.left + self.offset,
                self.offset,
                self.left - 2 * self.offset,
                self.height - self.left - 2 * self.offset,
            ),
            rectangle(
                self.left + self.out_size + self.offset,
                self.height - self.left + self.offset,
                self.width - self.out_size - self.left - 2 * self.offset,
                self.left - 2 * self.offset,
            ),
        ]

    @default("domain")
    def _default_domain(self):
        return rectangle(0, 0, self.width, self.height)
