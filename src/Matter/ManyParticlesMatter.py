from MagneticMatter import MagneticMatter
import numpy as np
import matplotlib.pyplot as plt

from MagneticParticle import MagneticParticle


class ManyParticlesMatter(MagneticMatter):
    def __init__(self, particles):
        super().__init__()
        self.positive_saturation_field = -1
        self.negative_saturation_field = 1
        self.particles = particles
        for i in range(len(particles)):
            if self.positive_saturation_field < particles[i].positive_saturation_field:
                self.positive_saturation_field = particles[i].positive_saturation_field

            if self.negative_saturation_field > particles[i].negative_saturation_field:
                self.negative_saturation_field = particles[i].negative_saturation_field

            self.magnetization += particles[i].magnetization

        self.magnetization /= len(particles)

    def magnetize(self, field):
        self.magnetization = 0
        for i in range(len(self.particles)):
            self.particles[i].apply_field(field)
            self.magnetization += self.particles[i].magnetization
        self.magnetization /= len(self.particles)

    def saturate_to_positive(self):
        self.magnetization = 0
        for i in range(len(self.particles)):
            self.particles[i].set_up()
            self.magnetization += self.particles[i].magnetization
        self.magnetization /= len(self.particles)

    def saturate_to_negative(self):
        self.magnetization = 0
        for i in range(len(self.particles)):
            self.particles[i].set_down()
            self.magnetization += self.particles[i].magnetization
        self.magnetization /= len(self.particles)

    def draw_matter_representation(self, directory):
        hmax = self.positive_saturation_field
        hstep = 0.01
        field = np.concatenate(
            (np.arange(0, hmax, hstep), np.arange(hmax, -hmax, -hstep), np.arange(-hmax, hmax + hstep, hstep)))
        magnetization = np.zeros((len(field), 1))
        for i in range(len(field)):
            self.magnetize(field[i])
            magnetization[i] = self.magnetization

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title("M-H of multiparticle matter (n=" + str(len(self.particles)))

        if np.max(field) < 1000:
            ax.plot(field, magnetization)
            ax.set_xlabel("H, A/m")
            ax.set_xlabel("M, A/m")
        elif np.max(field) < 1e6:
            ax.plot(field / 1e3, magnetization / 1e3)
            ax.set_xlabel("H, kA/m")
            ax.set_xlabel("M, kA/m")
        else:
            ax.plot(field / 1e6, magnetization / 1e6)
            ax.set_xlabel("H, MA/m")
            ax.set_xlabel("M, MA/m")
