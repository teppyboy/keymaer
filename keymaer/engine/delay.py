from random import uniform


class Delay:
    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max

    def random(self) -> float:
        return uniform(self.min, self.max)

    @staticmethod
    def from_dict(delay_dict: dict) -> "Delay":
        return Delay(delay_dict["min"], delay_dict["max"])