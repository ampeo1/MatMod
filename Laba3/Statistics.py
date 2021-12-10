import numpy as np
import statistics as st

from QueueSystem import QueueSystem


def get_theoretical_final_probabilities(n, _lambda, mu):
    rho = _lambda / mu
    p_0 = (np.sum([(rho ** i) / np.math.factorial(i) for i in range(n)])) ** -1
    final_probabilities = [p_0] + [((rho ** k) / np.math.factorial(k)) * p_0 for k in range(1, n + 1)]

    return final_probabilities


def get_theoretical_reject_probability(n, final_probabilities):
    return final_probabilities[n]


def get_theoretical_relative_bandwidth(reject_probability):
    return 1 - reject_probability


def get_theoretical_absolute_bandwidth(relative_bandwidth, _lambda):
    return relative_bandwidth * _lambda


def get_theoretical_average_active_channal_count(relative_bandwidth, rho):
    return relative_bandwidth * rho


def get_theoretical_info(n, _lambda, mu):
    final_probabilities = get_theoretical_final_probabilities(n, _lambda, mu)
    reject_probability = get_theoretical_reject_probability(n, final_probabilities)
    relative_bandwidth = get_theoretical_relative_bandwidth(reject_probability)
    absolute_bandwidth = get_theoretical_absolute_bandwidth(relative_bandwidth, _lambda)
    average_active_channal_count = get_theoretical_average_active_channal_count(relative_bandwidth, _lambda / mu)

    return final_probabilities, reject_probability, relative_bandwidth, absolute_bandwidth, average_active_channal_count


def get_experimental_final_probabilities(queue_system: QueueSystem):
    items = np.array(queue_system.reject_items + queue_system.serve_items)
    return [(len(items[items == i]) / len(items)) for i in range(1, queue_system.n + 2)]


def get_experimental_queue_probability(queue_system: QueueSystem):
    items = np.array(queue_system.reject_items + queue_system.serve_items)
    return np.sum([(len(items[items == i]) / len(items)) for i in range(1, queue_system.n + 2) if
                   queue_system.n < i < queue_system.n + 1])


def get_experimental_reject_probability(queue_system: QueueSystem):
    items = np.array(queue_system.reject_items + queue_system.serve_items)
    return len(items[items == queue_system.n + 1]) / len(items)


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
    reject_probability = get_experimental_reject_probability(queue_system)
    relative_bandwidth = get_experimental_relative_bandwidth(queue_system)
    absolute_bandwidth = get_experimental_absolute_bandwidth(queue_system)
    average_active_chanal_count = get_experimental_average_active_channal_count(queue_system)

    return final_probabilities, reject_probability, relative_bandwidth, absolute_bandwidth, average_active_chanal_count


def get_theoretical_info_uniform(n, _lambda, mu):
    final_probabilities = get_theoretical_final_probabilities_uniform(n, _lambda, mu)
    reject_probability = get_theoretical_reject_probability(n, final_probabilities)
    relative_bandwidth = get_theoretical_relative_bandwidth(reject_probability)
    absolute_bandwidth = get_theoretical_absolute_bandwidth(relative_bandwidth, _lambda)
    average_active_channal_count = get_theoretical_average_active_channal_count(relative_bandwidth, _lambda / mu)

    return final_probabilities, reject_probability, relative_bandwidth, absolute_bandwidth, average_active_channal_count


def get_theoretical_final_probabilities_uniform(n, _lambda, mu):
    p_ = _lambda / (n * mu)
    p_0 = (1 - p_) / (1 - p_ ** n)
    final_probabilities = [p_0] + [(p_ ** k) * p_0 for k in range(1, n + 1)]

    return final_probabilities