import itertools
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
from mpl_toolkits.mplot3d import Axes3D

from MagneticMatter import MagneticMatter


class PikeFORC:
    N = 101
    SF = 4

    def __init__(self, maxHc: float, minHu: float, maxHu: float, matter: MagneticMatter, directory: str):
        minHc = 0
        self.maxHr = maxHu - minHc
        self.minHr = minHu - maxHc
        self.maxH = maxHu + maxHc
        self.minH = self.minHr
        self.Hr = np.round(np.linspace(self.minHr, self.maxHr, self.N, dtype=float), decimals=4)
        self.Hstep = np.mean(np.diff(self.Hr))
        self.minHc = minHc
        self.maxHc = maxHc
        self.minHu = minHu
        self.maxHu = maxHu

        if self.maxH < self.maxHr:
            self.maxH = self.maxHr

        self.H = np.concatenate((self.Hr, np.arange((self.Hr[self.N - 1] + self.Hstep), self.maxH, self.Hstep)))

        self.Hgrid, self.Hrgrid = np.meshgrid(self.H, self.Hr)

        grid_size = np.shape(self.Hgrid)
        self.PgridHHr = np.empty(grid_size)
        self.PgridHHr.fill(np.nan)
        self.PgridHcHu = np.empty(grid_size)
        self.PgridHcHu.fill(np.nan)
        self.Hugrid = np.empty(grid_size)
        self.Hugrid.fill(np.nan)
        self.Hcgrid = np.empty(grid_size)
        self.Hcgrid.fill(np.nan)
        self.Mgrid = np.empty(grid_size)
        self.Mgrid.fill(np.nan)

        self.matter = matter
        self.FolderForResults_common = os.path.join(directory, 'Common')
        self.FolderForResults_with_time = os.path.join(directory, 'By time',
                                                       datetime.datetime.now().strftime("%H_%M_%S"))

        if not os.path.exists(self.FolderForResults_common):
            os.makedirs(self.FolderForResults_common)

        if not os.path.exists(self.FolderForResults_with_time):
            os.makedirs(self.FolderForResults_with_time)

    def magnetization_forc(self):
        for i in range(len(self.Hr) - 1, 0, -1):
            self.matter.saturate_to_positive()
            self.matter.magnetize(self.Hr[i])

            for j in range(len(self.H)):
                if self.H[j] >= self.Hr[i]:
                    self.matter.magnetize(self.H[j])
                    self.Mgrid[i, j] = self.matter.magnetization

    def calculate_forc_distribution(self):
        for i in range(len(self.Hr)):
            for j in range(len(self.H)):
                if self.H[j] >= self.Hr[i]:
                    self.PgridHHr[i, j] = self._get_local_forc_distribution(i, j)

        for i in range(len(self.Hr)):
            for j in range(len(self.H)):
                self.Hugrid[i, j] = np.round((self.H[j] + self.Hr[i]) / 2.0, 4)
                self.Hcgrid[i, j] = np.round((self.H[j] - self.Hr[i]) / 2.0, 4)
                self.PgridHcHu[i, j] = self.PgridHHr[i, j]

                if self.Hugrid[i, j] > self.maxHu or self.Hugrid[i, j] < self.minHu:
                    self.PgridHcHu[i, j] = np.NaN

                if self.Hcgrid[i, j] > self.maxHc or self.Hcgrid[i, j] < self.minHc:
                    self.PgridHcHu[i, j] = np.NaN

    def _get_local_forc_distribution(self, i, j) -> (float, np.NaN):
        h = np.array([])
        hr = np.array([])
        m = np.array([])

        for u in range(i - self.SF, i + self.SF, 1):
            if u < 0 or u >= len(self.Hr):
                continue
            for v in range(j - self.SF, j + self.SF, 1):
                if v < 0 or v >= len(self.H):
                    continue

                if np.isnan(self.Mgrid[u, v]):
                    continue

                hr = np.append(hr, self.Hrgrid[u, v])
                h = np.append(h, self.Hgrid[u, v])
                m = np.append(m, self.Mgrid[u, v])

        if len(m) < 6:
            return np.NaN

        an = self._poly2_surface_fit(hr, h, m)

        return -an[0][5]

    def _poly2_surface_fit(self, hr: np.ndarray, h: np.ndarray, m: np.ndarray) -> tuple:
        # Xa=m, where x - products of h and hr
        # m = a0 + a1*hr + a2*h + a3*hr**2 + a4*h**2 + a5*hr*h
        a_number = 6
        X = np.zeros((len(m), a_number))

        X[:, 0] = hr ** 0 * h ** 0
        X[:, 1] = hr ** 1 * h ** 0
        X[:, 2] = hr ** 0 * h ** 1
        X[:, 3] = hr ** 2 * h ** 0
        X[:, 4] = hr ** 0 * h ** 2
        X[:, 5] = hr ** 1 * h ** 1

        a = np.linalg.lstsq(X, m)
        return a

    def draw_magnetization_forc(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(self.Hgrid, self.Hrgrid, self.Mgrid)
        plt.show()

    def draw_forc_diagram_hc_hu(self):
        n_contour = 9

        max_z = np.nanmax(np.nanmax(self.PgridHcHu))

        if self.maxHc > 1e3:
            plt.contourf(self.Hcgrid / 1e3, self.Hugrid / 1e3, self.PgridHcHu / 1e3, n_contour,
                         cmap=plt.get_cmap('seismic'), vmin=-max_z, vmax=max_z)
            plt.xlabel('$H_c$, (kA/m)')
            plt.ylabel('$H_u$, (kA/m)')
            plt.xlim([self.minHc / 1e3, self.maxHc / 1e3])
            plt.ylim([self.minHu / 1e3, self.maxHu / 1e3])
        elif self.maxHc > 1e6:
            plt.contourf(self.Hcgrid / 1e6, self.Hugrid / 1e6, self.PgridHcHu / 1e6, n_contour,
                         cmap=plt.get_cmap('seismic'), vmin=-max_z, vmax=max_z)
            plt.xlabel('$H_c$, (MA/m)')
            plt.ylabel('$H_u$, (MA/m)')
            plt.xlim([self.minHc / 1e6, self.maxHc / 1e6])
            plt.ylim([self.minHu / 1e6, self.maxHu / 1e6])
        else:
            plt.contourf(self.Hcgrid, self.Hugrid, self.PgridHcHu, n_contour, cmap=plt.get_cmap('seismic'), vmin=-max_z,
                         vmax=max_z)
            plt.xlabel('$H_c$, (A/m)')
            plt.ylabel('$H_u$, (A/m)')
            plt.xlim([self.minHc, self.maxHc])
            plt.ylim([self.minHu, self.maxHu])

        plt.title('FORC diagram', fontsize=14)
        plt.colorbar()
        plt.axes().set_aspect(aspect='equal')

        folder_for_forc_hc_hu_diagram = os.path.join(self.FolderForResults_common, 'countur_FORC_diagram_in_Hc_Hu')
        if not os.path.exists(folder_for_forc_hc_hu_diagram):
            os.makedirs(folder_for_forc_hc_hu_diagram)

        plt.savefig(os.path.join(folder_for_forc_hc_hu_diagram, datetime.datetime.now().strftime("%H_%M_%S") + '.jpg'))
        plt.show()
