# Python translation of some of the functionalities in the famous `mgcv` R package

## Status

This package is currently under development.

## Goal

The ulterior goal would be to have a clone of mgcv in Python with little overhead.
At least for me, the currently available alternatives in Python are not sufficient.

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

