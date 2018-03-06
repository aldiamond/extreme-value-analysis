# Copyright (c) 2017 Arup Pty. Ltd.
# Distributed under the terms of the MIT License.

"""Annual Maxima Analysis
"""

import numpy as np


def gumbel(max_annual_gusts, gust_threshold=0):
    """Build a function that estimates the gust wind speed given
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
    """
    ln = np.log

    max_annual_gusts = max_annual_gusts**2
    
    # rank maximum annual gusts
    no_years = max_annual_gusts.size
    rank = np.array(range(1,no_years+1))
    V = np.sort(max_annual_gusts)

    # ignore smaller velocities
    rank = rank[V > gust_threshold]
    V = V[V > gust_threshold]

    # probability_ordinate
    Pm = rank/(no_years+1)

    # reduced variate
    y = -ln(-ln(Pm))

    # least squares straight line fit to estimate Type 1 parameters
    _A = np.vstack([y, np.ones(y.size)]).T
    _y = np.array(V).T
    a, u = np.linalg.lstsq(_A, _y)[0]

    # build function that returns wind speed given a return period
    design_windspeed_fn = lambda R: np.sqrt(u+a*(-ln(-ln(1-1/R))))
    measured_data = [(1/(1-pm), np.sqrt(v)) for pm, v in zip(Pm, V)]
    
    return design_windspeed_fn, measured_data

def gringorten(max_annual_gusts, gust_threshold=0):
    """Build a function that estimates the gust wind speed given
    the return period in yeats.
    
    Parameters:
    -----------
    max_annual_gusts :: np.array

    Returns:
    -----------
    callable
        function that calculates wind speed given return preiod in
        years
    list
        list of tuples of measured data - (return period, gust speed)
    
    Other Parameters:
    -----------------
    gust_threshold :: float
        Anything below this value will not be used to when curve
        fitting, but will be used for calculating probabilities.
    """
    ln = np.log
    max_annual_gusts = max_annual_gusts**2
    
    # rank maximum annual gusts
    no_years = max_annual_gusts.size
    rank = np.array(range(1,no_years+1))
    V = np.sort(max_annual_gusts)

    # ignore smaller velocities
    rank = rank[V > gust_threshold]
    V = V[V > gust_threshold]

    # probability_ordinate
    Pm = (rank-0.44)/(no_years+0.12)

    # reduced variate
    y = -ln(-ln(Pm))

    # least squares straight line fit to estimate Type 1 parameters
    _A = np.vstack([y, np.ones(y.size)]).T
    _y = np.array(V).T
    a, u = np.linalg.lstsq(_A, _y)[0]

    # build function that returns wind speed given a return period
    design_windspeed_fn = lambda R: np.sqrt(u+a*(-ln(-ln(1-1/R))))
    measured_data = [(1/(1-pm), np.sqrt(v)) for pm, v in zip(Pm, V)]
    
    return design_windspeed_fn, measured_data

def method_of_means(max_annual_gusts, gust_threshold=0):
    """Build a function that estimates the gust wind speed given
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
        fitting, but will be used for calculating probabilities.
    """
    ln = np.log
    EulerConstant = -0.5772215665

    max_annual_gusts = max_annual_gusts**2

    # ignore smaller velocities
    max_annual_gusts = max_annual_gusts[max_annual_gusts > gust_threshold]
    
    mean = max_annual_gusts.mean()
    stddev = max_annual_gusts.std()

    a = stddev * np.sqrt(6)/np.pi
    u = mean + EulerConstant*a
    
    # build function that returns wind speed given a return period
    design_windspeed_fn = lambda R: np.sqrt(max(u+a*(-ln(-ln(1-1/R))), 0))
    
    return design_windspeed_fn