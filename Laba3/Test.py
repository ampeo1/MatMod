import math

import simpy as sp
import numpy as np
import prettytable as pt

from Graphics import plot_histograms, plot_queue_system_probabilities
from QueueSystem import QueueSystem
from Statistics import get_theoretical_info, get_experimental_info, get_theoretical_info_uniform


def serve_without_assistance(queue_system: QueueSystem):
    qn_count = queue_system.get_workload()
    with queue_system.resources.request() as request:
        qn_current_count = queue_system.get_workload()
        queue_system.counts.append(qn_count)
        if qn_current_count <= queue_system.n:
            response = yield request | queue_system.env.process(queue_system.wait())
            if request in response:
                yield queue_system.env.process(queue_system.serve())
                queue_system.serve_items.append(qn_current_count)
            else:
                queue_system.reject_items.append(qn_current_count + 1)
        else:
            queue_system.reject_items.append(queue_system.n + 1)


def serve_with_uniform_assistance(queue_system: QueueSystem):
    qn_count = queue_system.get_workload()
    with queue_system.resources.request() as request:
        qn_current_count = queue_system.get_workload()
        queue_system.counts.append(qn_count)
        if qn_current_count <= queue_system.n:
            response = yield request | queue_system.env.process(queue_system.wait())
            if request in response:
                queue_system = update_queue(queue_system, qn_current_count)
                yield queue_system.env.process(queue_system.serve())
                queue_system.serve_items.append(qn_current_count)
            else:
                queue_system.reject_items.append(qn_current_count + 1)
        else:
            queue_system.reject_items.append(queue_system.n + 1)


def update_queue(queue_system: QueueSystem, count):
    queue_system.mu = queue_system.default_mu * math.trunc(queue_system.n / count)

    return queue_system


def test_case(n, _lambda, mu, v, time, interval_count, _round, type):
    env = sp.Environment()
    queue_system = QueueSystem(env, n, _lambda, mu, v)
    if type == 'full assistance':
        mu = n * mu
        n = 1
        queue_system = QueueSystem(env, n, _lambda, mu, v)

    if type == 'uniform assistance':
        env.process(queue_system.start(serve_with_uniform_assistance))
    else:
        env.process(queue_system.start(serve_without_assistance))

    env.run(until=time)
    if type == 'uniform assistance':
        theoretical_info = get_theoretical_info_uniform(n, _lambda, mu)
    else:
        theoretical_info = get_theoretical_info(n, _lambda, mu)

    experimental_info = (get_experimental_info(queue_system))

    final_probabilities_info = pt.PrettyTable()
    final_probabilities_info.add_column("Теоретические финальные вероятности", np.around(theoretical_info[0], _round))
    final_probabilities_info.add_column("Эмпирические финальные вероятности", np.around(experimental_info[0], _round))
    print(final_probabilities_info)

    plot_histograms(np.around(theoretical_info[0], _round), np.around(experimental_info[0], _round))

    field_names = ["Вероятность отказа",
                   "Относитальная пропускная способность",
                   "Абсолютная пропускная способность",
                   "Среднее число активных каналов"]

    for index, value in enumerate(field_names):
        info = pt.PrettyTable()
        info.field_names = ["Исследование", value]
        info.add_row(["Теоретическое", np.around(theoretical_info[index + 1], _round)])
        info.add_row(["Эмпирическое", np.around(experimental_info[index + 1], _round)])
        print(info)

    plot_queue_system_probabilities(queue_system, theoretical_info[0], interval_count)


if __name__ == '__main__':
    #test_case(3, 1, 0.5, 2, 6000, 100, 10, 'without assistance')
    #test_case(3, 1, 0.5, 2, 6000, 100, 10, 'full assistance')
    test_case(3, 1, 0.5, 2, 6000, 100, 10, 'uniform assistance')