import numpy as np
import statistics as st

from Queue import QueueSystem


def get_theoretical_final_probabilities(n, m, _lambda, mu, v):
    rho = _lambda / mu
    beta = v / mu
    p_0 = (np.sum([(rho ** i) / np.math.factorial(i) for i in range(n + 1)]) + ((rho ** n) / np.math.factorial(n)) * (
        np.sum([(rho ** i) / (np.prod([n + l * beta for l in range(1, i + 1)])) for i in range(1, m + 1)]))) ** -1
    final_probabilities = [p_0] + [((rho ** k) / np.math.factorial(k)) * p_0 for k in range(1, n + 1)]
    p_n = final_probabilities[-1]
    final_probabilities += [((rho ** i) / (np.prod([n + l * beta for l in range(1, i + 1)]))) * p_n for i in
                            range(1, m + 1)]
    return final_probabilities


def get_theoretical_queue_probability(n, m, final_probabilities):
    return np.sum([final_probabilities[n + i] for i in range(0, m)])


def get_theoretical_reject_probability(n, m, final_probabilities):
    return final_probabilities[n + m]


def get_theoretical_relative_bandwidth(reject_probability):
    return 1 - reject_probability


def get_theoretical_absolute_bandwidth(relative_bandwidth, _lambda):
    return relative_bandwidth * _lambda


def get_theoretical_average_queue_items_count(n, m, final_probabilities):
    return np.sum([i * final_probabilities[n + i] for i in range(1, m + 1)])


def get_theoretical_average_queue_system_items_count(n, m, final_probabilities):
    return np.sum([k * final_probabilities[k]
                   for k in range(1, n + 1)]) + np.sum([(n + i) * final_probabilities[n + i]
                                                        for i in range(1, m + 1)])


def get_theoretical_average_active_channal_count(relative_bandwidth, rho):
    return relative_bandwidth * rho


def get_theoretical_average_queue_items_time(reject_probability, _lambda):
    return reject_probability / _lambda


def get_theoretical_average_queue_system_items_time(average_queue_system_items_count, _lambda):
    return average_queue_system_items_count / _lambda


def get_theoretical_info(n, m, _lambda, mu, v):
    final_probabilities = get_theoretical_final_probabilities(n, m, _lambda, mu, v)
    queue_probability = get_theoretical_queue_probability(n, m, final_probabilities)
    reject_probability = get_theoretical_reject_probability(n, m, final_probabilities)
    relative_bandwidth = get_theoretical_relative_bandwidth(reject_probability)
    absolute_bandwidth = get_theoretical_absolute_bandwidth(relative_bandwidth, _lambda)
    average_queue_items_count = get_theoretical_average_queue_items_count(n, m, final_probabilities)
    average_queue_system_items_count = get_theoretical_average_queue_system_items_count(n, m, final_probabilities)
    average_active_channal_count = get_theoretical_average_active_channal_count(relative_bandwidth, _lambda / mu)
    average_queue_items_time = get_theoretical_average_queue_items_time(average_queue_items_count, _lambda)
    average_queue_system_items_time = get_theoretical_average_queue_system_items_time(average_queue_system_items_count,
                                                                                      _lambda)
    return final_probabilities, queue_probability, reject_probability, relative_bandwidth, absolute_bandwidth, average_queue_items_count, average_queue_system_items_count, average_active_channal_count, average_queue_items_time, average_queue_system_items_time


def get_experimental_final_probabilities(queue_system: QueueSystem):
    items = np.array(queue_system.reject_items + queue_system.serve_items)
    return [(len(items[items == i]) / len(items)) for i in range(1, queue_system.n + queue_system.m + 2)]


def get_experimental_queue_probability(queue_system: QueueSystem):
    items = np.array(queue_system.reject_items + queue_system.serve_items)
    return np.sum([(len(items[items == i]) / len(items)) for i in range(1, queue_system.n + queue_system.m + 2) if
                   i > queue_system.n and i < queue_system.n + queue_system.m + 1])


def get_experimental_reject_probability(queue_system: QueueSystem):
    items = np.array(queue_system.reject_items + queue_system.serve_items)
    return len(items[items == queue_system.n + queue_system.m + 1]) / len(items)


def get_experimental_relative_bandwidth(queue_system: QueueSystem):
    return 1 - get_experimental_reject_probability(queue_system)


def get_experimental_absolute_bandwidth(queue_system: QueueSystem):
    return get_experimental_relative_bandwidth(queue_system) * queue_system._lambda


def get_experimental_average_queue_items_count(queue_system: QueueSystem):
    return st.mean(queue_system.queue_counts)


def get_experimental_average_queue_system_items_count(queue_system: QueueSystem):
    return st.mean(queue_system.counts)


def get_experimental_average_active_channal_count(queue_system: QueueSystem):
    return get_experimental_relative_bandwidth(queue_system) * queue_system._lambda / queue_system.mu


def get_experimental_average_queue_items_time(queue_system: QueueSystem):
    return st.mean(queue_system.queue_times)


def get_experimental_average_queue_system_items_time(queue_system: QueueSystem):
    return st.mean(queue_system.times)


def get_experimental_info(queue_system: QueueSystem):
    final_probabilities = get_experimental_final_probabilities(queue_system)
    queue_probability = get_experimental_queue_probability(queue_system)
    reject_probability = get_experimental_reject_probability(queue_system)
    relative_bandwidth = get_experimental_relative_bandwidth(queue_system)
    absolute_bandwidth = get_experimental_absolute_bandwidth(queue_system)
    average_queue_items_count = get_experimental_average_queue_items_count(queue_system)
    average_queue_system_items_count = get_experimental_average_queue_system_items_count(queue_system)
    average_active_channal_count = get_experimental_average_active_channal_count(queue_system)
    average_queue_items_time = get_experimental_average_queue_items_time(queue_system)
    average_queue_system_items_time = get_experimental_average_queue_system_items_time(queue_system)
    return final_probabilities, queue_probability, reject_probability, relative_bandwidth, absolute_bandwidth, average_queue_items_count, average_queue_system_items_count, average_active_channal_count, average_queue_items_time, average_queue_system_items_time
