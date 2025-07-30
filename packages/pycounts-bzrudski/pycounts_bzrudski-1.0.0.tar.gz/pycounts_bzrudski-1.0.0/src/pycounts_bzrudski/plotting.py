import matplotlib.container
import matplotlib.pyplot as plt

from collections import Counter

def plot_words(word_counts: Counter, n: int = 10) -> matplotlib.container.BarContainer:
    """Plot a bar chart of word counts.

    Parameters
    ----------
    word_counts : collections.Counter
        Counter object of word counts.
    n : int, optional
        Plot the top n words. By default, 10.

    Returns
    -------
    matplotlib.container.BarContainer
        Bar chart of word counts.

    Examples
    --------
    >>> from pycounts_bzrudski.pycounts_bzrudski import count_words
    >>> from pycounts_bzrudski.plotting import plot_words
    >>> counts = count_words("text.txt")
    >>> plot_words(counts)
    """
    if not isinstance(word_counts, Counter):
        raise TypeError("'word_counts' should be of type 'Counter'.")
    top_n_words = word_counts.most_common(n)
    word, count = zip(*top_n_words)
    fig = plt.bar(range(n), count)
    plt.xticks(range(n), labels=word, rotation=45)
    plt.xlabel("Word")
    plt.ylabel("Count")
    return fig
