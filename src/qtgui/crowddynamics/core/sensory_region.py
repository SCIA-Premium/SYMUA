import numba
from numba.types import f8, boolean
from numba import typeof

from crowddynamics.core.geom2D import line_intersect
from crowddynamics.core.structures import obstacle_type_linear


@numba.jit([boolean(f8[:], f8[:], typeof(obstacle_type_linear)[:])],
           nopython=True, nogil=True, cache=True)
def is_obstacle_between_points(p0, p1, obstacles):
    """Tests if there is obstacles between the two points p0 and p1."""
    for obstacle in obstacles:
        if line_intersect(p0, p1, obstacle['p0'], obstacle['p1']):
            return True
    return False


@numba.jit([boolean(f8[:], typeof(obstacle_type_linear)[:])],
           nopython=True, nogil=True, cache=True)
def near_obstacle(p0, obstacles):
    """Tests if there is obstacles between the two points p0 and p1."""
    for obstacle in obstacles:
        p1, p2 = obstacle['p0'], obstacle['p1']
        xmin= min(p1[0], p2[0])-0.5
        xmax = max(p1[0], p2[0]) + 0.5
        ymin = min(p1[1], p2[1]) - 0.5
        ymax = max(p1[1], p2[1]) + 0.5
        if xmin < p0[0] < xmax and ymin < p0[1] < ymax:
            print(p0,p1,p2)
            return True
    return False
