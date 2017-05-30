import numpy as np
import matplotlib.pyplot as plt
from MagneticParticle import MagneticParticle


class Hysteron(MagneticParticle):
    """A class representing an abstract particle with a rectangular hysteresis loop"""

    def __init__(self, a: float, b: float):

        super().__init__()

        self.alpha = a
        self.beta = b

        if a < b:
            raise Exception('Alpha parameter should be greater or equal than beta')

        self.magnetization = 1
        self.positive_saturation_field = (a + (a - b) / 2)
        self.negative_saturation_field = (b - (a - b) / 2)

    def set_up(self):
        self.magnetization = 1

    def set_down(self):
        self.magnetization = -1

    def apply_field(self, field_value: float):
        if field_value > self.alpha:
            self.magnetization = 1

        if field_value < self.beta:
            self.magnetization = -1

    def _prepare_plot(self):
        t = np.arange(0, 2 * np.pi, 0.01)
        input = -(self.alpha - self.beta) * np.cos(t) + (self.alpha + self.beta) / 2
        output = np.zeros(len(t))
        for i in range(len(t)):
            self.apply_field(input[i])
            output[i] = self.magnetization

        plt.plot(input, output, 'b-.')
        plt.grid()
        plt.title('Single hysteron')
        plt.xlabel('h(t)')
        plt.ylabel('m(h)')
        plt.xlim([np.amin(input), np.amax(input)])

    def prepare_particle(self, neg_to_pos, pos_to_neg):
        pass
