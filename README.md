# Python translation of some of the functionalities in the famous `mgcv` R package

## Status

This package is currently under development.

## Goal

The ultimate goal is to create a clone of mgcv in Python with minimal overhead. 
At least for me, the currently available alternatives in Python are insufficient.

## Features

### Log

- April 21: Added smoothing constructor via `rpy2`

### New features

Feel free to make pull requests :)

## Reference

Consider citing one/multiple of the following papers as indicated in `citation("mgcv")`:

```
2011 for generalized additive model method; 2016 for beyond exponential family; 2004 for strictly additive
GCV based model method and basics of gamm; 2017 for overview; 2003 for thin plate regression splines.

  Wood, S.N. (2011) Fast stable restricted maximum likelihood and marginal likelihood estimation of
  semiparametric generalized linear models. Journal of the Royal Statistical Society (B) 73(1):3-36

  Wood S.N., N. Pya and B. Saefken (2016) Smoothing parameter and model selection for general smooth models
  (with discussion). Journal of the American Statistical Association 111:1548-1575.

  Wood, S.N. (2004) Stable and efficient multiple smoothing parameter estimation for generalized additive
  models. Journal of the American Statistical Association. 99:673-686.

  Wood, S.N. (2017) Generalized Additive Models: An Introduction with R (2nd edition). Chapman and
  Hall/CRC.

  Wood, S.N. (2003) Thin-plate regression splines. Journal of the Royal Statistical Society (B)
  65(1):95-114.
```

## Details: SmoothConTransformer

The `SmoothConTransformer` class interfaces with R's `mgcv` package via `rpy2` to utilize smoothing functions for statistical modeling in Python. 
It provides methods to fit models, transform data, and retrieve important objects like the design matrix and penalty matrices.

### Installation

To install this package, clone the repository and install it using `setup.py`:

```bash
git clone https://your-repository-url.git
cd your-repository-directory
pip install .
```

This will install the package along with its dependencies.

### Usage

Here's how to use the `SmoothConTransformer`:

#### Importing the Class

```python
from my_package_name import SmoothConTransformer
```

#### Initializing the Transformer

```python
transformer = SmoothConTransformer()
```

#### Fitting the Model

To fit the model, you need a formula and a dataset. Here is an example of fitting the transformer with a dataset of size 20:

```python
import pandas as pd

# Sample data
data = pd.DataFrame({
    'x': range(20),
    'y': [xi**2 for xi in range(20)]  # Quadratic relationship
})

# Fit the model using a thin plate regression spline
transformer.fit(obj="s(x)", data=data)
```

#### Transforming Data

After fitting, you can apply the transformation to new data:

```python
# New sample data
new_data = pd.DataFrame({
    'x': range(20, 40)
})

# Transform the data
transformed_data = transformer.transform(data=new_data)
print(transformed_data)
```

#### Retrieving the Design Matrix

Get the design matrix as a NumPy array:

```python
design_matrix = transformer.get_design()
print(design_matrix)
```

#### Retrieving the Penalty Matrices

Get the penalty matrices as a list of NumPy arrays:

```python
penalty_matrices = transformer.get_penalty()
for mat in penalty_matrices:
    print(mat)
```


