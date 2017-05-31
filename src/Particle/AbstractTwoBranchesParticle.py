from MagneticParticle import MagneticParticle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


class AbstractTwoBranchesParticle(MagneticParticle):
    def __init__(self, path_to_data_file, upper_to_bottom_switching_field: float,
                 bottom_to_upper_switching_field: float):
        super().__init__()

        self.upper_to_bottom_switching_field = upper_to_bottom_switching_field
        self.bottom_to_upper_switching_field = bottom_to_upper_switching_field

        data = np.loadtxt(path_to_data_file, skiprows=1)
        upper_branch = data[data[:, 0] == 1]
        bottom_branch = data[data[:, 0] == -1]
        self.upper_branch = upper_branch[upper_branch[:, 1].argsort()]
        self.bottom_branch = bottom_branch[bottom_branch[:, 1].argsort()]

        self.interpolated_upper_magnetization = interp1d(self.upper_branch[:, 1], self.upper_branch[:, 2])
        self.interpolated_bottom_magnetization = interp1d(self.bottom_branch[:, 1], self.bottom_branch[:, 2])
        self.interpolated_upper_distance = interp1d(self.upper_branch[:, 1], self.upper_branch[:, 4])
        self.interpolated_bottom_distance = interp1d(self.bottom_branch[:, 1], self.bottom_branch[:, 4])
        self.min_data_field_upper = np.min(self.upper_branch[:, 1])
        self.max_data_field_upper = np.max(self.upper_branch[:, 1])
        self.min_data_field_bottom = np.min(self.bottom_branch[:, 1])
        self.max_data_field_bottom = np.max(self.bottom_branch[:, 1])

        self.max_common_field = self.max_data_field_upper if self.max_data_field_upper < self.max_data_field_bottom else self.max_data_field_bottom
        self.min_common_field = self.min_data_field_upper if self.min_data_field_upper > self.min_data_field_bottom else self.min_data_field_bottom

        self.upper_chi_zero = 0
        if self.min_data_field_upper != 0:
            self.upper_chi_zero = self.interpolated_upper_magnetization(
                self.min_data_field_upper) / self.min_data_field_upper

        self.bottom_chi_zero = 0
        if self.min_data_field_bottom != 0:
            self.bottom_chi_zero = self.interpolated_bottom_magnetization(
                self.min_data_field_bottom) / self.min_data_field_bottom

        len_upper_data = len(self.upper_branch)
        a_upper_saturation = (self.upper_branch[len_upper_data - 1, 2] * self.upper_branch[len_upper_data - 2, 1] -
                              self.upper_branch[len_upper_data - 2, 2] * self.upper_branch[len_upper_data - 1, 1]) / (
                                 self.upper_branch[(len(self.upper_branch) - 12), 1] - self.upper_branch[
                                     (len(self.upper_branch) - 1), 1])

        b_upper_saturation = (self.upper_branch[(len(self.upper_branch) - 1), 2] - self.upper_branch[
            (len(self.upper_branch) - 2), 2]) / (
                                 self.upper_branch[(len(self.upper_branch) - 1), 1] - self.upper_branch[
                                     (len(self.upper_branch) - 2), 1])

        self.upper_saturation_magnetization = lambda h: a_upper_saturation + h * b_upper_saturation

        len_bottom_data = len(self.bottom_branch)
        a_bottom_saturation = (self.bottom_branch[len_bottom_data - 1, 2] * self.bottom_branch[len_bottom_data - 2, 1] -
                               self.bottom_branch[len_bottom_data - 2, 2] * self.bottom_branch[
                                   len_bottom_data - 1, 1]) / (
                                  self.bottom_branch[(len(self.bottom_branch) - 12), 1] - self.bottom_branch[
                                      (len(self.bottom_branch) - 1), 1])

        b_bottom_saturation = (self.bottom_branch[(len(self.bottom_branch) - 1), 2] - self.bottom_branch[
            (len(self.bottom_branch) - 2), 2]) / (
                                  self.bottom_branch[(len(self.bottom_branch) - 1), 1] - self.bottom_branch[
                                      (len(self.bottom_branch) - 2), 1])

        self.bottom_saturation_magnetization = lambda h: a_bottom_saturation + h * b_bottom_saturation

        self.branch = 1
        self.last_applied_field = 0

    def _prepare_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        h = np.concatenate(
            (np.arange(0, 1, 0.01), np.arange(1, 0, -0.01), np.arange(0, -1, -0.01), np.arange(-1, 0.01, 0.01)))
        m = np.zeros([len(h), 1])
        for i in range(len(h)):
            self.apply_field(h[i])
            m[i] = self.magnetization

        ax.plot(h, m)
        ax.set_xlabel("h")
        ax.set_ylabel("m")
        ax.grid(axis='both')
        ax.set_title('m(h) - interpolated')

    def _prepare_four_plots(self):
        f, axarr = plt.subplots(2, 3)

        axarr[0, 0].plot(self.upper_branch[:, 1], self.upper_branch[:, 2])
        axarr[0, 0].plot(self.bottom_branch[:, 1], self.bottom_branch[:, 2])
        axarr[0, 0].set_xlabel("h")
        axarr[0, 0].set_ylabel("m")
        axarr[0, 0].grid(axis='both')
        axarr[0, 0].set_title('m(h) - clear data')

        axarr[1, 0].plot(self.upper_branch[:, 1], self.upper_branch[:, 4])
        axarr[1, 0].plot(self.bottom_branch[:, 1], self.bottom_branch[:, 4])
        axarr[1, 0].set_xlabel("h")
        axarr[1, 0].set_ylabel("q")
        axarr[1, 0].grid(axis='both')
        axarr[1, 0].set_title('q(h) - clear data')

        h_upper = np.linspace(self.min_data_field_upper, self.max_data_field_upper, 101)
        h_bottom = np.linspace(self.min_data_field_bottom, self.max_data_field_bottom, 101)

        axarr[0, 1].plot(h_upper, self.interpolated_upper_magnetization(h_upper))
        axarr[0, 1].plot(h_bottom, self.interpolated_bottom_magnetization(h_bottom))
        axarr[0, 1].set_xlabel("h")
        axarr[0, 1].set_ylabel("m")
        axarr[0, 1].grid(axis='both')
        axarr[0, 1].set_title('m(h) - interpolated')

        axarr[1, 1].plot(h_upper, self.interpolated_upper_distance(h_upper))
        axarr[1, 1].plot(h_bottom, self.interpolated_bottom_distance(h_bottom))
        axarr[1, 1].set_xlabel("h")
        axarr[1, 1].set_ylabel("q")
        axarr[1, 1].grid(axis='both')
        axarr[1, 1].set_title('q(h) - interpolated')

        h = np.concatenate(
            (np.arange(0, 1, 0.01), np.arange(1, 0, -0.01), np.arange(0, -1, -0.01), np.arange(-1, 0.01, 0.01)))
        m = np.zeros([len(h), 1])
        for i in range(len(h)):
            self.apply_field(h[i])
            m[i] = self.magnetization

        axarr[0, 2].plot(h, m)
        axarr[0, 2].set_xlabel("h")
        axarr[0, 2].set_ylabel("m")
        axarr[0, 2].grid(axis='both')
        axarr[0, 2].set_title('m(h) - Via applied field')

    def apply_field(self, field_value: float):

        if field_value < 0:
            applied_field = np.abs(field_value)
        else:
            applied_field = field_value

        if self.last_applied_field * field_value < 0:
            self.branch = 1

        if applied_field > self.upper_to_bottom_switching_field:
            self.branch = -1

        if applied_field < self.bottom_to_upper_switching_field:
            self.branch = 1

        if self.branch == 1:
            if applied_field < self.min_data_field_upper:
                self.magnetization = self.upper_chi_zero * applied_field
            else:
                self.magnetization = self.interpolated_upper_magnetization(applied_field)

        if self.branch == -1:
            if applied_field > self.max_data_field_bottom:
                self.magnetization = self.bottom_saturation_magnetization(applied_field)
            else:
                self.magnetization = self.interpolated_bottom_magnetization(applied_field)

        if field_value < 0:
            self.magnetization = -self.magnetization

        self.last_applied_field =  field_value
