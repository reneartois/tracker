from matplotlib import pyplot as plt
import numpy as np

class Plots():
    def __init__(self):
        pass


    def plot_1D(self, X_est, X_true, y_w=None):
        plt.plot(X_true[0, :],"-", label= "true")
        plt.plot(X_est[0, :],"--", label= "estimate")
        if y_w is not None:
            plt.plot(y_w[0, :], "rx", label= "measurement")
        plt.legend(loc= "best")
        plt.show()


    def plot_1D_and_error(self, X_est, X_true, p_val, k_val, y_w=None):
        fig, ax = plt.subplots(2)
        ax[0].plot(X_true[0, :],"-", label= "true")
        ax[0].plot(X_est[0, :],"--", label= "estimate")
        if y_w is not None:
            ax[0].plot(y_w[0, :], "rx", label= "measurement")
        ax[0].legend(loc= "best")

        ax[1].plot(p_val[0, :], label= "P")
        ax[1].plot(k_val[0, :], label= "K")
        ax[1].legend(loc= "best")
        plt.show()


    def plot_live_estimate(y_data):
        """
        Plots "live" updates
        """
        # FIX
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
