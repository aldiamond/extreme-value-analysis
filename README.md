# Extreme Value Method

Used to predict the gust wind speeds for large return periods. There are two families of methods contains in this package; annual maxima and independent storms.

Annual maxima:
- Gumbel
- Gringorten
- Method of Moments

Independent Storms:
- Peaks-Over-Threshold
- Improved Method of Independent Storms (IMIS)

All methods take an array of gust winds speeds and returns a function. This function takes the return period in years and returns the gust wind speed for that return period.

## Installing the library

This library has been written using Python 3.6 but should work for Python 3.2 onwards.

Currently a work in progress. To get the latest development version:

```
> pip install git+https://github.com/AlexLSmith/extreme-value-analysis#egg=extremevaluemethod
```

It will one day be added to PYPI.

*Note: the library has one dependency, numpy. If you are new to python and are using the windows operating system, I suggest using an anaconda distribution of python.*

## Using the library

```py
from extremevaluemethod.annualmaxima import gumbel, gringorten, method_of_means
from extremevaluemethod.independentstorms import peaks_over_threshold

# example annual maximum gusts array
gusts = [25.0, 27.0, 31.3, 30.5, 30.1, 29.4, 34.8, 24.3]

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

To get help on how to use a function, use python in interative mode.

```
> python
Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from extremevaluemethod.annualmaxima import gumbel
>>> help(gumbel)

Build a function that estimates the gust wind speed given
the return period in yeats.

Parameters:
-----------
max_annual_gusts :: np.array

Returns:
-----------
callable
    function that calculates wind speed given return preiod in
    years.
list
    list of tuples of measured data - (return period, gust speed)

Other Parameters:
-----------------
gust_threshold :: float
    Anything below this value will not be used to when curve
    fitting, but will be used for calculating probabilities.
```

## Contributing

We welcome any contributions! Either raise an issue on github and we will attempt to update the library or make the changes yourself and submit a pull request.

## Contact us

Contact details can be found on the AUTHORS page.