# Copyright (c) 2017 Arup Pty. Ltd.
# Distributed under the terms of the MIT License.

"""Annual Maxima Analysis
"""

import numpy as np

from .utils import least_squares

EULERCONSTANT = -0.5772215665
PI = np.pi

ln = np.log

def gumbel(max_annual_gusts):
    """Build a function that estimates the gust wind speed given the return period in years.

    Uses Gumbel method as described in J.D. Holmes, Wind Loading of Structures, CFC Press, 2007.
    
    Parameters:
    -----------
    max_annual_gusts :: np.ndarray
        Array of maximum annual gust wind speeds

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in years
    list
        list of tuples of measured data - [(return period, gust speed), ... ]
    """
    assert isinstance(max_annual_gusts, np.ndarray), "Function argument must be a numpy array."
    
    # rank maximum annual gusts
    no_years = max_annual_gusts.size
    rank = np.array(range(1,no_years+1))
    sorted_max_annual_gusts = np.sort(max_annual_gusts)

    probability_ordinate = rank/(no_years+1)
    reduced_variate = -ln(-ln(probability_ordinate))

    # least squares straight line fit y = mx + b
    slope, intercept = least_squares(reduced_variate, sorted_max_annual_gusts)

    # build function that returns wind speed given a return period
    design_windspeed_fn = lambda x: intercept+slope*(-ln(-ln(1-1/x)))
    # list of tuples of calculated return period and gust speed for each annual gust
    measured_data = [(1/(1-pm), v) for pm, v in zip(probability_ordinate, sorted_max_annual_gusts)]
    
    return design_windspeed_fn, measured_data

def gringorten(max_annual_gusts):
    """Build a function that estimates the gust wind speed given the return period in years.

    Uses Gringorten method as described in J.D. Holmes, Wind Loading of Structures, CFC Press, 2007.
    
    Parameters:
    -----------
    max_annual_gusts :: np.ndarray
        Array of maximum annual gust wind speeds

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in years
    list
        list of tuples of measured data - [(return period, gust speed), ... ]
    """
    assert isinstance(max_annual_gusts, np.ndarray), "Function argument must be a numpy array."
    
    # rank maximum annual gusts
    no_years = max_annual_gusts.size
    rank = np.array(range(1,no_years+1))
    sorted_max_annual_gusts = np.sort(max_annual_gusts)

    probability_ordinate = (rank-0.44)/(no_years+0.12)
    reduced_variate = -ln(-ln(probability_ordinate))

    # least squares straight line fit y = mx + b
    slope, intercept = least_squares(reduced_variate, sorted_max_annual_gusts)

    # build function that returns wind speed given a return period
    design_windspeed_fn = lambda x: intercept+slope*(-ln(-ln(1-1/x)))
    # list of tuples of calculated return period and gust speed for each annual gust
    measured_data = [(1/(1-pm), v) for pm, v in zip(probability_ordinate, sorted_max_annual_gusts)]
    
    return design_windspeed_fn, measured_data

def method_of_moments(max_annual_gusts):
    """Build a function that estimates the gust wind speed given the return period in years.

    Uses Method of Moments as described in J.D. Holmes, Wind Loading of Structures, CFC Press, 2007.
    
    Parameters:
    -----------
    max_annual_gusts :: np.ndarray
        Array of maximum annual gust wind speeds

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in years
    """
    assert isinstance(max_annual_gusts, np.ndarray), "Function argument must be a numpy array."

    slope = max_annual_gusts.std() * np.sqrt(6)/PI
    intercept = max_annual_gusts.mean() + EULERCONSTANT*slope
    
    # build function that returns wind speed given a return period
    return lambda R: intercept+slope*(-ln(-ln(1-1/R)))