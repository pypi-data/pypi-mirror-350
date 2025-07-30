# GRIP
Implementation of GRIP & FLAMES algorithms, for Fast & Global Point Cloud rigid registration.

## Installation

```
pip install grip
```


## Basic Usage


- **Pairwise**:

```python
from grip import PairwiseGRIP, icp

estimator = PairwiseGRIP(icp)
T_s2m_hat = estimator(sources, models)
# or
registered_sources, registered_models = estimator.register(sources, models)
```


- **Generative multiview**:

```python
from grip import GenerativeMultiviewsGRIP, ChamferJRMPC

estimator = GenerativeMultiviewsGRIP(ChamferJRMPC())
estimator(views)
T_hat = estimator.T_hat
```