from individual import Individual
from _path import Path
from point import Point
from random import randint, random
from copy import deepcopy

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
            #individual.print()

    def tournament_selection(self, n):
        indexes_of_individuals = []
        selected_individuals_count = 0
        while selected_individuals_count != n:
            random_index = randint(0, len(self.__individuals) - 1)#[a,b]
            if random_index not in indexes_of_individuals:
                indexes_of_individuals.append(random_index)
                selected_individuals_count += 1
        assessment_individuals = []
        for selected_individual_index in indexes_of_individuals:
            assessment_individuals.append(self.__individuals[selected_individual_index].assessment())
        return self.__individuals[indexes_of_individuals[assessment_individuals.index(min(assessment_individuals))]]

    def roulette_selection(self
                           ):
        weights_of_choice = [1 / individual.assessment() for individual in self.__individuals]
        whole_weight = 0
        for weight_of_choice in weights_of_choice:
            whole_weight += weight_of_choice
        probability_of_choice = [weight/whole_weight for weight in weights_of_choice]
        last_interval_end = 0
        intervals = []
        for pr in probability_of_choice:
            intervals.append((last_interval_end, last_interval_end + pr))
            last_interval_end += pr
        rand_pos = random()
        selected_individual = None
        for index_interval in range(len(intervals)):
            if intervals[index_interval][0] <= rand_pos < intervals[index_interval][1]:
                selected_individual = self.__individuals[index_interval]
                break
        return selected_individual

    def cross(self, individual_basis: Individual, individual_donor: Individual, prob_cross=0.97, prob_change_path=0.4):
        prob_cross_random = random()
        if prob_cross_random > prob_cross:
            return None
        new_path_list = []
        for index_path in range(len(individual_basis.path_list)):#[a, b)
            prob_change_path_random = random()
            if prob_change_path_random <= prob_change_path:#change
                new_path_list.append(deepcopy(individual_donor.path_list[index_path]))
            else:
                new_path_list.append(deepcopy(individual_basis.path_list[index_path]))
        return Individual(new_path_list)

    def exists_individual_matches(self):
        for individual in self.__individuals:
            if individual.match_individual():
                return individual
        return None

    # def start_searching_for_match_individual(self):
    #     assessment_best_individuals = []
    #     match_individual = self.exists_individual_matches()
    #     counter_search = 0
    #     count_przepis = len(self.__individuals) // 10
    #     count_parents = len(self.__individuals) // 3
    #     while match_individual is None:
    #         assessment_best_individuals.append(self.tournament_selection(len(self.__individuals)).assessment())
    #         counter_search += 1
    #         new_population = []
    #         for counter in range(count_przepis):
    #             new_population.append(self.roulette_selection())
    #         parents = []
    #         for counter in range(count_parents):
    #             parents.append(self.roulette_selection())
    #         children = []
    #         while len(children) != len(self.__individuals) - count_przepis:
    #             child = self.cross(parents[randint(0, len(parents) - 1)], parents[randint(0, len(parents) - 1)])
    #             if child is not None:
    #                 children.append(child)
    #         new_population += children
    #         for individual in new_population:
    #             for path in individual.path_list:
    #                 path.mutation()
    #         self.__individuals = new_population
    #         match_individual = self.exists_individual_matches()
    #     print(counter_search)
    #     print("success")
    #     print("found individual")
    #     match_individual.print()

    def start_search_new(self):
        match_individual = self.exists_individual_matches()
        iterations = 0
        assessment_best_individuals = []
        while match_individual is None:
            iterations += 1
            new_population = []
            parents_count = len(self.__individuals) // 3
            parents = []
            while len(parents) != parents_count:
                #new_parent = self.tournament_selection(len(self.__individuals) // 3)
                new_parent = self.roulette_selection()
                if new_parent not in parents:
                    parents.append(new_parent)
            while len(new_population) != len(self.__individuals) - 1:
                child = self.cross(parents[randint(0, len(parents) - 1)], parents[randint(0, len(parents) - 1)])
                if child is not None:
                    new_population.append(child)
            for individual in new_population:
                for path in individual.path_list:
                    path.mutation()
            last_best_individual = self.tournament_selection(len(self.__individuals))
            last_bes_individual_copy = deepcopy(last_best_individual)
            for path in last_best_individual.path_list:
                path.mutation()

            if last_best_individual.assessment() < last_bes_individual_copy.assessment():
                best_result = last_best_individual
            else:
                best_result = last_bes_individual_copy
            new_population.append(best_result)
            self.__individuals = new_population
            new_best_individual = self.tournament_selection(len(self.__individuals))
            assessment_best_individuals.append(new_best_individual.assessment())
            match_individual = self.exists_individual_matches()
        print(iterations)
        match_individual.print()

    def search_rollet(self, generation_num_stop=20, pr_mutation=0.1, turn_size=0.2, prob_cross=0.97, prob_change_path=0.4):
        match_individual = self.exists_individual_matches()
        num_of_generation = 0
        assessment_best_individuals = []
        while match_individual is None and num_of_generation != generation_num_stop:
            num_of_generation += 1
            new_population = []
            while len(new_population) != len(self.__individuals) - 1:
                mom = self.tournament_selection(turn_size * len(self.__individuals))
                dad = self.tournament_selection(turn_size * len(self.__individuals))
                child = self.cross(dad, mom, prob_cross, prob_change_path)
                if child is not None:
                    for path in child.path_list:
                        path.mutation(pr_mutation)
                    new_population.append(child)
            last_best_individual = self.tournament_selection(len(self.__individuals))
            last_bes_individual_copy = deepcopy(last_best_individual)
            for path in last_best_individual.path_list:
                path.mutation(0.3)
            if last_best_individual.assessment() < last_bes_individual_copy.assessment():
                best_result = last_best_individual
            else:
                best_result = last_bes_individual_copy
            new_population.append(best_result)
            self.__individuals = new_population
            new_best_individual = self.tournament_selection(len(self.__individuals))
            assessment_best_individuals.append(new_best_individual.assessment())
            match_individual = self.exists_individual_matches()
        print("found")
        print("Assessment list: {}".format(assessment_best_individuals))
        print("Num of generation {}".format(num_of_generation))
        print("Best individual assessment {}".format(assessment_best_individuals[-1]))




