import numpy as np

g = 9.8

class CartPendulumInX:

    def __init__(self, l1, l2, m1, m2, width, theta, x, y, color):

        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2
        self.width = width
        self.color = color

        self.y = y
        self.state = [theta, x, 0, 0]
        self.state0 = [theta, x, 0, 0]

        self.I = m2 * l2**2
        self.forcex = 0

        self.torque = 0

    def set_state(self, s):

        self.state = s
        self.forcex = 0

        self.torque = 0

    def get_state(self):

        s = np.array(self.state)

        return s

    def get_state_prime(self, s):

        #matrix equation to solve coupled DiffEQs
        tot_mass = (self.m1 + self.m2)
        f1 = -(g * np.sin(s[0])) / self.l2
        f2 = (s[2]**2 * self.m2 * self.l2 * np.sin(s[0])) / (tot_mass) + self.forcex

        a1 = np.cos(s[0])  / self.l2
        a2 = np.cos(s[0]) * self.l2 * self.m2 / (tot_mass)

        detA = 1 - (a1 * a2)

        anga = (f1 - (f2 * a1)) / detA
        ax = (f2 - (f1 * a2)) / detA
        
        UIanga = self.torque / self.I


        s_dot = np.array([s[2], s[3], anga + UIanga, ax])

        return s_dot
    
    def get_state_size(self):
        return 4

    def get_y(self):
        return self.y

    def get_lengths(self):
        return self.l1, self.l2

    def get_masses(self):
        return self.m1, self.m2

    def get_width(self):
        return self.width

    def get_color(self):
        return self.color

    def impulse(self, direction):
        force = 1000
        if direction == 0:
            self.torque = -force * self.l2 / 1
        elif direction == 1:
            self.torque = force * self.l2 / 1
        elif direction == 4:
            self.forcex = force
        elif direction == 5:
            self.forcex = -force