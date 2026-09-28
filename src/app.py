from datetime import date

from fastapi import FastAPI

from src.sensor import VisitSensor


app = FastAPI()

capteur = VisitSensor(
    avg_visit=1500,
    std_visit=150,
)


@app.get("/visits")
def get_visits(business_date: date):
    visits = []

    for hour in range(24):
        visits.append(
            {
                "date": business_date,
                "hour": hour,
                "sensor_id": 1,
                "store_id": 1,
                "visitors": capteur.simulate_visit(
                    business_date,
                    hour,
                ),
                "unit": "visitors",
            }
        )

    return visits