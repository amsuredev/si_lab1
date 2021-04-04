from population import Population


if __name__ == '__main__':
    population = Population(size=100)
    population.create_empty_population()
    population.fill_population(70)
    for individual in population.individuals:
        for path in individual.path_list:
            path.mutation()
    print("----------------------------------\nAFTER MUTATION")
    for individual in population.individuals:
        individual.print()

