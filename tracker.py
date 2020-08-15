import config
import numpy as np
from estimator import Estimator
from models import Vehicle
import matplotlib.pyplot as plt


def plot_dynamic_estimate(y_data):
    n_states = y_data.shape[0]
    n_measurements = y_data.shape[1]

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


def estimate_trajectory_1():
    """test estimator on trajectory data"""
    # generate data
    v = Vehicle()
    x_true = v.generate_trajectory_1()
    y_w = v.generate_measurements()
    #print(y_w.shape)
    # edit v measurements
    #y_w[1, :] = np.ones((1, y_w.shape[1]))*999
    # estimations
    x_est = np.zeros((y_w.shape))

    est = Estimator()
    #initial prediction
    est.predict_next_state()
    est.covariance_extrapolation()
    for i in range(y_w.shape[1]):
        #measure
        est.make_measurement(y_w[:, i])
        #update
        est.update_kalman_gain()
        x_hat = np.reshape(est.estimate_current_state(), (y_w.shape[0]))
        x_est[:, i] = x_hat
        est.update_estimate_uncertainty()
        #predict
        est.predict_next_state()
        est.covariance_extrapolation()

    v.plot_trajectory_1(x_est, x_true)


if __name__ == "__main__":
    estimate_trajectory_1()
