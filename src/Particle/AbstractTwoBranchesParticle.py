from MagneticParticle import MagneticParticle
import numpy as np
import matplotlib.pyplot as plt


class AbstractTwoBranchesParticle(MagneticParticle):
    def load_soft_magnetic_symmetric_branches_from_file(self, path_to_data_file):
        data = np.loadtxt(path_to_data_file, skiprows=1)
        upper_branch = data[data[:, 0] == 1]
        bottom_branch = data[data[:, 0] == -1]
        self.upper_branch = upper_branch[upper_branch[:, 1].argsort()]
        self.bottom_branch = bottom_branch[bottom_branch[:, 1].argsort()]

    def draw(self, directory: str):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.upper_branch[:, 1], self.upper_branch[:, 2])
        ax.plot(self.bottom_branch[:, 1], self.bottom_branch[:, 2])
        ax.set_xlabel("h")
        ax.set_ylabel("m")
        ax.grid(axis='both')
        self.save_current_plot(directory)
        plt.show()

