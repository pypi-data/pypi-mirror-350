# thinst: Thin data spatiotemporally

## Description
Thin datapoints spatiotemporally, spatially, or temporally.
<br>Spatiotemporal thinning will remove datapoints so that no two datapoints are within a given spatial threshold _and_ 
within a given temporal threshold of each other. Accordingly, two datapoints may overlap spatially, provided that they 
do not overlap temporally, and vice versa.
<br>Spatial thinning will remove datapoints so that no two datapoints are within a given spatial threshold of each 
other. 
<br>Temporal thinning will remove datapoints so that no two datapoints are within a given temporal threshold of each 
other. 

Thinning is set up to retain the maximum number of datapoints.

Thinning (whether it is spatiotemporal, spatial, or temporal) is conducted with the ```thinst``` function.

Simple plots of datapoints are also included within the ```plots``` module.

## Installation
```pip install thinst```

## Example usage
An exemplar illustrating how to use ```thinst``` is available on GitHub at: 
https://github.com/JSBigelow/thinst/blob/main/exemplar.ipynb

## License
MIT
