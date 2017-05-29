class MagneticParticle:
    mu0 = 1.2566e-06

    def __init__(self):
        self.magnetization = .0
        self.positive_saturation_field = .0
        self.negative_saturation_field = .0

    def apply_field(self, field_value: float) -> None:
        pass

    def set_up(self) -> None:
        pass

    def set_down(self) -> None:
        pass

    def draw(self, directory: str) -> None:
        pass

    def prepare_particle(self, neg_to_pos, pos_to_neg) -> None:
        pass
