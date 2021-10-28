import Graphics
from MatModel import MatModel
from Statistics import get_interval_empirical_mathematical_expectation, \
    get_interval_empirical_variance, correlation_coefficient, get_points_theoretical_mathematical_expectation, \
    get_points_empirical_mathematical_expectation, get_points_theoretical_variance, get_points_empirical_variance


def draw_graphics(model):
    Graphics.draw_heatmap(model.probability_matrix, model.X, model.Y, 'Теоретическая матрица')
    Graphics.draw_heatmap(model.empirical_probability, model.X, model.Y, 'Эмпирическая матрица')

    count = len(model.discrete_sv)
    vector = [item[0] for item in model.discrete_sv]
    Graphics.draw_histogram(vector, model.X, count, 'Эмпирическая матрица X')

    vector = [item[1] for item in model.discrete_sv]
    Graphics.draw_histogram(vector, model.Y, count, 'Эмпирическая матрица Y')


model = MatModel(3, 3)
draw_graphics(model)

theoretical_expectation = get_points_theoretical_mathematical_expectation(model.probability_matrix, model.X, model.Y)
print('Теоретическое мат ожидание\n', theoretical_expectation)

empirical_expectation = get_points_empirical_mathematical_expectation(model.discrete_sv)
print('Эмпирическое мат ожидание:\n', empirical_expectation)

theoretical_variance = get_points_theoretical_variance(model.probability_matrix, model.X, model.Y,
                                                       theoretical_expectation[0],
                                                       theoretical_expectation[1])
print('Теоретическая дисперсия:\n', theoretical_variance)

empirical_variance = get_points_empirical_variance(model.discrete_sv, empirical_expectation[0], empirical_expectation[1])
print('Эмпирическая дисперсия:\n', empirical_variance)

interval_expectation = get_interval_empirical_mathematical_expectation(model.discrete_sv, empirical_expectation[0],
                                                                       empirical_expectation[1], empirical_variance[0],
                                                                       empirical_variance[1])
print('Интервальная оценка мат ожидание: \n', interval_expectation)

interval_variance = get_interval_empirical_variance(model.discrete_sv, empirical_variance[0], empirical_variance[1])
print('Интервальная оценка дисперсии\n', interval_variance)

theoretical_correlation_coefficient = correlation_coefficient(model.probability_matrix, model.X, model.Y,
                                                              theoretical_expectation[0], theoretical_expectation[1],
                                                              theoretical_variance[0],
                                                              theoretical_variance[1])

print('Теоретический коэффициент корреляции: ', theoretical_correlation_coefficient)

empirical_correlation_coefficient = correlation_coefficient(model.empirical_probability, model.X, model.Y,
                                                            empirical_expectation[0], empirical_expectation[1],
                                                            empirical_variance[0], empirical_variance[1])

print('Эмперический коэффициент корреляции: ', empirical_correlation_coefficient)

if interval_expectation[0][0] < empirical_expectation[0] < interval_expectation[0][1]:
    print('точечная вероятность мат ожидания X попала в интервал')
else:
    print('точечная вероятность мат ожидания X не попала в интервал')

if interval_variance[0][0] < empirical_variance[0] < interval_variance[0][1]:
    print('точечная вероятность дисперсии X попала в интервал')
else:
    print('точечная вероятность дисперсии X не попала в интервал')

if interval_expectation[1][0] < empirical_expectation[1] < interval_expectation[1][1]:
    print('точечная вероятность мат ожидания Y попала в интервал')
else:
    print('точечная вероятность мат ожидания Y не попала в интервал')

if interval_variance[1][0] < empirical_variance[1] < interval_variance[1][1]:
    print('точечная вероятность дисперсии Y попала в интервал')
else:
    print('точечная вероятность дисперсии Y не попала в интервал')
