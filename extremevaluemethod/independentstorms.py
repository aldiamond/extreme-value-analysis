# Copyright (c) 2017 Arup Pty. Ltd.
# Distributed under the terms of the MIT License.

"""Methods for Independent storms.
"""

import numpy as np

def peaks_over_threshold(max_storm_gusts, no_years, min_threshold=None, max_threshold=None):
    """Build a function that estimates the gust speed given
    the return period in yeats.
    
    Parameters:
    -----------
    max_annual_gusts :: np.array

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in
        years.
    
    Other Parameters:
    -----------------
    gust_threshold :: float
        Anything below this value will not be used to when curve
        fitting, but will be used for calculating probabilities
    """

    max_gust = max_storm_gusts.max()
    min_gust = max_storm_gusts.min()
    storm_rate = max_storm_gusts.size/no_years # storms per year
    
    min_threshold = min_threshold if min_threshold else int(min_gust)
    max_threshold = max_threshold if max_threshold else int(max_gust)
    threshold_values = range(min_threshold, max_threshold)
    min_threshold = min(threshold_values)
    
    def mean_excess(u):
        excesses = max_storm_gusts[max_storm_gusts>u]-u
        return excesses.mean()
    
    mean_excesses = [mean_excess(u) for u in threshold_values]
    
    A = np.vstack([threshold_values, np.ones(len(threshold_values))]).T
    y = np.array(mean_excesses).T
    slope, intercept = np.linalg.lstsq(A, y)[0]
    k = -slope/(slope+1)
    sigma = intercept*(slope+1)

    return lambda R: min_threshold+sigma*(1-(storm_rate*R)**(-k))/k

def method_independent_storms(stn_id, dataframe):
    """
    Harris's Improved Method of Independent Storms (IMIS).

    In:
        Pandas dataframe with the following column headings:
        - timestamp (datetime - used as index column)
        - peak gust
        - storm type
        - wind direction
        Sorted in chronological order.
    Out:
        Pandas dataframe with design windspeeds based on:
        - wind direction
        - storm type
        - return period
    
    Parameters:
    -----------
    max_annual_gusts :: np.array

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in
        years list of tuples of measured data
    
    Other Parameters:
    -----------------
     gust_threshold :: float
        Anything below this value will not be used to when curve
        fitting, but will be used for calculating probabilities
    """
    
    raise NotImplementedError('This method is not yet implemented.')
