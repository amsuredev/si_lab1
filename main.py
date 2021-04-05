from population import Population


if __name__ == '__main__':
    population = Population(size=10)
    population.create_empty_population('files_input/zad1.txt')
    population.fill_population(70)
    # for individual in population.individuals:
    #     for path in individual.path_list:
    #         path.mutation()
    # print("----------------------------------\nAFTER MUTATION")
    # for individual in population.individuals:
    #     individual.print()
    #     print("OCENA: {ocena}".format(ocena=individual.assessment()))
    #population.start_searching_for_match_individual()
    population.search_rollet()


