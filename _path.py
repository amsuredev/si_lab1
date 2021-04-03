from point import Point


class Path:
    def __init__(self, start_point: Point, finish_point: Point, segments=[], connecting_points=[], max_x=0, max_y=0):
        self.__start_point = start_point
        self.__finish_point = finish_point
        self.__segments = segments
        self.__connecting_points = connecting_points
        self.__max_x = max_x
        self.__max_y = max_y

    @property
    def start_point(self):
        return self.__start_point

    @start_point.setter
    def start_point(self, start_point):
        self.__start_point = start_point

    @property
    def finish_point(self):
        return self.__finish_point

    @finish_point.setter
    def finish_point(self):
        return self.__finish_point

    @property
    def segments(self):
        return self.__segments

    @segments.setter
    def segments(self, segments):
        self.__segments = segments

    @property
    def connecting_points(self):
        return self.__connecting_points

    @connecting_points.setter
    def connecting_points(self, connecting_points):
        self.__connecting_points = connecting_points

    @property
    def max_x(self):
        return self.max_x

    @max_x.setter
    def max_x(self, max_x):
        self.__max_x = max_x

    @property
    def max_y(self):
        return self.max_y

    @max_y.setter
    def max_y(self, max_y):
        self.__max_y = max_y