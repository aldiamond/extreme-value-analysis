# Copyright (c) 2017 Arup Pty. Ltd.
# Distributed under the terms of the MIT License.

"""Methods for Independent storms.
"""

import numpy as np

from utils import least_squares

def peaks_over_threshold(max_storm_gusts, no_years, min_threshold=None, max_threshold=None):
    """Build a function that estimates the gust speed given
    the return period in yeats.
    
    Parameters:
    -----------
    max_annual_gusts :: np.ndarray
    no_years :: int

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in
        years.
    
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

def method_independent_storms(stn_id, dataframe):
    """
    Harris's Improved Method of Independent Storms (IMIS).
    
    Parameters:
    -----------
    max_annual_gusts :: np.array

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in
        years list of tuples of measured data
    """
    
    raise NotImplementedError('This method is not yet implemented.')
    #TODO
