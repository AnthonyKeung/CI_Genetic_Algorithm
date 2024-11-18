from random import randint, random
from operator import add
import numpy as np
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

def fitness(individual, target, X_test_values):

    errors = []
    for x in X_test_values:
        target_y_value = target[0] * x**5 +target[1] * x**4 + target[2] * x**3 + target[3] * x**2 + target[4] * x + target[5] 
        individual_y_value = individual[0] * x**5 + individual[1] * x**4 + individual[2] * x**3 + individual[3] * x**2 + individual[4] * x + individual[5]
        errors.append(abs(target_y_value - individual_y_value))
    return sum(errors)


def grade(pop, target, X_values):
    """ Find average fitness for a population."""
    summed = sum(fitness(x, target, X_values) for x in pop)
    return summed / (len(pop) * 1.0)

def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.1, X_test_values = np.linspace(-100, 100, 200)):
    graded = [(fitness(x, target, X_test_values), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]
    retain_length = int(len(graded) * retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)


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

    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual) - 1)
            # this mutation is not ideal, because it restricts the range of possible values
            individual[pos_to_mutate] = randint(-100, 100)
    return parents

# Example usage
target = [25, 18, 31, -14, 7, -19]
p_count = 1000
i_length = 6
i_min = -100
i_max = 100
generations = 100
convergence_threshold = 0.04
x_test_values = np.linspace(-100, 100, 10)
error_log = []
average_generations = []


for run in range(1):
    p = population(p_count, i_length, i_min, i_max)
    for i in range(generations):
        p = evolve(p, target, mutate=0.35, retain=0.15, X_test_values=x_test_values)
        current_fitness = grade(p, target, x_test_values)
        error_log.append(current_fitness)
        print(p[0], current_fitness)

        #check for convergence based on fittest individual
        fittest_individual_grade = fitness(p[0],target= target, X_test_values=x_test_values)

        if fittest_individual_grade == 0:
            print(f"Perfect after {i} generations.")
            break
        elif fittest_individual_grade < convergence_threshold:
            print(f"Converged after {i} generations.")
            break
    average_generations.append(i)


print(sum(average_generations) / len(average_generations))



plt.xlabel('Generations over time')
plt.ylabel('Average Fitness')
plt.title('Fitness over Generations')
plt.plot(error_log)
plt.show()
