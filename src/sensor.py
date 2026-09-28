from datetime import date

import numpy as np


class VisitSensor:
    """
    Simulates a sensor at the entrance of a mall.
    """

    def __init__(
        self,
        avg_visit: int,
        std_visit: int,
        perc_break: float = 0.015,
        perc_malfunction: float = 0.015,
    ) -> None:
        """Initialize sensor"""
        self.avg_visit = avg_visit
        self.std_visit = std_visit
        self.perc_malfunction = perc_malfunction
        self.perc_break = perc_break

    def simulate_visit(self, business_date: date, hour: int):
        """Simulate the number of persons detected by the sensor
        during a given hour."""

        # Ensure reproducibility for the same day and hour
        np.random.seed(seed=business_date.toordinal() * 24 + hour)

        # Generate the normal number of visitors
        visit = np.random.normal(
            self.avg_visit / 24,
            self.std_visit / 24,
        )

        # Generate a random value to simulate sensor problems
        random_value = np.random.random()

        # Sensor is broken: null data
        if random_value < self.perc_break:
            return None

        # Sensor malfunction: improbable value
        if random_value < self.perc_break + self.perc_malfunction:
            visit *= 10

        return int(np.floor(visit))


if __name__ == "__main__":
    capteur = VisitSensor(
        avg_visit=1500,
        std_visit=150,
        perc_break=0.015,
        perc_malfunction=0.015,
    )

    for day in range(1, 32):
        for hour in range(24):
            visit = capteur.simulate_visit(
                date(year=2023, month=10, day=day),
                hour,
            )

            if visit is None or visit > 200:
                print(day, hour, visit)