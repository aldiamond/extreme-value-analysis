# Copyright (c) 2017 Arup Pty. Ltd.
# Distributed under the terms of the MIT License.

"""Annual Maxima Analysis
"""

import numpy as np

from utils import least_squares

EULERCONSTANT = -0.5772215665
PI = np.pi

ln = np.log
sqrt = np.sqrt

def gumbel(max_annual_gusts):
    """Build a function that estimates the gust wind speed given
    the return period in yeats.
    
    Parameters:
    -----------
    max_annual_gusts :: np.ndarray
        Array of maximum annual gust wind speeds

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in
        years
    list
        list of tuples of measured data - [(return period, gust speed), ... ]
    """
    assert isinstance(max_annual_gusts, np.ndarray), "Function argument must be a numpy array."

    max_annual_pressures = max_annual_gusts**2
    
    # rank maximum annual gusts
    no_years = max_annual_pressures.size
    rank = np.array(range(1,no_years+1))
    sorted_max_annual_pressures = np.sort(max_annual_pressures)

    probability_ordinate = rank/(no_years+1)

    reduced_variate = -ln(-ln(probability_ordinate))

    # least squares straight line fit y = mx + b
    slope, intercept = least_squares(reduced_variate, sorted_max_annual_pressures)

    # build function that returns wind speed given a return period
    design_windspeed_fn = lambda x: sqrt(intercept+slope*(-ln(-ln(1-1/x))))
    # list of tuples of calculated return period and gust speed for each annual gust
    measured_data = [(1/(1-pm), sqrt(p)) for pm, p in zip(probability_ordinate, sorted_max_annual_pressures)]
    
    return design_windspeed_fn, measured_data

def gringorten(max_annual_gusts):
    """Build a function that estimates the gust wind speed given
    the return period in yeats.
    
    Parameters:
    -----------
    max_annual_gusts :: np.ndarray
        Array of maximum annual gust wind speeds

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in
        years
    list
        list of tuples of measured data - [(return period, gust speed), ... ]
    """
    assert isinstance(max_annual_gusts, np.ndarray), "Function argument must be a numpy array."

    max_annual_pressures = max_annual_gusts**2
    
    # rank maximum annual gusts
    no_years = max_annual_pressures.size
    rank = np.array(range(1,no_years+1))
    sorted_max_annual_pressures = np.sort(max_annual_pressures)

    probability_ordinate = (rank-0.44)/(no_years+0.12)
    reduced_variate = -ln(-ln(probability_ordinate))

    # least squares straight line fit y = mx + b
    slope, intercept = least_squares(reduced_variate, sorted_max_annual_pressures)

    # build function that returns wind speed given a return period
    design_windspeed_fn = lambda x: sqrt(intercept+slope*(-ln(-ln(1-1/x))))
    # list of tuples of calculated return period and gust speed for each annual gust
    measured_data = [(1/(1-pm), sqrt(p)) for pm, p in zip(probability_ordinate, sorted_max_annual_pressures)]
    
    return design_windspeed_fn, measured_data

def method_of_means(max_annual_gusts):
    """Build a function that estimates the gust wind speed given
    the return period in yeats.
    
    Parameters:
    -----------
    max_annual_gusts :: np.ndarray
        Array of maximum annual gust wind speeds

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in
        years
    """
    assert isinstance(max_annual_gusts, np.ndarray), "Function argument must be a numpy array."

    max_annual_pressures = max_annual_gusts**2

    slope = max_annual_pressures.std() * sqrt(6)/PI
    intercept = max_annual_pressures.mean() + EULERCONSTANT*slope
    
    # build function that returns wind speed given a return period
    design_windspeed_fn = lambda R: sqrt(offest+slope*(-ln(-ln(1-1/R))))
    
    return design_windspeed_fn