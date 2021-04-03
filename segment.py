from enum import Enum


class Segment:
    def __init__(self, direction, step, end_point=None, points=[]):
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


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
