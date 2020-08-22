import tkinter as tk
import numpy as np
from kalman import KalmanFilter

class Gui:

    def __init__(self, master):
        # settings
        master.title("Estimator")
        master_width = 1000
        master_heigth = 600
        master.geometry(f"{master_width}x{master_heigth}")
        self.Show_True_Values = True
        self.Show_Measured_Values = True
        self.Show_Est_Values = True
        self.sigma = 30
        self.mu = 0
        self.canvas_oval_delta = 3
        stored_values = 40

        # frames
        canvas_width = 1000
        canvas_height =400
        main_frame_heigth = 200
        canvas_frame = tk.Frame(master, height= canvas_height)
        main_frame = tk.Frame(master, width= canvas_width, height= main_frame_heigth)

        # layout
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # main frames
        canvas_frame.grid(row=0, column= 0,  sticky= "NESW", padx= 5, pady= 5)
        main_frame.grid(row=1, column= 0, sticky= "NESW", padx= 5, pady= 5)

        # canvas
        self.canvas_bg_color = "black"
        self.canvas_true_val_color = "red"
        self.canvas_measurement_color = "blue"
        self.canvas_estimate_color = "green"
        self.w = tk.Canvas(canvas_frame,
               bg= self.canvas_bg_color)
        self.w.pack(fill="both", expand=True)
        self.w.bind("<B1-Motion>", self.update_canvas)  #drag
        self.w.bind("<Button-1>", self.update_canvas)   #click

        # display frames
        frame_width=350
        padx= 40
        pady=5
        display_frame = tk.Frame(main_frame, width=frame_width, height= main_frame_heigth, padx= padx, pady= pady)
        display_frame.grid(row=0, column=0, sticky= "NW")
        P_frame = tk.Frame(main_frame, width=frame_width, height= main_frame_heigth, padx= padx, pady= pady)
        P_frame.grid(row=0, column=1, sticky= "NW")
        K_frame = tk.Frame(main_frame, width=frame_width, height= main_frame_heigth, padx= padx, pady= pady)
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
        self.kf = KalmanFilter(X0)


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

        self.update_display_labels(self.display_var, x_true, y_true, x_meas, y_meas, x_est, y_est, vx_est, vy_est)
        self.update_matrix_label(self.P_var, self.kf.P, "P")
        self.update_matrix_label(self.K_var, self.kf.K, "K")


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
