from MagneticParticle import MagneticParticle
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


class SwParticle(MagneticParticle):
    critical_angle = 76.72 * np.pi / 180  # the angle at which the branches begin to intersect

    def __init__(self, psi_in_radians: float):
        super().__init__()
        self.psi = np.mod(np.abs(psi_in_radians), np.pi)
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
        result = minimize(energy, np.array([self.last_phi]), method='Nelder-Mead', tol=1e-8)

        self.last_phi = result.x/np.abs(result.x)*np.mod(np.abs(result.x), 2*np.pi)
        return np.cos(result.x)

    def _prepare_plot(self):
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

        self._draw_rectangular_border(ax)
        self._draw_axes(ax)
        ax.set_aspect(aspect='equal')

    def _draw_rectangular_border(self, ax: plt.Axes):
        max_magnetization = 1.0
        field_of_one = 1.0
        stepy = np.abs(max_magnetization / 10.0)
        border_yy = np.arange(-max_magnetization, max_magnetization + stepy, stepy)
        border_yx_rt = field_of_one * np.ones((len(border_yy), 1))
        border_yx_lt = -field_of_one * np.ones((len(border_yy), 1))

        stepx = np.abs(field_of_one / 10.0)
        border_xx = np.arange(-field_of_one, field_of_one + stepx, stepx)
        border_xy_up = max_magnetization * np.ones((len(border_xx), 1))
        border_xy_dn = -max_magnetization * np.ones((len(border_xx), 1))
        ax.plot(border_yx_rt, border_yy, '-.r',
                border_yx_lt, border_yy, '-.r',
                border_xx, border_xy_up, '-.r',
                border_xx, border_xy_dn, '-.r')

    def _draw_axes(self, ax: plt.Axes):
        ax.grid(which='both')
        max_magn = 1.0
        max_field = 2.0

        stepy = np.abs(max_magn/10)
        zero_yy = np.arange(-max_magn-stepy,max_magn+2*stepy, stepy )
        zero_yx = np.zeros((len(zero_yy), 1))

        stepx = np.abs(max_field / 10)
        zero_xx = np.arange(-max_field-stepx,max_field+2*stepx, stepx )
        zero_xy = np.zeros((len(zero_xx), 1))

        ax.plot(zero_yx, zero_yy, '--k', zero_xx, zero_xy, '--k');
        ax.set_ylim(np.min(zero_yy), np.max(zero_yy))
        ax.set_xlim(np.min(zero_xx), np.max(zero_xx))

    def draw_astroid(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        theta = np.arange(-np.pi, np.pi, 0.0001)
        x = np.cos(theta) ** 3
        y = np.sin(theta) ** 3
        ax.plot(x, y);
        ax.grid(which='both')
        plt.show()
