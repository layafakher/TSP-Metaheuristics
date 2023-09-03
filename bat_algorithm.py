import numpy as np
import random
from scipy.spatial import distance_matrix
import time


class BatAlgorithm:
    def __init__(self, D, NP, N_Gen, A, r, Qmin, Qmax, Lower, Upper, function):
        self.D = D  # dimension
        self.solution = np.random.permutation(D)
        self.velocity = np.zeros(D)
        self.NP = NP  # population size
        self.N_Gen = N_Gen  # generations
        self.A = A  # loudness
        self.r = r  # pulse rate
        self.Qmin = Qmin  # frequency min
        self.Qmax = Qmax  # frequency max
        self.Lower = Lower  # lower bound
        self.Upper = Upper  # upper bound
        self.function = function  # fitness function

    def move_bat(self):
        # Initialize the bats
        solutions = np.zeros((self.NP, self.D), dtype=int)
        for i in range(self.NP):
            solutions[i] = np.random.permutation(D)

        # Initialize the velocities and frequencies
        velocities = np.zeros((self.NP, D), dtype=int)
        frequencies = np.zeros(self.NP)
        for i in range(self.NP):
            frequencies[i] = random.uniform(0, 1)

        # Find the best solution
        best_solution = solutions[0]
        best_cost = self.function(self.D, best_solution)
        for i in range(1, self.NP):
            cost = self.function(self.D, solutions[i])
            if cost < best_cost:
                best_solution = solutions[i]
                best_cost = cost

        # Main loop
        for t in range(self.N_Gen):
            for i in range(self.NP):
                # Update the Qmin
                frequencies[i] = self.Qmin + (self.Qmax - self.Qmin) * random.uniform(0, 1)

                # Update the velocity
                np.add(velocities[i], ((solutions[i] - best_solution) * frequencies[i]), out=velocities[i],
                       casting="unsafe")
                # velocities[i] += (solutions[i] - best_solution) * frequencies[i]

                # Update the solution
                solutions[i] = np.argsort(velocities[i])
                if random.uniform(0, 1) > self.r:
                    # Local search
                    j = random.randint(0, D - 1)
                    k = random.randint(0, D - 1)
                    solutions[i][j], solutions[i][k] = solutions[i][k], solutions[i][j]

                # Evaluate the solution
                cost = self.function(self.D, solutions[i])

                # Update the best solution
                if cost < best_cost:
                    best_solution = solutions[i]
                    best_cost = cost

            # Update the A
            self.A *= 0.99

            # Print the best solution
        #     print("Iteration {}: Best Cost = {}".format(t + 1, best_cost))
        # best_solution = np.append(best_solution, best_solution[0])
        # print("Best Solution: {}".format(best_solution))
        out =[
        ]
        out.append((list(best_solution), best_cost))
        return out[0]


def tsp_cost(D, solution):
    return sum(cities[solution[i], solution[(i + 1) % D]] for i in range(D))


def read_cities(path):
    # Read the city's coordinates and create distance matrix
    coords = np.loadtxt(path, usecols=(1, 2))
    dist = distance_matrix(coords, coords)
    return dist


if __name__ == '__main__':
    cities = read_cities("canada-cities.txt")
    D = cities.shape[0]
    NP = 10
    Lower = 0
    Upper = D - 1
    A = 0.9
    r = 0.1
    Qmin = 0
    Qmax = 2
    N_Gen = 100

    ba = BatAlgorithm(D, NP, N_Gen, A, r, Qmin, Qmax, Lower, Upper, tsp_cost)
    st = time.time()
    print(ba.move_bat())
    et = time.time()

    print("Number of iterations :", N_Gen)
    res = et - st
    final_res = res / 60
    print('Runtime : ', final_res, 'minutes')

