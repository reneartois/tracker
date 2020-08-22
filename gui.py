import tkinter as tk
import numpy as np
from kalman import KalmanFilter

class Gui:

    def __init__(self, master):
        # settings
        self.Show_True_Values = True
        self.Show_Measured_Values = True
        self.Show_Est_Values = True
        self.sigma = 30
        self.mu = 0
        self.canvas_oval_delta = 3
        stored_values = 40

        # frames
        canvas_frame = tk.Frame(master)

        #layout all main containers
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)


        # canvas
        canvas_width = 1000
        canvas_height =500
        self.canvas_bg_color = "black"
        self.canvas_true_val_color = "red"
        self.canvas_measurement_color = "blue"
        self.canvas_estimate_color = "green"
        self.w = tk.Canvas(master,
               width= canvas_width,
               height= canvas_height,
               bg= self.canvas_bg_color)
        self.w.grid(row = 0, columnspan=6, sticky= "NESW", padx=5, pady = 5)
        self.w.bind("<B1-Motion>", self.update_canvas)  #drag
        self.w.bind("<Button-1>", self.update_canvas)   #click

        # values
        self.true_val_idx = np.ones((2, stored_values))*-1
        self.meas_val_idx = np.ones((2, stored_values))*-1
        self.est_val_idx = np.ones((2, stored_values))*-1

        # kalman filter
        # only position measurement
        X0 = [int(canvas_width/2), 0, int(canvas_height/2), 0]
        self.kf = KalmanFilter(X0)

        # labels
        l1 = tk.Label(master, text = f"\tRed: true\t\tBlue: measured\t\tGreen: estimated")
        l1.grid(row = 1, columnspan=1, sticky = "EW")
        #l2 = tk.Label(master, text = "")
        #l2.grid(row = 3, sticky = "EW")#

        l2 = tk.Label(master, text= f"\tTrue\tMeas\tEst")
        l2.grid(row = 4, columnspan=1,sticky = "W")#

        self.lx_var = tk.StringVar()
        self.update_labels(self.lx_var, "X")
        l_X = tk.Label(master, textvariable= self.lx_var)
        l_X.grid(row = 5, columnspan=1,sticky = "W")#

        self.lvx_var = tk.StringVar()
        self.update_labels(self.lvx_var, "vX")
        l_X = tk.Label(master, textvariable= self.lvx_var)
        l_X.grid(row = 6, columnspan=1,sticky = "W")#

        self.ly_var = tk.StringVar()
        self.update_labels(self.ly_var, "Y")
        l_Y = tk.Label(master, textvariable= self.ly_var)
        l_Y.grid(row = 7, columnspan=1,sticky = "W")

        self.lvy_var = tk.StringVar()
        self.update_labels(self.lvy_var, "vY")
        l_X = tk.Label(master, textvariable= self.lvy_var)
        l_X.grid(row = 8, sticky = "W")#

        fff = tk.Label(master, text= "pffffffffffff")
        fff.grid(row = 8, column=1, sticky = "W")#

        #e1 = tk.Entry(master)
        #e1.grid(row = 5, column = 0, sticky = "W", pady = 2)

    def update_labels(self, lab, s1, s2="", s3="", s4=""):
        s = f"{s1}\t{s2}\t{s3}\t{s4}"
        lab.set(str(s))


    def update_canvas(self, event):
        # true values
        x_true = (event.x)
        y_true = (event.y)

        # add noise
        [x_meas, y_meas] = self.generate_measurements(X= [x_true, y_true])
        # measure
        self.kf.make_measurement(np.array([x_meas, 0, y_meas, 0]).T)
        #self.kf.make_measurement(np.array([x_meas, y_meas, 0, 0]).T)

        # update
        K = np.array(self.kf.update_kalman_gain()).T
        [x_est, vx_est, y_est, vy_est] = np.array(self.kf.estimate_current_state()).T
        #[x_est, y_est, _, _] = np.array(self.kf.estimate_current_state()).T
        P = self.kf.update_estimate_uncertainty()

        #predict
        [x_pred, _, y_pred, _] = np.array(self.kf.predict_next_state()).T
        self.kf.covariance_extrapolation()

        #to int, FIX
        x_est = np.int(np.asscalar(np.round(x_est)))
        y_est = np.int(np.asscalar(np.round(y_est)))
        vx_est = np.int(np.asscalar(np.round(vx_est)))
        vy_est = np.int(np.asscalar(np.round(vy_est)))
        x_meas = np.int(np.asscalar(np.round(x_meas)))
        y_meas = np.int(np.asscalar(np.round(y_meas)))
        #print(x_true, y_true)
        #print(x_est, y_est)
        #print("")
        # edit canvas
        d = self.canvas_oval_delta
        if self.Show_True_Values:
            self.true_val_idx = self.remove_points(x_true, y_true, self.true_val_idx, "cross")
            self.draw_cross(x_true, y_true, self.canvas_true_val_color)
        if self.Show_Est_Values:
            self.est_val_idx = self.remove_points(x_est, y_est, self.est_val_idx, "oval")
            self.w.create_oval(x_est-d, y_est-d, x_est+self.canvas_oval_delta, y_est+self.canvas_oval_delta, fill= self.canvas_estimate_color )
        if self.Show_Measured_Values:
            self.meas_val_idx = self.remove_points(x_meas, y_meas, self.meas_val_idx, "oval")
            self.w.create_oval(x_meas-d, y_meas-d, x_meas+self.canvas_oval_delta, y_meas+self.canvas_oval_delta, fill= self.canvas_measurement_color )

        self.update_labels(self.lx_var , "X", str(x_true), str(x_meas), str(x_est))
        self.update_labels(self.lvx_var , "vX", "", "", str(vx_est))
        self.update_labels(self.ly_var , "Y", str(y_true), str(y_meas), str(y_est))
        self.update_labels(self.lvy_var , "vY", "", "", str(vy_est))


    def draw_cross(self, x, y, color):
        x1 = int((x - self.canvas_oval_delta/2))
        x2 = int((x + self.canvas_oval_delta/2))
        y1 = int((y - self.canvas_oval_delta/2))
        y2 = int((y + self.canvas_oval_delta/2))
        self.w.create_line(x1, y1, x2+1, y2+1, fill= color)
        self.w.create_line(x1, y2, x2+1, y1+1, fill= color)



    def remove_points(self, x, y, val, type):
        d = self.canvas_oval_delta
        [last_x, last_y] = val[:, -1]
        val[:, :] = np.roll(val, 1, axis= 1)
        val[:, 0] = [x, y]
        if last_x > -1:
            if type == "cross":
                self.draw_cross(last_x, last_y, self.canvas_bg_color)
            else:
                self.w.create_oval(last_x-d, last_y-d, last_x+self.canvas_oval_delta, last_y+self.canvas_oval_delta, fill= self.canvas_bg_color)
        return val


    def generate_measurements(self, X):
        """ Add random noise"""
        r =X + np.random.randn(1, len(X)) * self.sigma + self.mu
        return np.reshape(r, (len(X)))
