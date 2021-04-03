class Individual:
    def __init__(self, path_list=[]):
        self.__path_list = path_list

    @property
    def path_list(self):
        return self.__path_list

    @path_list.setter
    def path_list(self, path_list):
        self.__path_list = path_list
