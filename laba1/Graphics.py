from matplotlib import pyplot as plt
import seaborn as sns


def draw_heatmap(matrix, X, Y, title):
    ax = plt.axes()
    sns.heatmap(matrix, xticklabels=Y, yticklabels=X, annot=True, vmin=0, vmax=1, cmap='coolwarm', ax=ax)
    ax.set_title(title)
    plt.show()


def draw_histogram(vector, X, count, title):
    values = [vector.count(x) / count for x in X]
    fig, ax = plt.subplots(1, 1)
    ax.bar(X, values, width=0.1)
    ax.set_title(title)
    plt.show()