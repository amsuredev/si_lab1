from point import Point
from segment import Segment, Direction
from copy import deepcopy
from random import random


class Path:
    def __init__(self, start_point: Point, finish_point: Point, segments=None, connecting_points=None, max_x=0,
                 max_y=0):
        self.__start_point = start_point
        self.__finish_point = finish_point
        if segments is None:
            self.__segments = []
        if connecting_points is None:
            self.__connecting_points = []
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
    def finish_point(self, finish_point):
        self.__finish_point = finish_point

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
        return self.__max_x

    @max_x.setter
    def max_x(self, max_x):
        self.__max_x = max_x

    @property
    def max_y(self):
        return self.__max_y

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
            self.__connecting_points = self.__connecting_points[
                                       :len(self.__connecting_points) - segment_increase_points]
            self.__segments[-1].points = self.__segments[-1].points[
                                         :len(self.__segments[-1].points) - segment_increase_points]
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
        else:  # right
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
            if Direction.direction_orientation(rand_direction) == "horisontal":  # last_direction
                direction_probabiltiy = self.__get_direction_preference("vertical", cor_direct_probab_pr)
                rand_direction = Direction.smart_random_vert_direction(direction_probabiltiy[0],
                                                                       direction_probabiltiy[1])
            else:
                direction_probabiltiy = self.__get_direction_preference("horisontal", cor_direct_probab_pr)
                rand_direction = Direction.smart_random_hor_direction(direction_probabiltiy[0],
                                                                      direction_probabiltiy[1])
            max_step = self.__count_max_step(rand_direction)
            while max_step <= 0:
                if Direction.direction_orientation(rand_direction) == "horisontal":  # last_direction
                    direction_probabiltiy = self.__get_direction_preference("horisontal", cor_direct_probab_pr)
                    rand_direction = Direction.smart_random_hor_direction(direction_probabiltiy[0],
                                                                          direction_probabiltiy[1])
                else:
                    direction_probabiltiy = self.__get_direction_preference("vertical", cor_direct_probab_pr)
                    rand_direction = Direction.smart_random_vert_direction(direction_probabiltiy[0],
                                                                           direction_probabiltiy[1])
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
            to_return = (Direction.LEFT, cor_direct_probab_pr) if result < 0 else (
            Direction.RIGHT, cor_direct_probab_pr)
            return to_return
        else:
            result = self.__finish_point.y - last_point.y
            if result == 0:
                return (Direction.UP, 50)
            to_return = (Direction.DOWN, cor_direct_probab_pr) if result < 0 else (Direction.UP, cor_direct_probab_pr)
            return to_return

    def get_last_point(self):
        if not self.__connecting_points:  # empty
            return self.__start_point
        else:
            return self.__connecting_points[-1]

    def print(self):
        print("start point: x={0}, y = {1}".format(self.__start_point.x, self.__start_point.y))
        print("end point: x={0}, y = {1}".format(self.__finish_point.x, self.__finish_point.y))
        for segment in self.__segments:
            print(segment)

    def mutation(self, prob_mutate=0.4):
        for segment in self.__segments:
            do_mutation = random() < prob_mutate
            if do_mutation:
                orient_cur_seg = Direction.direction_orientation(segment.direction)
                if orient_cur_seg == "vertical":  # horizontal mutation
                    mutation_direction = Direction.get_random_hor_direction()
                    self.__move_hor_segment(mutation_direction, segment)
                else:  # vertical mutation
                    mutation_direction = Direction.get_random_vert_direction()
                    self.__move_vert_segment(mutation_direction, segment)
                self.__repair()
                if self.__capture_end_point():
                    self.__cut_path()
                    self.__renew_connection_points()
                    return
                self.__renew_connection_points()

    def __renew_connection_points(self):
        self.__connecting_points = []
        for segment in self.__segments:
            for point in segment.points:
                self.__connecting_points.append(Point(point.x, point.y))
        self.__connecting_points = self.__connecting_points[:len(self.__connecting_points) - 1]  # obciac ostatni punkt

    def __get_index_of_segment(self, segment):
        for index in range(len(self.__segments)):
            if self.__segments[index] is segment:
                return index
        raise Exception("Segment not in path")

    def __move_hor_segment(self, mutation_direction, segment):
        cur_seg_index = self.__get_index_of_segment(segment)
        if cur_seg_index != 0 and cur_seg_index != len(self.__segments) - 1:  # segment not last not first
            self.__hor_move_not_last_not_first(cur_seg_index, mutation_direction)
        elif cur_seg_index == 0 and cur_seg_index != len(self.__segments) - 1:  # segment first not last
            self.__hor_move_first_not_last(mutation_direction)
        elif cur_seg_index == 0 and cur_seg_index == len(self.__segments) - 1:  # segment first and last
            self.__hor_move_first_and_last(mutation_direction)
        else:  # not first and last
            self.__hor_move_last_not_first(mutation_direction)

    def __move_vert_segment(self, mutation_direction, segment):
        cur_seg_index = self.__get_index_of_segment(segment)
        if cur_seg_index != 0 and cur_seg_index != len(self.__segments) - 1:  # segment not last not first
            self.__vert_move_not_last_not_first(cur_seg_index, mutation_direction)
        elif cur_seg_index == 0 and cur_seg_index != len(self.__segments) - 1:  # segment first not last
            self.__vert_move_first_not_last(mutation_direction)
        elif cur_seg_index == 0 and cur_seg_index == len(self.__segments) - 1:  # segment first and last
            self.__vert_move_first_and_last(mutation_direction)
        else:  # not first but last
            self.__vert_move_last_not_first(mutation_direction)

    def __move_on_x_segment(self, cur_seg_index, offset_x_move_all_points):
        for index in range(len(self.__segments[cur_seg_index].points)):
            point_before_mutation = self.__segments[cur_seg_index].points[index]
            self.__segments[cur_seg_index].points[index] = Point(point_before_mutation.x + offset_x_move_all_points,
                                                                 point_before_mutation.y)  # create new objects, makes more safety
        self.__segments[cur_seg_index].end_point = deepcopy(self.__segments[cur_seg_index].points[-1])

    def __move_on_y_segment(self, cur_seg_index, offset_y_move_all_points):
        for index in range(len(self.__segments[cur_seg_index].points)):
            point_before_mutation = self.__segments[cur_seg_index].points[index]
            self.__segments[cur_seg_index].points[index] = Point(point_before_mutation.x,
                                                                 point_before_mutation.y + offset_y_move_all_points)  # create new objects, makes more safety
        self.__segments[cur_seg_index].end_point = deepcopy(self.__segments[cur_seg_index].points[-1])

    def __hor_move_not_last_not_first(self, cur_seg_index, mutation_direction):
        offset_x_move_all_points = 1 if mutation_direction == Direction.RIGHT else -1
        self.__move_on_x_segment(cur_seg_index, offset_x_move_all_points)
        before_segment = self.__segments[cur_seg_index - 1]
        self.__move_before_segment_hor(mutation_direction, before_segment, offset_x_move_all_points)
        after_segment = self.__segments[cur_seg_index + 1]
        self.__move_after_segment_hor(mutation_direction, after_segment)

    def __vert_move_not_last_not_first(self, cur_seg_index, mutation_direction):
        offset_y_move_all_points = 1 if mutation_direction == Direction.UP else -1
        self.__move_on_y_segment(cur_seg_index, offset_y_move_all_points)
        before_segment = self.__segments[cur_seg_index - 1]
        self.__move_before_segment_vert(mutation_direction, before_segment, offset_y_move_all_points)
        after_segment = self.__segments[cur_seg_index + 1]
        self.__move_after_segment_vert(mutation_direction, after_segment)

    def __move_before_segment_hor(self, mutation_direction, before_segment, offset_x_move_all_points):
        if mutation_direction == before_segment.direction:
            new_last_point = Point(before_segment.end_point.x + offset_x_move_all_points, before_segment.end_point.y)
            before_segment.points.append(new_last_point)
            before_segment.end_point = Point(new_last_point.x, new_last_point.y)
            before_segment.step += 1
        else:
            before_segment.points = before_segment.points[:-1]
            before_segment.step -= 1
            if len(before_segment.points) != 0:
                before_segment.end_point = deepcopy(before_segment.points[-1])
            else:
                before_segment.end_point = None

    def __move_before_segment_vert(self, mutation_direction, before_segment, offset_y_move_all_points):
        if mutation_direction == before_segment.direction:
            new_last_point = Point(before_segment.end_point.x, before_segment.end_point.y + offset_y_move_all_points)
            before_segment.points.append(new_last_point)
            before_segment.end_point = Point(new_last_point.x, new_last_point.y)
            before_segment.step += 1
        else:
            before_segment.points = before_segment.points[:-1]
            before_segment.step -= 1
            if len(before_segment.points) != 0:
                before_segment.end_point = deepcopy(before_segment.points[-1])
            else:
                before_segment.end_point = None

    def __move_after_segment_hor(self, mutation_direction, after_segment):
        if mutation_direction == after_segment.direction:  # after segment direction equals move -> cut
            after_segment.points.pop(0)
            after_segment.step -= 1
            if len(after_segment.points) == 0:
                after_segment.end_point = None
        else:  # after segment direction not equals move -> append element to the beginning
            x_offset = -1 if after_segment.direction == Direction.RIGHT else 1  # correct
            point_insert = Point(after_segment.points[0].x + x_offset, after_segment.points[0].y)
            after_segment.points.insert(0, point_insert)
            after_segment.step += 1

    def __move_after_segment_vert(self, mutation_direction, after_segment):
        if mutation_direction == after_segment.direction:  # after segment direction equals move -> cut
            after_segment.points.pop(0)
            after_segment.step -= 1
            if len(after_segment.points) == 0:
                after_segment.end_point = None
        else:  # after segment direction not equals move -> append element to the beginning
            y_offset = -1 if after_segment.direction == Direction.UP else 1
            point_insert = Point(after_segment.points[0].x, after_segment.points[0].y + y_offset)
            after_segment.points.insert(0, point_insert)
            after_segment.step += 1

    def __hor_move_first_not_last(self, mutation_direction):
        offset_x_move_all_points = 1 if mutation_direction == Direction.RIGHT else -1
        self.__move_on_x_segment(cur_seg_index=0, offset_x_move_all_points=offset_x_move_all_points)
        after_segment = self.__segments[1]
        self.__move_after_segment_hor(mutation_direction, after_segment=after_segment)
        new_first_segment = self.__hor_create_new_first_segment(mutation_direction, offset_x_move_all_points)
        self.__segments.insert(0, new_first_segment)

    def __vert_move_first_not_last(self, mutation_direction):
        offset_y_move_all_points = 1 if mutation_direction == Direction.UP else -1
        self.__move_on_y_segment(cur_seg_index=0, offset_y_move_all_points=offset_y_move_all_points)
        after_segment = self.__segments[1]
        self.__move_after_segment_vert(mutation_direction=mutation_direction, after_segment=after_segment)
        new_first_segment = self.__vert_create_new_first_segment(mutation_direction, offset_y_move_all_points)
        self.__segments.insert(0, new_first_segment)

    def __hor_create_new_first_segment(self, mutation_direction, offset_x_move_all_points):
        point_first_segment = Point(self.__start_point.x + offset_x_move_all_points, self.__start_point.y)
        new_first_segment = Segment(direction=mutation_direction, step=1,
                                    end_point=Point(point_first_segment.x, point_first_segment.y))
        new_first_segment.points.append(Point(point_first_segment.x, point_first_segment.y))
        return new_first_segment

    def __vert_create_new_first_segment(self, mutation_direction, offset_y_move_all_points):
        point_first_segment = Point(self.__start_point.x, self.__start_point.y + offset_y_move_all_points)
        new_first_segment = Segment(direction=mutation_direction, step=1,
                                    end_point=Point(point_first_segment.x, point_first_segment.y))
        new_first_segment.points.append(Point(point_first_segment.x, point_first_segment.y))
        return new_first_segment

    def __hor_move_first_and_last(self, mutation_direction):
        offset_x_move_all_points = 1 if mutation_direction == Direction.RIGHT else -1
        self.__move_on_x_segment(cur_seg_index=0, offset_x_move_all_points=offset_x_move_all_points)
        new_first_segment = self.__hor_create_new_first_segment(mutation_direction, offset_x_move_all_points)
        self.__segments.insert(0, new_first_segment)
        new_last_segment = self.__hor_create_new_last_segment(mutation_direction)
        self.__segments.append(new_last_segment)

    def __vert_move_first_and_last(self, mutation_direction):
        offset_y_move_all_points = 1 if mutation_direction == Direction.UP else -1
        self.__move_on_y_segment(cur_seg_index=0, offset_y_move_all_points=offset_y_move_all_points)
        new_first_segment = self.__vert_create_new_first_segment(mutation_direction, offset_y_move_all_points)
        self.__segments.insert(0, new_first_segment)
        new_last_segment = self.__vert_create_new_last_segment(mutation_direction)
        self.__segments.append(new_last_segment)

    def __hor_create_new_last_segment(self, mutation_direction):
        point_last_segment = Point(self.__finish_point.x, self.__finish_point.y)
        new_last_segment = Segment(direction=Direction.opposite_direction(mutation_direction), step=1,
                                   end_point=Point(point_last_segment.x, point_last_segment.y))
        new_last_segment.points.append(Point(point_last_segment.x, point_last_segment.y))
        return new_last_segment

    def __hor_move_last_not_first(self, mutation_direction):
        offset_x_move_all_points = 1 if mutation_direction == Direction.RIGHT else -1
        self.__move_on_x_segment(cur_seg_index=-1, offset_x_move_all_points=offset_x_move_all_points)
        before_segment = self.__segments[-2]
        self.__move_before_segment_hor(mutation_direction, before_segment, offset_x_move_all_points)
        new_after_segment = self.__hor_create_new_last_segment(mutation_direction)
        self.__segments.append(new_after_segment)

    def __vert_move_last_not_first(self, mutation_direction):
        offset_y_move_all_points = 1 if mutation_direction == Direction.UP else -1
        self.__move_on_y_segment(cur_seg_index=-1, offset_y_move_all_points=offset_y_move_all_points)
        before_segment = self.__segments[-2]
        self.__move_before_segment_vert(mutation_direction, before_segment, offset_y_move_all_points)
        new_last_segment = self.__vert_create_new_last_segment(mutation_direction)
        self.__segments.append(new_last_segment)

    def __vert_create_new_last_segment(self, mutation_direction):
        point_last_segment = Point(self.__finish_point.x, self.__finish_point.y)
        new_last_segment = Segment(direction=Direction.opposite_direction(mutation_direction), step=1,
                                   end_point=Point(point_last_segment.x, point_last_segment.y))
        new_last_segment.points.append(Point(point_last_segment.x, point_last_segment.y))
        return new_last_segment

    def __exist_segments_with_step_zero(self):
        for segment in self.__segments:
            if segment.step == 0:
                return True
        return False

    def __one_segment_orientation_consistently(self):
        last_orientation = None
        for segment in self.__segments:
            if last_orientation is None:
                last_orientation = Direction.direction_orientation(segment.direction)
                continue
            else:
                if last_orientation == Direction.direction_orientation(segment.direction):
                    return True
                else:
                    last_orientation = Direction.direction_orientation(segment.direction)
        return False

    def __repair(self):
        while self.__exist_segments_with_step_zero() or self.__one_segment_orientation_consistently():
            for segment in self.__segments:
                if segment.step == 0:
                    self.__segments.remove(segment)
            last_orientation = None
            for segment in self.__segments:
                current_orientation = Direction.direction_orientation(segment.direction)
                if last_orientation is None:
                    last_orientation = current_orientation
                    continue
                if current_orientation == last_orientation:
                    before_segment = self.__segments[self.__get_index_of_segment(segment) - 1]
                    if segment.direction == before_segment.direction:
                        before_segment.step += segment.step
                        before_segment.points += deepcopy(segment.points)
                        before_segment.end_point = deepcopy(before_segment.points[-1])  # new
                        self.__segments.pop(self.__get_index_of_segment(segment))
                        self.__repair()
                        return
                    else:  # different directions
                        if before_segment.step > segment.step:
                            points_num_to_remove = segment.step
                            before_segment.step -= points_num_to_remove
                            before_segment.points = before_segment.points[
                                                    :len(before_segment.points) - points_num_to_remove]
                            before_segment.end_point = deepcopy(before_segment.points[-1])
                            self.__segments.pop(self.__get_index_of_segment(segment))
                            self.__repair()
                            return
                            # continue
                        elif before_segment.step < segment.step:
                            points_num_to_remove = before_segment.step
                            segment.step -= points_num_to_remove
                            segment.points = segment.points[points_num_to_remove:]
                            self.__segments.pop(self.__get_index_of_segment(before_segment))
                            segment.end_point = deepcopy(segment.points[-1])
                            self.__repair()
                            return
                        else:  # segments equal
                            self.__segments.pop(self.__get_index_of_segment(segment))
                            self.__segments.pop(self.__get_index_of_segment(before_segment))
                            self.__repair()
                            return
                            # continue
                last_orientation = current_orientation

    def debug_exist_change_two_coordinates_end_point_of_segment(self):
        if len(self.__segments) <= 1:
            return False
        count = 0
        last_x = None
        last_y = None
        for segment in self.__segments:
            if segment.end_point is None:
                continue
            if count == 0:
                last_x = segment.end_point.x
                last_y = segment.end_point.y
                count += 1
                continue
            if last_x != segment.end_point.x and last_y != segment.end_point.y:
                return True
            last_x = segment.end_point.x
            last_y = segment.end_point.y
            count += 1
        return False

    def __capture_end_point(self):
        for index in range(len(self.__segments) - 1):  # if segment that not last has end point
            if self.__finish_point in self.__segments[index].points:
                return True
        return False

    def __cut_path(self):
        for index in range(len(self.__segments)):
            if self.__finish_point in self.__segments[index].points:
                self.__segments = self.__segments[:index + 1]  # cut until new last include
                index_finish_point = self.__segments[index].points.index(self.__finish_point)
                self.__segments[index].points = self.__segments[index].points[:index_finish_point + 1]
                self.__segments[index].end_point = deepcopy(self.__segments[index].points[-1])
                return
