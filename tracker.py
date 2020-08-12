import config
import numpy as np
from estimator import Estimator


def test_tracking():
    """test estimator"""
    est = Estimator()
    #est.example_plot2()

    #predict
    est.predict_next_state()
    est.covariance_extrapolation()
    for m in range(est.N_MEASUREMENTS):
        print(est.i + 1)
        #measure
        est.make_measurement()

        #update
        est.update_kalman_gain()
        est.estimate_current_state()
        est.update_estimate_uncertainty()

        est.predict_next_state()
        est.covariance_extrapolation()

        est.increment_iteration()
        print("")


if __name__ == "__main__":
    test_tracking()
