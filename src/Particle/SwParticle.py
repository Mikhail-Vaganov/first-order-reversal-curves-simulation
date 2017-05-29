from MagneticParticle import MagneticParticle
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


class SwParticle(MagneticParticle):
    critical_angle = 76.72 * np.pi / 180  # the angle at which the branches begin to intersect

    def __init__(self, psi_in_radians: float):
        super().__init__()
        self.psi = psi_in_radians
        self.last_phi = psi_in_radians
        self.last_branch = 1
        self.last_applied_field = 0
        self.magnetization = np.cos(psi_in_radians)

        t = np.cbrt(np.tan(psi_in_radians))
        self.switching_field = np.sqrt(1 - t ** 2 + t ** 4) / (1 + t ** 2)
        self.positive_saturation_field = 1.5
        self.negative_saturation_field = -1.5

    def set_up(self):
        self.apply_field(self.positive_saturation_field)

    def set_down(self):
        self.apply_field(self.negative_saturation_field)

    def apply_field(self, field_value: float):
        if field_value >= self.switching_field:
            self.last_branch = 1
        elif field_value <= -self.switching_field:
            self.last_branch = -1

        self.magnetization = self.cos_search(field_value)
        self.last_applied_field = field_value

    def cos_search(self, h):
        if self.last_branch == 1:
            if self.psi < np.pi / 2:
                x = np.arange(0, np.pi, 0.001)
            else:
                x = np.arange(-np.pi, 0, 0.001)
        else:
            if self.psi < np.pi / 2:
                x = np.arange(-np.pi, 0, 0.001)
            else:
                x = np.arange(0, np.pi, 0.001)

        energy = lambda phi: 0.5 * np.sin(self.psi - phi) ** 2 - h * np.cos(phi)
        result = minimize(energy, np.array([self.last_phi]), method='Nelder-Mead', tol=1e-6)
        self.last_phi = result.x
        return np.cos(result.x)

    def draw(self, directory: str):
        hmax = self.positive_saturation_field
        hstep = 0.01
        field = np.concatenate(
            (np.arange(0, hmax, hstep), np.arange(hmax, -hmax, -hstep), np.arange(-hmax, hmax + hstep, hstep)))
        magnetization = np.zeros([len(field), 1])

        for i in range(len(field)):
            self.apply_field(field[i])
            magnetization[i] = self.magnetization

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(field, magnetization)
        ax.set_title("Hyseresis of the Stoner-Wohlfarth particle at $\psi$ =" + str(
            np.round(self.psi / np.pi * 180)) + "$^\circ$" + " SwField=" + str(np.round(self.switching_field, 2)))

        self.save_current_plot(directory)
        plt.show()
