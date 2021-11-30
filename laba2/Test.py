import simpy as sp
import numpy as np
import prettytable as pt

from Graphics import plot_histograms, plot_queue_system_probabilities
from Queue import QueueSystem
from Statistics import get_theoretical_info, get_experimental_info


def serve(queue_system: QueueSystem):
    queue_len = queue_system.get_queue_len()
    qn_count = queue_system.get_workload()
    with queue_system.resources.request() as request:
        queue_current_len = queue_system.get_queue_len()
        qn_current_count = queue_system.get_workload()
        queue_system.queue_counts.append(queue_len)
        queue_system.counts.append(queue_len + qn_count)
        if queue_current_len <= queue_system.m:
            start = queue_system.env.now
            response = yield request | queue_system.env.process(queue_system.wait())
            queue_system.queue_times.append(queue_system.env.now - start)
            if request in response:
                yield queue_system.env.process(queue_system.serve())
                queue_system.serve_items.append(queue_current_len + qn_current_count)
            else:
                queue_system.reject_items.append(queue_current_len + qn_current_count)
            queue_system.times.append(queue_system.env.now - start)
        else:
            queue_system.reject_items.append(queue_system.n + queue_system.m + 1)
            queue_system.times.append(0)
            queue_system.queue_times.append(0)


def test_case(n, m, _lambda, mu, v, time, interval_count, _round):
    env = sp.Environment()
    queue_system = QueueSystem(env, n, m, _lambda, mu, v)
    env.process(queue_system.start(serve))
    env.run(until=time)

    theoretical_info = (get_theoretical_info(n, m, _lambda, mu, v))
    experimental_info = (get_experimental_info(queue_system))

    final_probabilities_info = pt.PrettyTable()
    final_probabilities_info.add_column("Теоретические финальные вероятности", np.around(theoretical_info[0], _round))
    final_probabilities_info.add_column("Эмпирические финальные вероятности", np.around(experimental_info[0], _round))
    print(final_probabilities_info)

    plot_histograms(np.around(theoretical_info[0], _round), np.around(experimental_info[0], _round))

    field_names = ["Вероятность образования очереди",
                   "Вероятность отказа",
                   "Относитальная пропускная способность",
                   "Абсолютная пропускная способность",
                   "Среднее число элементов в очереди",
                   "Среднее число элементов в СМО",
                   "Среднее число активных каналов",
                   "Среднее время пребывания элемента в очереди",
                   "Среднее время пребывания элемента в СМО"]

    for index, value in enumerate(field_names):
        info = pt.PrettyTable()
        info.field_names = ["Исследование", value]
        info.add_row(["Теоретическое", np.around(theoretical_info[index + 1], _round)])
        info.add_row(["Эмпирическое", np.around(experimental_info[index + 1], _round)])
        print(info)

    plot_queue_system_probabilities(queue_system, theoretical_info[0], interval_count)


if __name__ == '__main__':
    test_case(2, 10, 10, 5, 1, 6000, 100, 10)