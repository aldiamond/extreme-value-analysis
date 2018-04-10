# To run unittests
# python -m unittest -v tests\tests.py

import unittest
import numpy as np

from . import annualmaxima_testdata
from extremevaluemethod import annualmaxima

def get_annual_maxima_data():
    years, gusts = zip(*annualmaxima_testdata.measured_data)
    return np.array(gusts)

class TestAnnualMaxima(unittest.TestCase):

    def test_Gumbel(self):
        gusts = get_annual_maxima_data()
        fn, _ = annualmaxima.gumbel(gusts)
        expected_results = annualmaxima_testdata.correct_results_gumbel
        for i, (return_period, expected_gust_speed) in enumerate(expected_results):
            with self.subTest(i=i):
                self.assertAlmostEqual(fn(return_period), expected_gust_speed, places=1)
    
    def test_Gringorten(self):
        gusts = get_annual_maxima_data()
        fn, _ = annualmaxima.gringorten(gusts)
        expected_results = annualmaxima_testdata.correct_results_gringorten
        for i, (return_period, expected_gust_speed) in enumerate(expected_results):
            with self.subTest(i=i):
                self.assertAlmostEqual(fn(return_period), expected_gust_speed, places=1)

    def test_Method_of_moments(self):
        gusts = get_annual_maxima_data()
        fn = annualmaxima.method_of_moments(gusts)
        expected_results = annualmaxima_testdata.correct_results_method_of_moments
        for i, (return_period, expected_gust_speed) in enumerate(expected_results):
            with self.subTest(i=i):
                self.assertAlmostEqual(fn(return_period), expected_gust_speed, places=1)

if __name__ == '__main__':
    unittest.main()