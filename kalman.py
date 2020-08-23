import config
import numpy as np
import sys

class KalmanFilter:
    """
    Kalman filter
    """
    def __init__(self, X0= None, nz=None):
        """
        KF
        ---
        Attributes:
        Initialized using config.py (and X0, nz)
        """
        # state vector
        if X0 is None:
            X0 = config.X0
        self.X_hat = np.transpose(np.matrix(X0))
        self.N_STATES = self.X_hat.shape[0]
        if nz is None:
            nz = config.nz
        self.N_MEAS = nz

        # state transition matrix
        self.F = np.matrix(config.F)[: self.N_STATES, : self.N_STATES]
        # control input transaction matrix
        self.B = None
        # control matrix
        self.u = None
        if config.B is not None and config.u is not None:
            self.B = np.matrix(config.B)
            self.u = np.matrix(config.u)
        # observation matrix
        self.H = np.matrix(config.H)[: self.N_MEAS, : self.N_STATES]
        # kalman gain
        self.K = np.matrix(config.K0)[: self.N_STATES, : self.N_MEAS]
        # measurement uncertainty, covariance matrix
        self.R = np.matrix(config.R)[: self.N_MEAS, : self.N_MEAS]
        # process noise uncertainty, cov matrix
        #self.Q = np.matrix(config.Q)[: self.N_STATES, : self.N_STATES]
        #Qv = self.F.dot(np.matrix(Qv)).dot(self.F.T)
        #print(Qv)
        self.Q = self.F.dot(np.matrix(config.Qv)).dot(self.F.T)
        print(self.Q)
        # state estimation uncertainty cov matrix
        self.P = np.matrix(config.P0)[: self.N_STATES, : self.N_STATES]

        self.last_measurement = self.X_hat
        self.I = np.eye(self.K.shape[0])
        self.print_values = config.PRINT_VALUES


    # PREDICTION EQUATIONS --------------------------------------------
    def predict_next_state(self):
        """state extrapolation"""
        x_hat = self.F.dot(self.X_hat)
        if self.B is not None and self.u is not None:
            x_hat += self.B.dot(self.u)
        self.X_hat = x_hat
        self.print("predicted next: ", self.X_hat)
        return np.reshape(self.X_hat, (self.X_hat.shape[0]))


    def covariance_extrapolation(self):
        """Process noise covariance extrapolation"""
        self.P = self.F.dot(self.P).dot(np.transpose(self.F)) + self.Q
        self.print("cov P prediction: ", self.P)
        return np.reshape(self.P, (self.P.shape[0]*self.P.shape[1]))


    # ESTIMATION EQUATIONS -------------------------------------------
    def estimate_current_state(self):
        """State update"""
        x = self.X_hat
        z = self.last_measurement
        e = z - self.H.dot(x)
        self.print("error: ", e)
        self.X_hat = self.X_hat + self.K.dot(e)
        self.print("current estimate: ", self.X_hat)
        return np.reshape(self.X_hat, (self.X_hat.shape[0]))


    def update_estimate_uncertainty(self):
        """Covariance update"""
        i_minus_kh = self.I - self.K.dot(self.H)
        i_minus_kh_t = np.transpose(i_minus_kh)
        krk = self.K.dot(self.R).dot(np.transpose(self.K))
        self.P = i_minus_kh.dot(self.P).dot(i_minus_kh_t) + krk
        self.print("cov P update: ", self.P)
        return np.reshape(self.P, (self.P.shape[0]*self.P.shape[1]))


    def update_kalman_gain(self):
        """Kalman Gain update"""
        print(self.R)
        print(self.P)
        print(self.H)
        hph_r = self.H.dot(self.P).dot(np.transpose(self.H)) + self.R
        hph_r = np.linalg.inv(hph_r)
        self.K = self.P.dot(np.transpose(self.H)).dot(hph_r)
        self.print("kalman gain: ", self.K)
        return np.reshape(self.K, (self.K.shape[0]*self.K.shape[1]))

    # MISC ------------------------------------------------------------
    def test_estimator():
        """ test KF"""
        # FIX
        pass


    def make_measurement(self, y):
        """ measurement equation """
        n_max = max(y.shape)
        y = np.reshape(y, (n_max, 1))
        self.last_measurement = self.H.dot(y)
        self.print("measurement: ", self.last_measurement)


    def print(self, str, val):
        if self.print_values:
            print(str)
            print(val)


    def estimate_all_values(self, y_w):
        """
        Kalman filter run on measured data
        """
        # save results
        x_pred = np.zeros((self.N_STATES, y_w.shape[1]))
        x_est = np.zeros((self.N_STATES, y_w.shape[1]))
        p_val = np.zeros((self.P.shape[0]*self.P.shape[1], y_w.shape[1]))
        k_val = np.zeros((self.K.shape[0]*self.K.shape[1], y_w.shape[1]))

        #initial prediction
        self.print("# initial prediction")
        self.predict_next_state()
        self.covariance_extrapolation()
        self.print("")
        for i in range(y_w.shape[1]):
            self.print(i+1)
            #measure
            self.print("# measure")
            if not np.isnan(y_w[:, i]).any():
                self.make_measurement(y_w[:, i])

            #update
            self.print("# update")
            k_val[:, i] = self.update_kalman_gain()
            x_est[:, i] = self.estimate_current_state()
            p_val[:, i] = self.update_estimate_uncertainty()

            #predict
            self.print("# predict")
            x_pred[:, i] = self.predict_next_state()
            self.covariance_extrapolation()
            self.print("")
        return x_est, x_pred, p_val, k_val


    def test_kf():
        m = [49.979, 50.025, 50, 50.003, 49.994, 50.002, 49.999, 50.006, 49.998, 49.991]
        y_w = [49.95, 49.967, 50.01, 50.106, 49.992, 49.819, 49.933, 50.007, 50.023, 49.99]
        y_w = np.matrix(y_w)
        kf = KalmanFilter_Custom()
        x_est, x_pred = kf.estimate_all_values(y_w)
        #FIX


if __name__ == "__main__":
    kf = KalmanFilter()
    kf.test_kf()
