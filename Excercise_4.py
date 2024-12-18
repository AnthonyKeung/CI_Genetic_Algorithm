from random import randint, random
from operator import add
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
    error = []
    for i,member in enumerate(individual):
        error.append(abs(member - target[i]))
    return sum(error)

def grade(pop, target):
    """ Find average fitness for a population."""
    summed = sum(fitness(x, target) for x in pop)
    return summed / (len(pop) * 1.0)

def twos_complement_to_decimal(binary_str):
    if binary_str[0] == '1':
        return -((1 << len(binary_str)) - int(binary_str, 2))
    else:
        return int(binary_str, 2)
    
def binary_decimal(parents):
    decimal_list = []
    for parent in parents:
        decimal = []
        for i in range(int(len(parent)/8)):
            mod_i = i*7
            decimal.append(twos_complement_to_decimal(parent[mod_i : mod_i +7]))
        decimal_list.append(decimal)  
    print(decimal_list)

def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [(fitness(x, target), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]
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
target = [25, 18, 31, -14, 7, -19]
p_count = 1000
i_length = 6
i_min = -100
i_max = 100
generations = 200
convergence_threshold = 0.04
runs = 100
average_generations = []


for run in range(runs):
    p = population(p_count, i_length, i_min, i_max)
    for i in range(generations):
        p = evolve(p, target, mutate=0.1, retain=0.1)
        print("population is",p)
        p = binary_decimal(p)
        current_fitness = grade(p, target)

        if normalised_fitness == 0:
            print(f"Converged after {i} generations.")
            break
        elif normalised_fitness < convergence_threshold:
            print(f"Converged after {i} generations.")
            break
        # fitness_history.append(current_fitness)
    average_generations.append(i)
    print("finished run", run)

print(sum(average_generations) / len(average_generations))



# plt.xlabel('Generations over time')
# plt.ylabel('Average Fitness')
# plt.title('Fitness over Generations')
# plt.plot(fitness_history)
# plt.show()
