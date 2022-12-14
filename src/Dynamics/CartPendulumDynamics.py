import numpy as np

g = 9.8

class CartPendulum:

    def __init__(self, l1, l2, m1, m2, width, theta, x, y, z, color):

        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2
        self.width = width
        self.color = color
        self.z = z

        self.state = [theta, x, y, 0, 0, 0]
        self.state0 = [theta, x, y, 0, 0, 0]

        self.I = m2 * l2**2
        self.forcex = 0
        self.forcey = 0
        self.torque = 0

    def set_state(self, s):

        self.state = s
        self.forcex = 0
        self.forcey = 0
        self.torque = 0

    def get_state(self):

        s = np.array(self.state)

        return s

    def get_state_prime(self, s):

        #matrix equation to solve coupled DiffEQs
        z = self.z
        tot_mass = (self.m1 + self.m2)
        f1 = -(g * np.sin(s[0])) / self.l2 + self.torque / self.l2 - s[3] * z
        f2 = (s[3]**2 * self.m2 * self.l2 * np.sin(s[0])) / (tot_mass) + self.forcex / tot_mass
        f3 = (s[3]**2 * self.m2 * self.l2 * np.cos(s[0])) / (tot_mass) + self.forcey / tot_mass
        a1 = np.cos(s[0])  / self.l2
        a2 = -np.sin(s[0])  / self.l2
        a3 = np.cos(s[0]) * self.l2 * self.m2 / (tot_mass)
        a4 = -np.sin(s[0]) * self.l2 * self.m2 / (tot_mass)
        detA = 1 - (a1 * a3) - (a2 * a4)

        anga = (f1 - (f2 * a1) - (f3 * a2)) / detA
        ax = (-(f1 * a3) + (f2 * (1 - (a2 * a4))) + (f3 * a2 * a3)) / detA
        ay = (-(f1 * a4) + (f2 * a1 * a4) + (f3 * (1 - (a1 * a3)))) / detA

        s_dot = np.array([s[3], s[4], s[5], anga, ax, ay])

        return s_dot
    
    def get_state_size(self):
        return 6

    def get_lengths(self):
        return self.l1, self.l2

    def get_masses(self):
        return self.m1, self.m2

    def get_width(self):
        return self.width

    def get_color(self):
        return self.color

    def impulse(self, direction):
        force = 10000
        if direction == 0:
            self.torque = -force / 10
        elif direction == 1:
            self.torque = force / 10
        elif direction == 2:
            self.forcey = force
        elif direction == 3:
            self.forcey = -force
        elif direction == 4:
            self.forcex = force
        elif direction == 5:
            self.forcex = -force