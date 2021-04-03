class Population:

    def __init__(self, individuals=[], size=10, max_x=0, max_y=0):
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