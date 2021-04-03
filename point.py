class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    def __eq__(self, other):
        return self.__x == other.x and self.__y == other.__y

    def __hash__(self):
        return hash((self.__x, self.__y))

    def __str__(self):
        return "x: {0}, y: {1}".format(self.__x, self.__y)


def tests():
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(2, 3)
    if p1 != p2 or p3 == p1:
        print("Incorrect implementation eq Point")
    elif hash(p1) != hash(p2) or hash(p3) == hash(p1):
        print("Incorrect implementation hash Point")
    else:
        print("test passed")

if __name__=="__main__":
    tests()
