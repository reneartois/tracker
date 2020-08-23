import tkinter as tk
import numpy as np
from kalman import KalmanFilter
import config

class Gui:

    def __init__(self, master):
        """
        Canvas frame for clicking to set true postion.
        Noise measurements are made from these points, and the kalman filter
        estimates the position based on measurements and the underlying model.
        These points are visualized on a canvas.
        ---
        Attributes:
        initalized with config.py
        """
        # settings
        master.title(config.master_title)
        master_width = config.master_width
        master_heigth = config.master_heigth
        master.geometry(f"{master_width}x{master_heigth}")
        self.Show_True_Values = config.show_true_values
        self.Show_Measured_Values = config.show_measured_values
        self.Show_Est_Values = config.show_est_values
        self.sigma = config.sigma
        self.mu = config.mu
        self.canvas_oval_delta = config.canvas_oval_delta
        stored_values = config.n_stored_values

        # frames
        canvas_width = config.canvas_width
        canvas_height = config.canvas_height
        main_frame_heigth = config.main_frame_heigth
        main_frame_width = config.main_frame_width
        canvas_frame = tk.Frame(master, height= canvas_height)
        main_frame = tk.Frame(master, width= canvas_width, height= main_frame_heigth)

        # layout
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # main frames
        canvas_frame.grid(row=0, column= 0,  sticky= "NESW", padx= 5, pady= 5)
        main_frame.grid(row=1, column= 0, sticky= "NESW", padx= 5, pady= 5)

        # canvas
        self.canvas_bg_color = config.canvas_bg_color
        self.canvas_true_val_color = config.canvas_true_val_color
        self.canvas_measurement_color = config.canvas_measurement_color
        self.canvas_estimate_color = config.canvas_estimate_color
        self.w = tk.Canvas(canvas_frame,
               bg= self.canvas_bg_color)
        self.w.pack(fill="both", expand=True)
        self.w.bind("<B1-Motion>", self.update_canvas)  #drag
        self.w.bind("<Button-1>", self.update_canvas)   #click

        # display frames
        padx = config.display_padx
        pady = config.display_pady
        display_frame = tk.Frame(main_frame, width=main_frame_width, height= main_frame_heigth, padx= padx, pady= pady)
        display_frame.grid(row=0, column=0, sticky= "NW")
        P_frame = tk.Frame(main_frame, width=main_frame_width, height= main_frame_heigth, padx= padx, pady= pady)
        P_frame.grid(row=0, column=1, sticky= "NW")
        K_frame = tk.Frame(main_frame, width=main_frame_width, height= main_frame_heigth, padx= padx, pady= pady)
        K_frame.grid(row=0, column=2, sticky= "NW")

        # display frame labels
        self.display_var = tk.StringVar()
        display_label = tk.Label(display_frame, textvariable= self.display_var)
        display_label.grid(row= 0, column= 0, sticky = "NW")

        self.P_var = tk.StringVar()
        display_label = tk.Label(P_frame, textvariable= self.P_var)
        display_label.grid(row=0, column= 0, sticky = "NW")

        self.K_var = tk.StringVar()
        display_label = tk.Label(K_frame, textvariable= self.K_var)
        display_label.grid(row=0, column= 0, sticky = "NW")

        # values
        self.true_val_idx = np.ones((2, stored_values))*-1
        self.meas_val_idx = np.ones((2, stored_values))*-1
        self.est_val_idx = np.ones((2, stored_values))*-1

        # kalman filter
        # only position measurement
        X0 = [int(canvas_width/2), 0, int(canvas_height/2), 0]
        self.kf = KalmanFilter(X0= X0, nz= 2)


    def update_matrix_label(self, lab, m, name):
        r,c = m.shape
        s = ""
        for i in range(r):
            for j in range(c):
                s += f"{m[i,j]:.2f}\t"
            s += f"\r"
        ss = name + f":\n" + s
        lab.set(ss)


    def update_display_labels(self, lab, x_true, y_true, x_meas, y_meas, x_est, y_est, vx_est, vy_est):
        header = f"\tTrue\tMeas\tEst\n"
        x = f"X:\t{x_true}\t{x_meas}\t{x_est}\n"
        y = f"Y:\t{y_true}\t{y_meas}\t{y_est}\n"
        vx = f"VX:\t\t\t{vx_est}\n"
        vy = f"VY:\t\t\t{vy_est}\r"
        lab.set(header+x+y+vx+vy)


    def update_canvas(self, event):
        """
        After click: extracts x,y-pos.
        Generates measurements, adds noise, position estimated by kalman filter.
        Updates canvas.
        """
        # true values
        x_true = (event.x)
        y_true = (event.y)

        # measure
        [x_meas, y_meas] = self.generate_measurements(X= [x_true, y_true])
        # add noise
        self.kf.make_measurement(np.array([x_meas, 0, y_meas, 0]).T)

        # update estimate
        K = np.array(self.kf.update_kalman_gain()).T
        [x_est, vx_est, y_est, vy_est] = np.array(self.kf.estimate_current_state()).T
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

        # clear canvas
        self.w.delete("all")

        # redraw
        if self.Show_True_Values:
            self.update_points(self.true_val_idx, x_true, y_true)
            self.draw_points(self.true_val_idx, type= "cross", color= self.canvas_true_val_color)
        if self.Show_Est_Values:
            self.update_points(self.est_val_idx, x_est, y_est)
            self.draw_points(self.est_val_idx, type= "oval", color= self.canvas_estimate_color)
        if self.Show_Measured_Values:
            self.update_points(self.meas_val_idx, x_meas, y_meas)
            self.draw_points(self.meas_val_idx, type= "oval", color= self.canvas_measurement_color)

        self.update_display_labels(self.display_var, x_true, y_true, x_meas, y_meas, x_est, y_est, vx_est, vy_est)
        self.update_matrix_label(self.P_var, self.kf.P, "P")
        self.update_matrix_label(self.K_var, self.kf.K, "K")


    def draw_points(self, val, type, color):
        """draw oval or cross on points in val"""
        d = self.canvas_oval_delta
        for [x, y] in val.T:
            if x > -1:
                if type == "cross":
                    self.draw_cross(x, y, color)
                else:
                    self.w.create_oval(x-d, y-d, x+d, y+d, fill= color)


    def update_points(self,val, x, y):
        """Shifts val one position and inserts x,y 0"""
        val[:, :] = np.roll(val, 1, axis= 1)
        val[:, 0] = [x, y]
        return val


    def draw_cross(self, x, y, color):
        x1 = int((x - self.canvas_oval_delta/2))
        x2 = int((x + self.canvas_oval_delta/2))
        y1 = int((y - self.canvas_oval_delta/2))
        y2 = int((y + self.canvas_oval_delta/2))
        self.w.create_line(x1, y1, x2+1, y2+1, fill= color)
        self.w.create_line(x1, y2, x2+1, y1+1, fill= color)


    def generate_measurements(self, X):
        """Returns X-array with noise"""
        """ Add random noise"""
        r =X + np.random.randn(1, len(X)) * self.sigma + self.mu
        return np.reshape(r, (len(X)))
