from point import Point
from segment import Segment, Direction
from copy import deepcopy


class Path:
    def __init__(self, start_point: Point, finish_point: Point, segments=None, connecting_points=None, max_x=0,
                 max_y=0):
        if segments is None:
            segments = []
        if connecting_points is None:
            connecting_points = []
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

    def generate_connection_between_points(self, cor_direct_probab_pr=70):
        first_rand_direction = self.__generate_first_segment()
        self.__generate_segments(cor_direct_probab_pr, first_rand_direction)
        self.__delete_unnecessary_points()

    def __delete_unnecessary_points(self):
        if self.__connecting_points[-1] != self.__finish_point:
            direction_finish_segment = self.__segments[-1].direction
            if Direction.direction_orientation(direction=direction_finish_segment) == "vertical":
                segment_increase_points = abs(self.get_last_point().y - self.__finish_point.y)
            else:
                segment_increase_points = abs(self.get_last_point().x - self.__finish_point.x)
            self.__segments[-1].step -= segment_increase_points
            self.__connecting_points = self.__connecting_points[:len(self.__connecting_points) - segment_increase_points]
            self.__segments[-1].points = self.__segments[-1].points[:len(self.__segments[-1].points) - segment_increase_points]
            self.__segments[-1].end_point = deepcopy(self.__connecting_points[-1])
        # usunac z pointow finish_point, aby ulatwic obliczenie funkcji oceny
        self.__connecting_points = self.__connecting_points[:len(self.__connecting_points) - 1]

    def __count_max_step(self, direction):
        last_point = self.get_last_point()
        if direction == Direction.UP:
            return self.__max_y - last_point.y
        elif direction == Direction.DOWN:
            return last_point.y
        elif direction == Direction.LEFT:
            return last_point.x
        elif direction == Direction.RIGHT:
            return self.__max_x - last_point.x
        else:
            raise Exception("incorrect value")

    def get_added_points(self, segment: Segment):
        connection_points = []
        last_point = self.get_last_point()
        if segment.direction == Direction.UP:
            for i in range(1, segment.step + 1):
                connection_points.append(Point(last_point.x, last_point.y + i))
        elif segment.direction == Direction.DOWN:
            for i in range(1, segment.step + 1):
                connection_points.append(Point(last_point.x, last_point.y - i))
        elif segment.direction == Direction.LEFT:
            for i in range(1, segment.step + 1):
                connection_points.append(Point(last_point.x - i, last_point.y))
        else:#right
            for i in range(1, segment.step + 1):
                connection_points.append(Point(last_point.x + i, last_point.y))
        return connection_points

    def __generate_first_segment(self):
        rand_direction = Direction.random_direction()
        max_step = 0
        while max_step == 0:
            max_step = self.__count_max_step(rand_direction)
            rand_direction = Direction.random_direction()
        segment_to_add = Segment.generate_segment(point_from=self.start_point, direction=rand_direction,
                                                  max_step=max_step)
        added_points = self.get_added_points(segment_to_add)
        segment_to_add.points = added_points
        self.__segments.append(segment_to_add)
        self.__connecting_points += deepcopy(added_points)
        return rand_direction

    def __generate_segments(self, cor_direct_probab_pr, rand_direction):
        while self.__finish_point not in self.__connecting_points:
            if Direction.direction_orientation(rand_direction) == "horisontal":#last_direction
                direction_probabiltiy = self.__get_direction_preference("vertical", cor_direct_probab_pr)
                rand_direction = Direction.smart_random_vert_direction(direction_probabiltiy[0], direction_probabiltiy[1])
            else:
                direction_probabiltiy = self.__get_direction_preference("horisontal", cor_direct_probab_pr)
                rand_direction = Direction.smart_random_hor_direction(direction_probabiltiy[0], direction_probabiltiy[1])
            max_step = self.__count_max_step(rand_direction)
            while max_step <= 0:
                if Direction.direction_orientation(rand_direction) == "horisontal":  # last_direction
                    direction_probabiltiy = self.__get_direction_preference("horisontal", cor_direct_probab_pr)
                    rand_direction = Direction.smart_random_hor_direction(direction_probabiltiy[0], direction_probabiltiy[1])
                else:
                    direction_probabiltiy = self.__get_direction_preference("vertical", cor_direct_probab_pr)
                    rand_direction = Direction.smart_random_vert_direction(direction_probabiltiy[0], direction_probabiltiy[1])
                max_step = self.__count_max_step(rand_direction)
            segment_to_add = Segment.generate_segment(self.get_last_point(), rand_direction, max_step=max_step)
            added_points = self.get_added_points(segment_to_add)
            segment_to_add.points = added_points
            self.__segments.append(segment_to_add)
            self.__connecting_points += deepcopy(added_points)

    def __get_direction_preference(self, orientation, cor_direct_probab_pr=70):
        last_point = self.get_last_point()
        if orientation == "horisontal":
            result = self.__finish_point.x - last_point.x
            if result == 0:
                return (Direction.RIGHT, 50)
            to_return = (Direction.LEFT, cor_direct_probab_pr) if result < 0 else (Direction.RIGHT, cor_direct_probab_pr)
            return to_return
        else:
            result = self.__finish_point.y - last_point.y
            if result == 0:
                return (Direction.UP, 50)
            to_return = (Direction.DOWN, cor_direct_probab_pr) if result < 0 else (Direction.UP, cor_direct_probab_pr)
            return to_return

    def get_last_point(self):
        if not self.__connecting_points:#empty
            return self.__start_point
        else:
            return self.__connecting_points[-1]


    def print(self):
        print("start point: x={0}, y = {1}".format(self.__start_point.x, self.__start_point.y))
        print("end point: x={0}, y = {1}".format(self.__finish_point.x, self.__finish_point.y))
        for segment in self.__segments:
            print(segment)

