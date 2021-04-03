from enum import Enum
from random import randint, random
from point import Point


class Segment:
    def __init__(self, direction, step, end_point=None, points=None):
        if points is None:
            points = []
        self.__direction = direction
        self.__step = step
        self.__end_point = end_point
        self.__points = points

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, step):
        self.__step = step

    @property
    def end_point(self):
        return self.__end_point

    @end_point.setter
    def end_point(self, end_point):
        self.__end_point = end_point

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, points):
        self.__points = points

    def __str__(self):
        return "direction: {direction} step: {step}, end_point: {end_point}".format(direction=self.__direction,
                                                                                    step=self.__step,
                                                                                    end_point=self.__end_point)

    @classmethod
    def generate_segment(cls, point_from, direction, max_step):
        assert max_step >= 1, "max_step could be greater or equals 1"
        step = randint(1, max_step)  # [a,b]
        if direction == Direction.UP:
            return Segment(direction, step, Point(point_from.x, point_from.y + step))
        elif direction == Direction.DOWN:
            return Segment(direction, step, Point(point_from.x, point_from.y - step))
        elif direction == Direction.LEFT:
            return Segment(direction, step, Point(point_from.x - step, point_from.y))
        else:
            return Segment(direction, step, Point(point_from.x + step, point_from.y))  # right

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    @classmethod
    def random_direction(cls):
        return {0: Direction.UP, 1: Direction.DOWN, 2: Direction.LEFT, 3: Direction.RIGHT}[randint(0, 3)]

    @classmethod
    def smart_random_vert_direction(cls, direction_preference, percent_preference=70):
        satisfy_preference = True if random() < percent_preference / 100 else False  # exactly like this
        if satisfy_preference:
            return direction_preference
        elif direction_preference == Direction.UP:
            return Direction.DOWN
        else:
            return Direction.UP

    @classmethod
    def smart_random_hor_direction(cls, direction_preference, percent_preference=70):
        satisfy_preference = True if random() < percent_preference / 100 else False  # exactly like this
        if satisfy_preference:
            return direction_preference
        elif direction_preference == Direction.LEFT:
            return Direction.RIGHT
        else:
            return Direction.LEFT

    @classmethod
    def direction_orientation(cls, direction):
        return {Direction.UP: "vertical", Direction.DOWN: "vertical", Direction.LEFT: "horisontal",
                Direction.RIGHT: "horisontal"}[direction]

def tests():
    Segment.generate_segment(Point(1, 4), Direction.UP, max_step=6)
    #Segment.generate_segment(Point(1, 4), Direction.UP, max_step=0)

if __name__ == "__main__":
    tests()


