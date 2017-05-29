import numpy as np
import matplotlib.pyplot as plt


class MagnetizationCurve:
    def load_from_h_m_values_file(self, path_to_data_file):
        f = open(path_to_data_file)
        line = f.readline()
        col_names = line.split("\t")

        data = np.loadtxt(path_to_data_file, skiprows=1)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(data[:, 0], data[:, 1])
        ax.plot(data[:, 0], data[:, 1])
        ax.set_xlabel(col_names[0])
        ax.set_ylabel(col_names[1])
        ax.grid(axis='both')
        plt.show()
