import config
import numpy as np
from estimator import Estimator
from cannon import Cannon
import matplotlib.pyplot as plt


def plot_estimate(Y_DATA):
    n_measurements = Y_DATA.shape[1]
    n_states = Y_DATA.shape[0]
    x = np.linspace(1, n_measurements, n_measurements)
    y = np.transpose(Y_DATA)

    y_true = np.full((n_measurements, n_states), config.TRUE_VALUE)

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    l,  = plt.plot(x[0], y[0], "r-")
    l2, = plt.plot(x, y_true, "b-")

    for i in range(len(x)):
        l.set_data(x[:i], y[:i])
        #l2.set_data(x[:i], y_true[:i])
        ax.relim()
        ax.autoscale_view(True, True, True)
        plt.draw()
        plt.pause(1)
    input("Press Enter to exit...")

def test_tracking():
    """test estimator"""
    est = Estimator()
    #est.example_plot2()

    #initial prediction
    est.predict_next_state()
    est.covariance_extrapolation()
    for m in range(est.N_MEASUREMENTS):
        if est.print_values:
            print(est.i + 1)
        #measure
        est.make_measurement()
        #update
        est.update_kalman_gain()
        est.estimate_current_state()
        est.update_estimate_uncertainty()
        #predict
        est.predict_next_state()
        est.covariance_extrapolation()

        est.increment_iteration()
        if est.print_values:
            print("")

    X_EST = est.X_estimate_array
    return X_EST


if __name__ == "__main__":
    #X_EST = test_tracking()
    #print(X_EST)
    #plot_estimate(X_EST)
    c = Cannon(80, 60)
    c.solve()
    c.solve_analytically()
    c.plot()
