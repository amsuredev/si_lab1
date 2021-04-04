from individual import Individual
from _path import Path
from point import Point

class Population:

    def __init__(self, individuals=None, size=10, max_x=0, max_y=0):
        if individuals is None:
            individuals = []
        self.__individuals = individuals
        self.__size = size
        self.__max_x = max_x
        self.__max_y = max_y

    @property
    def individuals(self):
        return self.__individuals

    @individuals.setter
    def individuals(self, individuals):
        self.__individuals = individuals

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

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

    def read_lines(self, path):
        read_file = open(path)
        lines = []
        for line in read_file:
            lines.append(line.replace("\n", ""))
        return lines

    def create_empty_population(self, path="files_input/zad0.txt"):
        lines = self.read_lines(path)
        dimensions = lines[0].split(";")
        self.__max_x = int(dimensions[0]) - 1
        self.__max_y = int(dimensions[1]) - 1

        for i in range(self.__size):
            self.__individuals.append(Individual())
            for j in range(1, len(lines)):
                point_coordinate = [int(coord) for coord in lines[j].split(";")]
                start_x = point_coordinate[0]
                start_y = point_coordinate[1]
                finish_x = point_coordinate[2]
                finish_y = point_coordinate[3]
                self.__individuals[i].path_list.append(Path(start_point=Point(start_x, start_y), finish_point=Point(finish_x, finish_y), max_x=self.max_x, max_y=self.max_y))
        return self.__individuals

    def fill_population(self, probability=70):
        for individual in self.__individuals:
            individual.generate_connectings_to_all_paths(probability)
            individual.print()
