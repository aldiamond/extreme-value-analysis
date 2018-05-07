# Copyright (c) 2017 Arup Pty. Ltd.
# Distributed under the terms of the MIT License.

"""Methods for Independent storms.
"""
from math import factorial as fac

import numpy as np
from scipy.special import gamma, polygamma, digamma
from scipy.integrate import romberg

from .utils import least_squares
from .constants import EULERCONSTANT, PI, DENSITY

ln = np.log
reverse = np.flipud

def peaks_over_threshold(max_storm_gusts, no_years, min_threshold=None, max_threshold=None):
    """Build a function that estimates the gust speed given
    the return period in yeats.
    
    Parameters:
    -----------
    max_annual_gusts :: np.ndarray
    no_years :: int
    min_threshold :: float, optional
    max_threshold :: float, optional

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in years.
    
    Other Parameters:
    -----------------
    min_threshold :: int
        Use to overide the minimum threshold value. Otherwise minimum gust is used.
    max_threshold :: int
        Use to overide the maximum threshold value. Otherwise maximum gust is used.
    """
    assert isinstance(max_storm_gusts, np.ndarray), "Function argument must be a numpy array."

    storm_rate = max_storm_gusts.size/no_years # storms per year
    
    min_threshold = min_threshold if min_threshold else max_storm_gusts.min()
    max_threshold = max_threshold if max_threshold else max_storm_gusts.max()
    threshold_values = np.linspace(min_threshold, max_threshold, 8) # TODO: Investigate sensitivity to spacing
    
    def mean_excess(u):
        excesses = max_storm_gusts[max_storm_gusts>u]-u
        return excesses.mean()
    
    mean_excesses = [mean_excess(u) for u in threshold_values]

    slope, intercept = least_squares(threshold_values, mean_excesses)
    
    k = -slope/(slope+1)
    sigma = intercept*(slope+1)

    return lambda R: min_threshold+sigma*(1-(storm_rate*R)**(-k))/k


def method_independent_storms(gust_windspeeds, no_years):
    """
    Harris's Improved Method of Independent Storms (IMIS) from his 1999 paper "Improvements to the 'Method of Independent Storms'".
    
    Parameters:
    -----------
    gust_windspeeds :: np.ndarray
        Array of gust wind speeds
    no_years :: int
        Number of wind years
    
    Returns:
    -----------
    callable
        function that calculates wind speed given return period in years
    list
        list of tuples of measured data - [(plotting position, gust speed), ... ]
    """

    raise NotImplementedError('This method is not yet implemented.')

    assert isinstance(max_annual_gusts, np.ndarray), "gust windspeeds must be a numpy array."
    assert isinstance(no_years, int), "No of years argument must be a integer."

    pressures = 0.5*DENSITY*gust_windspeeds**2
    
    rank = np.array(range(1,len(pressures)+1))
    sorted_pressures = reverse(np.sort(pressures)) # sort highest to smallest

    def plotting_position(v, N):
        if v < 4:
            return EULERCONSTANT


def ximis(gust_windspeeds, no_years):
    """
    NOTE: This function has not been validated!

    Harris's Penultimate Improved Method of Independent Storms (XIMIS) from his 2009 paper "XIMIS, a penultimate extreme value method suitable for all types of wind climate".

    This method is valid when there are more than 50 storms per year. For this many storms the minimum usuable reduced variate is y=-0.7
    
    Parameters:
    -----------
    gust_windspeeds :: np.ndarray
        Array of gust wind speeds
    no_years :: int
        Number of wind years
    
    Returns:
    -----------
    callable
        function that calculates wind speed given reduced variate (plotting position)
    list
        list of tuples of measured data - [(plotting position, gust speed), ... ]
    """

    #TODO: Implement lower bounds on reduced variate (plotting position) based on storm rate (see paper)

    assert isinstance(max_annual_gusts, np.ndarray), "gust windspeeds must be a numpy array."
    assert isinstance(no_years, int), "No of years argument must be a integer."
    
    rank = np.array(range(1,len(gust_windspeeds)+1))
    sorted_gust_windspeeds = reverse(np.sort(gust_windspeeds)) # sort highest to smallest

    plotting_position = ln(no_years)-digamma(rank)

    # build function that returns wind speed given a reduced variate
    slope, intercept = least_squares(plotting_position, sorted_gust_windspeeds)
    design_windspeed_fn = lambda y: intercept+slope*y
    # list of tuples of calculated reduced variate and gust speed for each annual gust
    measured_data = [(y, v) for y, v in zip(plotting_position, sorted_gust_windspeeds)]
    
    return design_windspeed_fn, measured_data