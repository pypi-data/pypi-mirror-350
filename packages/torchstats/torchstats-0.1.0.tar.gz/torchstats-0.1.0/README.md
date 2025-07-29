# torchstats
This package implements various probability distributions in PyTorch, 
among those univariate distributions from scipy, categorical distributions, mixture models, and Bayesian networks.
It implements computing probabilities and densities, and rudimentary functionality for fitting distributions to data.

## Examples
Categorical distributions in a [one-hot](https://en.wikipedia.org/wiki/One-hot) event space.
```python
import torch
from torchstats import CategoricalOneHot

d = CategoricalOneHot([0.1, 0.5, 0.2, 0.2])
events = d.sample(5)
# tensor([[0., 1., 0., 0.],
#         [0., 0., 0., 1.],
#         [0., 1., 0., 0.],
#         [0., 0., 0., 1.],
#         [0., 1., 0., 0.]], dtype=torch.float64)
d.probability((events, events))
# tensor([0.5000, 0.2000, 0.5000, 0.2000, 0.5000], dtype=torch.float64)

# Probabilities and densities are always computed for hyperrectangles in event space.
# These hyperrectangles are represented as tuples of lower bound and upper bounds.
# This allows us to compute, for example, the probability of all categories except the first.
d.probability((torch.tensor([0.0, 0.0, 0.0, 0.0]), torch.tensor([0.0, 1.0, 1.0, 1.0])))
# tensor([0.9000], dtype=torch.float64
```

A mixture model of truncated Gaussian distributions.
```python
import torch
from torchstats import MixtureModel

data = torch.rand(100)
d = MixtureModel.fit_truncnorm_mixture(data, bounds=(0.0, 1.0), n_components=3, n_init=3)
d.weights
# tensor([0.4785, 0.1701, 0.3514], dtype=torch.float64)
d.density(data)
# ...
```

A Bayesian network
```python
import torch
from torchstats import BayesianNetwork, Categorical

factory = BayesianNetwork.Factory()
n1 = factory.new_node("var1")
n1.discrete_event_space(0, 1, 2)
n1.set_conditional_probability({}, Categorical([0.1, 0.2, 0.7]))

n2 = factory.new_node("var2")
n2.discrete_event_space(0, 1, 2)
n2.set_conditional_probability({}, Categorical([0.8, 0.1, 0.1]))

n3 = factory.new_node("var3")
n3.set_parents(n1, n2)
n3.discrete_event_space(0, 1)
n3.set_conditional_probability({n1: 0, n2: 0}, Categorical([1.0, 0.0])) 
n3.set_conditional_probability({n1: 0, n2: (1, 2)}, Categorical([0.1, 0.9]))
n3.set_conditional_probability({n1: (1, 2), n2: (0, 2)}, Categorical([0.0, 1.0]))

n1.hidden = n2.hidden = True  # make n1 and n2 hidden/latent variables

d = factory.create()
type(d)
# <class 'torchstats.bayesian_network.BayesianNetwork'>
d.output_space.input_shape
# torch.Size([1])
d.probability((torch.tensor(0), torch.tensor(0)))
# tensor([0.0820], dtype=torch.float64)
d.probability((torch.tensor(1), torch.tensor(1)))
# tensor([0.0820], dtype=torch.float64)
d.probability((torch.tensor(1), torch.tensor(1)))
# tensor([0.9180], dtype=torch.float64)
```

## Installation
Install `torchstats` from PyPI using
```bash
pip install torchstats
```

To extend `torchstats`, clone this repository and run
```bash
pip install -e .[all]
```
to install development and testing dependencies.
To run the tests, run either `pytest` or `nox`.
