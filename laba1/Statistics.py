import math
import numpy as np
import scipy.stats as sts


def get_points_theoretical_mathematical_expectation(matrix, X, Y):
    delta_x = np.sum(matrix, axis=1)
    delta_y = np.sum(matrix, axis=0)
    expectation_x = sum(delta_x * X)
    expectation_y = sum(delta_y * Y)
    return expectation_x, expectation_y


def get_points_empirical_mathematical_expectation(matrix):
    delta_x = sum([item[0] for item in matrix])
    delta_y = sum([item[1] for item in matrix])
    count = len(matrix)
    expectation_x = delta_x / count
    expectation_y = delta_y / count
    return expectation_x, expectation_y


def get_points_theoretical_variance(matrix, X, Y, m_x, m_y):
    delta_x = np.sum(matrix, axis=1)
    delta_y = np.sum(matrix, axis=0)
    sq_expectation_x = sum(delta_x * (X ** 2))
    sq_expectation_y = sum(delta_y * (Y ** 2))
    variance_x = sq_expectation_x - m_x ** 2
    variance_y = sq_expectation_y - m_y ** 2
    return variance_x, variance_y


def get_points_empirical_variance(discrete_sv, m_x, m_y):
    delta_x = sum([(item[0] - m_x) ** 2 for item in discrete_sv])
    delta_y = sum([(item[1] - m_y) ** 2 for item in discrete_sv])
    count = len(discrete_sv)
    variance_x = delta_x / (count - 1)
    variance_y = delta_y / (count - 1)
    return variance_x, variance_y


def get_interval_empirical_mathematical_expectation(discrete_sv, m_x, m_y, D_x, D_y):
    count = len(discrete_sv)
    tt = sts.t(count - 1)
    arr = tt.rvs(1000000)

    delta = sts.mstats.mquantiles(arr, prob=0.95) * math.sqrt(D_x / (count - 1))
    expectation_x = m_x - delta, m_x + delta

    delta = sts.mstats.mquantiles(arr, prob=0.95) * math.sqrt(D_y / (count - 1))
    expectation_y = m_y - delta, m_y + delta

    return expectation_x, expectation_y


def get_interval_empirical_variance(discrete_2d, D_x, D_y):
    count = len(discrete_2d)
    tt = sts.chi2(count - 1)
    arr = tt.rvs(1000000)

    delta = sts.mstats.mquantiles(arr, prob=[0.01, 0.99])  # # 0.99

    variance_x = (count * D_x / delta[1], count * D_x / delta[0])
    variance_y = (count * D_y / delta[1], count * D_y / delta[0])

    return variance_x, variance_y


def correlation_coefficient(probability_matrix, X, Y, m_x, m_y, D_x, D_y):
    cov = 0
    for i in range(len(X)):
        for j in range(len(Y)):
            cov = cov + (X[i] * Y[j] * probability_matrix[i][j])

    cov -= m_x * m_y
    correlation = cov / np.sqrt(D_x * D_y)
    return correlation
