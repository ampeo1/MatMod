import numpy as np


class MatModel:
    n = 3
    m = 3
    X = []
    Y = []
    probability_matrix = []
    empirical_probability = []
    discrete_sv = []

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.X = self.get_vector_with_random_numbers(self.n, 10)
        self.Y = self.get_vector_with_random_numbers(self.m, 10)
        self.probability_matrix = self.get_probability_matrix()
        delta_x = self.get_delta()
        f = self.get_f(delta_x)
        f_x = self.get_f_x(delta_x)
        self.generate_discrete_sv(10, f, f_x)
        self.empirical_probability = self.get_empirical_probability()

    def get_probability_matrix(self):
        probability_vector = np.random.dirichlet(np.ones(self.n * self.m))
        probability_matrix = []
        for i in range(self.n):
            temp_vector = []
            for j in range(self.m):
                temp_vector.append(probability_vector[i * self.n - 1 + j])
            probability_matrix.append(temp_vector)

        return np.array(probability_matrix)

    def get_vector_with_random_numbers(self, size, right_range_random):
        array = []
        while True:
            random_number = np.random.randint(1, right_range_random)
            if random_number not in array:
                array.append(random_number)
                if len(array) == size:
                    return np.sort(np.array(array))

    def get_delta(self):
        delta = []
        row = 0
        for i in range(np.shape(self.probability_matrix)[row]):
            delta = np.append(delta, sum(self.probability_matrix[i]))

        return delta

    def get_f(self, delta):
        return np.array(np.cumsum(delta))

    def get_f_x(self, delta):
        f_x = []
        for n in range(self.n):
            f_x.append([])
            temp_delta = np.cumsum(self.probability_matrix[n])
            for m in range(self.m):
                f_x[-1].append(temp_delta[m] / delta[n])
        return np.array(f_x)

    def generate_discrete_sv(self, n, F, F_x):
        for i in range(n):
            x, y = np.random.uniform(size=2)

            x_index = np.searchsorted(F, x)
            y_index = np.searchsorted(F_x[x_index], y)

            self.discrete_sv.append([self.X[x_index], self.Y[y_index]])

    def get_empirical_probability(self):
        empirical_matrix = np.zeros((self.X.size, self.Y.size))

        for x, y in self.discrete_sv:
            x_index = np.where(self.X == x)
            y_index = np.where(self.Y == y)
            empirical_matrix[x_index, y_index] = self.discrete_sv.count([x, y]) / len(self.discrete_sv)

        return np.array(empirical_matrix)
