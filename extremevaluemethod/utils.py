# Copyright (c) 2017 Arup Pty. Ltd.
# Distributed under the terms of the MIT License.

import numpy as np

def least_squares(x, y):
    """
    Least squares straight line fit:
        y = mx + b
    
    We rewrite the line equation as y = Ap,
    where A = [[x 1]] and p = [[m], [b]]

    Parameters:
    -----------
    y :: np.ndarray
    x :: np.ndarray
    """
    A = np.vstack([x, np.ones(x.size)]).T
    m, b = np.linalg.lstsq(A, y, rcond=None)[0]
    return m, b