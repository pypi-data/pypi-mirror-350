# pycounts_bzrudski

Calculate word counts in a text file!

This repository is based on the tutorial presented in the [Py-Pkgs tutorial](https://py-pkgs.org/welcome). Due to slight differences in the versions of available packages, some of the code is a bit different.

## Installation

```bash
$ pip install pycounts_bzrudski
```

## Usage

`pycounts_bzrudski` can be used to count words in a text file and plot results
as follows:

```python
from pycounts_bzrudski.pycounts_bzrudski import count_words
from pycounts_bzrudski.plotting import plot_words
import matplotlib.pyplot as plt

file_path = "test.txt" # path to your file
counts = count_words(file_path)
fig = plot_words(counts, n=10)
plt.show()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pycounts_bzrudski` was created by bzrudski. It is licensed under the terms of the MIT license.

## Credits

`pycounts_bzrudski` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
