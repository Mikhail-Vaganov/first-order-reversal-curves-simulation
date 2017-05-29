class MagneticMatter:
    def __init__(self):
        self.magnetization = 0
        self.positive_saturation_field = 0
        self.negative_saturation_field = 0

    def magnetize(self, field) -> None:
        pass

    def saturate_to_positive(self) -> None:
        pass

    def saturate_to_negative(self) -> None:
        pass

    def draw_matter_representation(self, directory) -> None:
        pass

    def prepare_matter(self, net_to_pos, pos_to_neg) -> None:
        pass
