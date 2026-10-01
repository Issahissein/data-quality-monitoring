from datetime import date

from fastapi import FastAPI

from src.sensor import VisitSensor


app = FastAPI()


capteurs = {
    1: {
        1: VisitSensor(avg_visit=1500, std_visit=150),
        2: VisitSensor(avg_visit=1200, std_visit=120),
    },
    2: {
        3: VisitSensor(avg_visit=1000, std_visit=100),
        4: VisitSensor(avg_visit=800, std_visit=80),
    },
}


@app.get("/visits")
def get_visits(business_date: date):
    visits = []

    for store_id, store_sensors in capteurs.items():
        for sensor_id, capteur in store_sensors.items():
            for hour in range(24):
                visits.append(
                    {
                        "date": business_date,
                        "hour": hour,
                        "sensor_id": sensor_id,
                        "store_id": store_id,
                        "visitors": capteur.simulate_visit(
                            business_date,
                            hour,
                        ),
                        "unit": "visitors",
                    }
                )

    return visits