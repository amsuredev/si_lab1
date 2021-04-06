from population import Population, Individual


if __name__ == '__main__':
    def start_rand(size=50, generation_num=20):
        assessments = []
        for i in range(generation_num):
            assessments.append(rand(size))
        print("najlepszy osobnik: {}".format(min(assessments)))

    def rand(size):
        population = Population(size=size)
        population.create_empty_population('files_input/zad1.txt')
        population.fill_population(70)
        individual = population.tournament_selection(len(population.individuals))
        return individual.assessment()


    def start_population(size=50, generation_num=20, turn_size=0.2, prob_change_path=0.4, pr_mutation=0.1):
        population = Population(size=size)
        population.create_empty_population('files_input/zad1.txt')
        population.fill_population(70)
        population.search_rollet(generation_num_stop=generation_num, turn_size=turn_size, prob_change_path=prob_change_path, pr_mutation=pr_mutation)

    print("--------------------------")
    print("prob_mutation=0.1")
    for i in range(5):
        start_population(turn_size=0.2)

    print("--------------------------")
    print("prob_mutation=0.4")
    for i in range(5):
        start_population(turn_size=0.2)

    print("--------------------------")
    print("pr_mutation=0.8")
    for i in range(5):
        start_population(turn_size=0.3)



    # print("Analiza metody losowej")
    # print("--------------------------")
    # print("standart 1")
    # for i in range(5):
    #     start_rand()
    # print("--------------------------")
    # print("standart 2")
    # for i in range(5):
    #     start_rand()
    # print("--------------------------")
    # print("standart 3")
    # for i in range(5):
    #     start_rand()

