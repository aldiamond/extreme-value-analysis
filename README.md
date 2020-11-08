# Extreme Value Method

Used to predict the gust wind speeds for large return periods. There are two families of methods contains in this package; annual maxima and independent storms.

Annual maxima:
- Gumbel
- Gringorten
- Method of Moments

Independent Storms:
- Peaks-Over-Threshold
- Improved Method of Independent Storms (IMIS) (still a work in progress)

All methods take an array of gust winds speeds and returns a function. This function takes the return period in years and returns the gust wind speed for that return period.

## Installing the library

This library has been written using Python 3.6 but should work for Python 3.2 onwards.

This python package has been written to work with python's built in installer: `pip install`. To add this library to your installation it is as simple as:

```
> pip install git+https://github.com/aldiamond/extreme-value-analysis.git
```

## Using the library

```py
import numpy as np

from extremevaluemethod.annualmaxima import gumbel, gringorten, method_of_moments
from extremevaluemethod.independentstorms import peaks_over_threshold

# example annual maximum gusts array
gusts = np.array([25.0, 27.0, 31.3, 30.5, 30.1, 29.4, 34.8, 24.3])

fn, measured_data = gumbel(gusts)

return_period = 1000 # years

gust_wind_speed = fn(1000) # gust wind speed for 1000 year event

# example independent storm maximum gusts array
gusts = np.array([23.0, 21.0, 31.3, 30.5, 30.1, 29.4, 34.8, 24.3])
no_years = 3

fn = peaks_over_threshold(gusts, no_years)

return_period = 1000 # years

gust_wind_speed = fn(1000) # gust wind speed for 1000 year event
```

To get help on how to use a function, use python in interative mode and enter `help(gumbel)`.

## Contributing

We welcome any contributions! Either raise an issue on gitlab and we will attempt to update the library or make the changes yourself and submit a pull request.

## Contact us

Contact details can be found on the AUTHORS page.
