# Comparative Judgement

A package for comparative judgement (CJ).


Installation
------------

Dependencies


comparative-judgement requires:

- Python (>= |PythonMinVersion|)
- NumPy (>= |NumPyMinVersion|)
- SciPy (>= |SciPyMinVersion|)
- Ray


User installation


If you already have a working installation of NumPy and SciPy,
the easiest way to install comparative_judgement is using ``pip``::

```bash
    pip install comparative-judgement
```
```conda
    conda install -c conda-forge comparative-judgement
```


## Bayesian CJ
Importing the BCJ model and initiating a instance of the model with 4 samples:

```python
from cj.models import BayesianCJ

BCJ = BayesianCJ(4)
```

Creating the data:

```python
import numpy as np

data = np.asarray([
    [0, 1, 0],
    [0, 1, 0],
    [0, 3, 0],
    [1, 0, 1],
    [1, 0, 1],
    [1, 0, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [1, 2, 1],
    [2, 1, 2],
    [2, 1, 2],
    [2, 1, 2],
    [2, 3, 2],
    [3, 0, 3],
    [3, 0, 3],
    [3, 0, 3],
    [3, 0, 3],
    [3, 2, 3],
    [3, 2, 3],
    [3, 2, 3],
])
```

running the model:

```python
BCJ.run(data)
```

Finding the $\mathbb{E}[\mathbf{r}]$
```python
BCJ.Er_scores
>>> [3.046875, 2.09765625, 3.05859375, 1.796875]
```

Finding the BCJ rank:
```python
BCJ.rank
>>> array([3, 1, 0, 2])
```

<!-- ## Multi-Criterion Bayesian CJ
 -->


## Multi-Criteria BCJ

Importing the BCJ model and initiating a instance of the model with 4 samples:

```python
from cj.models import MBayesianCJ

criteria_weights = [0.2, 0.2, 0.6]

MBCJ = MBayesianCJ(3, criteria_weights)
```

```python
data = [
    #A, B,C1, 2, 3  
    [0, 1, 1, 1, 1],
    [1, 2, 1, 1, 1],
    [0, 2, 0, 0, 2]
]
```


running the model:

```python
MBCJ.run(data)
```

Finding the overall MBCJ rank:
```python
MBCJ.combined_rank
>>> array([1, 2, 0])
```

Finding the individual criteria BCJ ranks:
```python
MBCJ.lo_rank_scores
>>> {0: [np.float64(2.0), np.float64(1.5), np.float64(2.5)],
     1: [np.float64(2.0), np.float64(1.5), np.float64(2.5)],
     2: [np.float64(2.5), np.float64(1.5), np.float64(2.0)]}
```



## Traditional BTM CJ
Importing the BTM Model a instance of the model with 4 samples:

```python
from cj.models import BTMCJ

BTM = BTMCJ(4)
```

running the model:
```python
BTM.run(data)
```

Finding the optimised p scores:
```python
BTM.optimal_params
>>> array([-0.44654627,  0.04240265, -0.41580243,  0.81994508])
```

find BTM rank:
```python
BTM.rank
>>> array([3, 1, 2, 0])
```

---

# Pair Selection Methods

## Entropy

```python
from cj.pair_selector import EntropyPairSelector
```

```python
entropy_pairs = EntropyPairSelector(5)
```

```python
scores = [55, 65, 72, 45, 80]
standard_dev = 5
entropy_pairs.run_entropy_pairs_simulation(scores, standard_dev)
```

```python
entropy_pairs.results
>>> [[1, 4, 4],
 [1, 3, 1],
 [2, 3, 2],
 [1, 2, 2],
 [0, 2, 2],
 [0, 4, 4],
 [0, 1, 1],
 [3, 4, 4],
 [0, 3, 0],
 [2, 4, 4],
 [1, 2, 2],
 [2, 3, 2],
 [1, 4, 4],
 [3, 4, 4],
 [2, 4, 4],
 [0, 4, 4],
 [0, 2, 2],
 [0, 1, 1],
 [0, 3, 0],
 [1, 3, 1],
 [1, 4, 4],
 [0, 1, 1],
 [0, 4, 4],
 [3, 4, 4],
 [2, 3, 2],
...
 [2, 4, 4],
 [0, 1, 1],
 [0, 4, 4],
 [2, 3, 2],
 [1, 2, 2]]
```

---

Citing this Library:

```bib
@misc{comparative_judgement,
    author = {Andy Gray},
    title = {Comparative Judgement},
    year = {2024},
    publisher = {Python Package Index (PyPI)},
    howpublished = {\url{https://pypi.org/project/comparative-judgement/}}
}

```
