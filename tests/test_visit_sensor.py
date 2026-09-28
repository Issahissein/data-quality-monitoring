import unittest
from datetime import date

from src.sensor import VisitSensor


class TestVisitSensor(unittest.TestCase):

    def test_same_date_and_hour_same_result(self):
        sensor = VisitSensor(avg_visit=1500, std_visit=150)

        visit_1 = sensor.simulate_visit(
            date(year=2023, month=10, day=25), 10
        )
        visit_2 = sensor.simulate_visit(
            date(year=2023, month=10, day=25), 10
        )

        self.assertEqual(visit_1, visit_2)

    def test_null_data(self):
        sensor = VisitSensor(
            avg_visit=1500,
            std_visit=150,
            perc_break=1,
            perc_malfunction=0,
        )

        visit = sensor.simulate_visit(
            date(year=2023, month=10, day=25), 10
        )

        self.assertIsNone(visit)

    def test_abnormal_data(self):
        sensor = VisitSensor(
            avg_visit=1500,
            std_visit=150,
            perc_break=0,
            perc_malfunction=1,
        )

        visit = sensor.simulate_visit(
            date(year=2023, month=10, day=25), 10
        )

        self.assertGreater(visit, 200)


if __name__ == "__main__":
    unittest.main()