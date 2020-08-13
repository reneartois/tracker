import numpy as np
from scipy.integrate import odeint
from matplotlib import pyplot as plt

class Cannon():

    def __init__(self, angle, speed):
        """Fire a cannon
        ..
        mass: kg
        angle: degr, (horizontal = 0)
        speed: km/h, direction: angle

        system states: x, y: pos
        vx' = 0
        vy' = -g

        """
        rad = np.radians(angle)
        self.vy0 = np.sin(rad) * speed
        self.vx0 = np.cos(rad) * speed
        self.time_vec = np.linspace(0, 10, 100)
        self.g = 9.81
        # x, y, vx, vy
        self.X0 = [0, 0, self.vx0, self.vy0]
        self.sol = None


    def traj(self, states, t):
        x, y, vx, vy = states
        dx = vx
        dy = vy
        dvx = 0
        dvy = -1 * self.g
        dydt = [dx, dy, dvx, dvy]
        return dydt


    def solve(self):
        self.sol = odeint(self.traj, self.X0, self.time_vec)

    def solve_analytically(self):
        a = 0
        x = self.X0[2]*10 + 0.5*a*10**2
        a = -1*self.g
        y = self.X0[3]*10 + 0.5*a*10**2
        print(x, y)


    def plot(self):
        sol = self.sol
        t = self.time_vec
        x = sol[:, 0]
        y = sol[:, 1]
        dx = sol[:, 2]
        dy = sol[:, 3]
        plt.plot(x, y, 'b', label='trajectory')
        plt.legend(loc='best')
        plt.grid()
        plt.show()
