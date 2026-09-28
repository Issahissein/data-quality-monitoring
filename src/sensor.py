from datetime import date

import numpy as np


class VisitSensor:
    """
    Simulates a sensor at the entrance of a mall.
    """

    def __init__(self, avg_visit: int, std_visit: int) -> None:
        """Initialize sensor"""
        self.avg_visit = avg_visit
        self.std_visit = std_visit

    def simulate_visit(self, business_date: date, hour: int) -> int:
        """Simulate the number of persons detected by the sensor
        during a given hour."""

        # Ensure reproducibility for the same day and hour
        np.random.seed(seed=business_date.toordinal() * 24 + hour)

        visit = np.random.normal(
            self.avg_visit / 24,
            self.std_visit / 24,
        )

        return int(np.floor(visit))


if __name__ == "__main__":
    capteur = VisitSensor(avg_visit=1500, std_visit=150)

    print(capteur.simulate_visit(date(year=2023, month=10, day=25), 10))
    print(capteur.simulate_visit(date(year=2023, month=10, day=25), 10))