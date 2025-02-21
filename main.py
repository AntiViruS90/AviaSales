from fastapi import FastAPI
from service import get_onward_flights, get_best_flights, compare_flights
from config import FILE_1_PATH, FILE_2_PATH

app = FastAPI(
    title="Flight Service API",
    description="API для анализа данных о перелётах из XML-файлов",
    version="1.0.0",
    docs_url="/swagger",
)


@app.get("/onward-flights", summary="Получить все варианты перелёта из DXB в BKK")
def onward_flights():
    return get_onward_flights(FILE_1_PATH)


@app.get("/best-flights", summary="Получить лучшие варианты перелёта")
def best_flights():
    return get_best_flights(FILE_1_PATH)


@app.get("/compare-flights", summary="Сравнить результаты двух файлов")
def compare():
    return compare_flights(FILE_1_PATH, FILE_2_PATH)
