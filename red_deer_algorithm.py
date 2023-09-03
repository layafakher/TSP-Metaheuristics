import random
import time

import numpy as np
from scipy.spatial import distance_matrix


class RedDeerAlgorithm:
    def __init__(self, num_agents, max_iter, train_data, fitness_function):
        self.num_features = train_data.shape[0]  # number of cities
        self.train_data = train_data  # distance matrix
        self.max_iter = max_iter  # maximum number of generations
        self.num_agents = num_agents  # number of red deer
        self.fitness_function = fitness_function  # the function to maximize while doing feature selection

    def initialize_population(self):
        population = []
        for i in range(self.num_agents):
            path = list(range(self.num_features))
            random.shuffle(path)
            population.append(path)
        return population

    def select_red_deer(self, population):
        fitnesses = [self.fitness_function(path, self.train_data) for path in population]
        total_fitness = sum(fitnesses)
        probabilities = [fitness / total_fitness for fitness in fitnesses]
        r1 = random.choices(population, weights=probabilities)[0]
        r2 = random.choices(population, weights=probabilities)[0]
        return r1, r2

    def generate_fawn(self, r1, r2):
        n = len(r1)
        child = [-1] * n
        start = random.randint(0, n - 1)
        end = random.randint(start, n - 1)
        for i in range(start, end + 1):
            child[i] = r1[i]
        j = 0
        for i in range(n):
            if child[i] == -1:
                while r2[j] in child:
                    j += 1
                child[i] = r2[j]
                j += 1
        return child

    def mutate(self, path):
        n = len(path)
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        path[i], path[j] = path[j], path[i]
        return path

    def rda_run(self):
        distances = self.train_data
        population = self.initialize_population()
        best_path = population[0]
        best_fitness = self.fitness_function(best_path, distances)
        for i in range(self.max_iter):
            new_population = []
            for j in range(self.num_agents):
                r1, r2 = self.select_red_deer(population)
                child = self.generate_fawn(r1, r2)
                if random.random() < 0.1:
                    child = self.mutate(child)
                fitness = self.fitness_function(child, distances)
                if fitness < best_fitness:
                    best_path = child
                    best_fitness = fitness
                new_population.append(child)
            population = new_population
            print("Iteration {}: Best Cost = {}".format(i + 1, best_fitness))
        # return best_path, best_fitness
            out = []
            out.append((list(best_path), best_fitness))
            return out[0] 


def read_cities(path):
    # Read the city's coordinates and create distance matrix
    coords = np.loadtxt(path, usecols=(1, 2))
    dist = distance_matrix(coords, coords)
    return dist


def tsp_cost(path, distances):
    return sum(distances[path[i], path[(i + 1) % len(path)]] for i in range(len(path)))


if __name__ == '__main__':
    max_iterations = 10
    num_agents = 20
    train_data = read_cities("canada-cities.txt")
    rda = RedDeerAlgorithm(num_agents, max_iterations, train_data, tsp_cost)
    st = time.time()

    best_path, best_fitness = rda.rda_run()
    et = time.time()

    print("Best solution:", best_path)
    print("Best cost:", best_fitness)
    print("Number of iterations :", max_iterations)
    res = et - st
    final_res = res / 60
    print('Runtime : ', final_res, 'minutes')
