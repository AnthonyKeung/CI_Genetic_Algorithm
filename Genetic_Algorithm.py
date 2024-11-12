from random import randint, random

# Parameters
TARGET = 42
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
RETENTION_RATE = 0.2
GENERATIONS = 10
CONVERGENCE_THRESHOLD = 1
RANDOM_SELECT = 0.05

# Generate a random individual
def generate_individual():
    return randint(0, 100)

# Calculate fitness of an individual
def calculate_fitness(individual):
    return abs(TARGET - individual)

# Calculate average fitness of a population
def calculate_average_fitness(population):
    return sum([x[1] for x in population]) / len(population)


# Crossover between two parents
def crossover(parent1, parent2):
    return (parent1 + parent2) // 2

# Mutate an individual
def mutate(individual):
    if random() < MUTATION_RATE:
        return generate_individual()
    return individual

# Main genetic algorithm
def genetic_algorithm():
    population = [(generate_individual(), 0) for _ in range(POPULATION_SIZE)]
    for generation in range(GENERATIONS):

        # Calculate fitness of each individual
        for i in range(POPULATION_SIZE):
            population[i] = (population[i][0], calculate_fitness(population[i][0]))

        # Sort population based on fitness  
        population = sorted(population, key=lambda x: x[1])
        average_fitness = calculate_average_fitness(population)

        # Check if the target is reached
        if average_fitness == 0:
                print(f"Perfect fit in Generation {generation}: {average_fitness}")
                break
        elif average_fitness <  CONVERGENCE_THRESHOLD:
                print(f"Convergence found in Generation {generation}: {average_fitness}")
                break
        
        # Retain the best individuals
        sorted_population = sorted(population, key=lambda x: x[1])
        retain_length = int(len(sorted_population) * RETENTION_RATE)

        new_population = []

        # randomly add other individuals to promote genetic diversity
        for individual in sorted_population[retain_length:]:
            if RANDOM_SELECT > random():
                new_population.append(individual)

        while len(new_population) < POPULATION_SIZE:
            new_population.append(crossover(sorted_population[randint(0, retain_length)][0], sorted_population[randint(0, retain_length)][0]))     
    
        for individual in new_population:
            new_population[individual] = mutate(individual)
        
        population = new_population
        print(f"Generation {generation}: {average_fitness}")
        
if __name__ == "__main__":
    result = genetic_algorithm()
    print(f"Optimized number: {result}")