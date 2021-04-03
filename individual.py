class Individual:
    def __init__(self, path_list=None):
        if path_list is None:
            path_list = []
        self.__path_list = path_list

    @property
    def path_list(self):
        return self.__path_list

    @path_list.setter
    def path_list(self, path_list):
        self.__path_list = path_list

    def generate_connectings_to_all_paths(self, probability=70):
        for path_index in range(0, len(self.__path_list)):
            self.__path_list[path_index].generate_connection_between_points(probability)

    def print(self):
        print("------Individual-------")
        for path in self.__path_list:
            path.print()
