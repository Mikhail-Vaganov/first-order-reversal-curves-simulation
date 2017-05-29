from MagneticMatter import MagneticMatter
from MagneticParticle import MagneticParticle


class SingleParticleMatter(MagneticMatter):
    def __init__(self, particle: MagneticMatter):
        super().__init__()

        if not isinstance(particle, MagneticParticle):
            raise Exception('The particle should be an instance of the MagneticParticle class')

        self.particle = particle
        self.negative_saturation_field = particle.negative_saturation_field
        self.positive_saturation_field = particle.positive_saturation_field

    def magnetize(self, field: float) -> None:
        self.particle.apply_field(field)
        self.magnetization = self.particle.magnetization

    def saturate_to_positive(self):
        self.particle.set_up()
        self.magnetization = self.particle.magnetization

    def saturate_to_negative(self):
        self.particle.set_down()
        self.magnetization = self.particle.magnetization

    def draw_matter_representation(self, directory):
        self.particle.draw(directory)

    def prepare_matter(self, net_to_pos, pos_to_neg):
        self.particle.prepare_particle(net_to_pos, pos_to_neg)
