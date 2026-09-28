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
    total_visits = 0

    for hour in range(24):
        total_visits += capteur.simulate_visit(
            business_date,
            hour,
        )

    return {
        "date": business_date,
        "visitors": total_visits,
    }