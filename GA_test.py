from random import randint, random
from operator import add
import time
import matplotlib.pyplot as plt

def individual(length, min, max):
    """ Create a member of the population."""
    return [randint(min, max) for x in range(length)]

def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).
    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values
    """
    return [individual(length, min, max) for x in range(count)]

def fitness(individual, target):
    """
    Determine the fitness of an individual. Higher is better.
    individual: the individual to evaluate
    target: the target number individuals are aiming for
    """
    sum_values = sum(individual)
    return abs(target - sum_values)

def grade(pop, target):
    """ Find average fitness for a population."""
    summed = sum(fitness(x, target) for x in pop)
    return summed / (len(pop) * 1.0)

def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.2):
    graded = [(fitness(x, target), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]  # sort based on fitness [[60, 68, 75, 62, 68, 83], [60, 68, 75, 62, 68, 83]]
    retain_length = int(len(graded) * retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual) - 1)
            # this mutation is not ideal, because it restricts the range of possible values
            individual[pos_to_mutate] = randint(min(individual), max(individual))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) // 2
            child = male[:half] + female[half:]
            children.append(child)
    parents.extend(children)
    return parents

# Example usage

p_count = 50
i_length = 6
i_min = 0
i_max = 100
generations = 200
convergence_threshold = 0.5  # Define a threshold for early stopping

runs = 2000

generation_average  = []
population_size = []
runt_times = []

z_values = [i / 10.0 for i in range(1,11)]

for z in z_values:  
    start_time = time.time()
    number_of_generations = 0
    for y in range(runs):
        p = population(p_count, i_length, i_min, i_max)
        target = randint(0, 600)
        fitness_history = [grade(p, target)]
        for i in range(generations):
            p = evolve(p, target, z)
            current_fitness = grade(p, target)
            fitness_history.append(current_fitness)
            if current_fitness == 0:
                break
            elif current_fitness < convergence_threshold:
                break
        # if i == generations - 1:
        #     print(f"Failed to converge after {generations} generations.")
        number_of_generations += i
    end_time = time.time()
    print(f"Population size: {z}")

    print(f"Average number of generations to converge: {number_of_generations / runs}")
    generation_average.append(number_of_generations / runs)
    population_size.append(z)
    print(f"Time taken: {end_time - start_time}")
    runt_times.append(end_time - start_time)    

# for datum in fitness_history:
#     print(datum)

plt.title('Retain percentage effect on generations to converge')
plt.xlabel('Retain percentage')
plt.ylabel('Generatisons to converge')
plt.plot(population_size, runt_times, label='Time taken')
plt.plot(population_size, generation_average, label='Generations to converge')
plt.show()
