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
    #7 za swoi, 5 z drugimi, 4 za plytu, 2 ili 1 za dlugosc sciezki
    def assessment(self, weight_out_side=4, weight_cross_by_self=2.1, weight_cross_between=10, weight_length_path=0.003,
                   weight_num_segments=0.001):
        assessm_weight_out_side = self.get_points_out_size() * weight_out_side
        assessm_weight_cross_by_self = self.get_cross_by_self() * weight_cross_by_self
        assessm_weight_cross_between = self.get_cross_between() * weight_cross_between
        assessm_weight_length_path = self.get_path_length() * weight_length_path
        assessm_weight_num_segments = self.get_num_segments() * weight_num_segments
        final_assessment = assessm_weight_out_side + assessm_weight_cross_by_self \
                           + assessm_weight_cross_between + assessm_weight_length_path \
                           + assessm_weight_num_segments
        return final_assessment

    def get_points_out_size(self):
        count = 0
        for path in self.__path_list:
            count += path.get_points_out_size()
        return count

    def get_cross_by_self(self):
        count = 0
        for path in self.__path_list:
            count += path.get_cross_by_self()
        return count

    def get_cross_between(self):
        cross_between_count = 0
        index_path_check = 0
        while index_path_check != len(self.__path_list) - 1:  # when last element not compare
            for index_path_check_with in range(index_path_check + 1, len(self.__path_list)):  # compare include last element
                common_points_count = len(set(self.__path_list[index_path_check].connecting_points + [
                    self.__path_list[index_path_check].start_point] + [
                                                  self.__path_list[index_path_check].finish_point]) & set(
                    self.__path_list[index_path_check_with].connecting_points + [
                        self.__path_list[index_path_check_with].start_point] + [
                        self.__path_list[index_path_check_with].finish_point]))  # crosses between two lines
                cross_between_count += common_points_count
            index_path_check += 1  # next path index
        return cross_between_count

    def get_path_length(self):
        path_length = 0
        for path in self.__path_list:
            path_length += path.get_path_length()
        return path_length

    def get_num_segments(self):
        num_segments = 0
        for path in self.__path_list:
            num_segments += path.get_num_segments()
        return num_segments

    def match_individual(self):
        point_out_size = self.get_points_out_size()
        points_cross_by_self = self.get_cross_by_self()
        points_cross_beetween = self.get_cross_between()
        final_grade = point_out_size + points_cross_by_self + points_cross_beetween
        if final_grade == 0:
            return True
        else:
            return False

    def has_minus_in_end_point(self):
        for path in self.__path_list:
            for segment in path.segments:
                if segment.end_point.x < 0 or segment.end_point.y < 0:
                    return True
        return False
