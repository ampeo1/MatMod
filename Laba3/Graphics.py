import numpy as np
import matplotlib.pyplot as plt

from QueueSystem import QueueSystem


def plot_queue_system_probabilities(queue_system: QueueSystem, theoretical_probabilities, interval_count):
    intervals = np.array_split(queue_system.counts, interval_count)
    for i in range(1, len(intervals)):
        intervals[i] = np.append(intervals[i], intervals[i - 1])
    for i in range(len(theoretical_probabilities)):
        interval_probabilities = []
        for interval in intervals:
            interval_probabilities.append(len(interval[interval == i]) / len(interval))
        plt.figure(figsize=(5, 5))
        plt.bar(range(len(interval_probabilities)), interval_probabilities)
        plt.title(f"Probabilitiy {i}")
        plt.axhline(y=theoretical_probabilities[i], xmin=0, xmax=len(interval_probabilities), color='red')
        plt.show()


def plot_histograms(theoretical_probabilities, experimental_probabilities):
    plt.style.use('default')
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(25, 5))

    ax1.set_title('Теоретические финальные вероятности')
    ax1.bar(range(len(theoretical_probabilities)), theoretical_probabilities, width=0.2)

    ax2.set_title('Эмпирические финальные вероятности')
    ax2.bar(range(len(experimental_probabilities)), experimental_probabilities, width=0.2)

    ax3.set_title('Финальные вероятности')
    ax3.bar(range(len(theoretical_probabilities)), theoretical_probabilities - experimental_probabilities, width=0.3)
    ax3.axhline(y=0, xmin=0, xmax=len(theoretical_probabilities), color='red')

    plt.show()
