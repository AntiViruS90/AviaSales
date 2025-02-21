from datetime import datetime
from typing import List, Dict, Optional
from parsers import parse_xml
from models import Itinerary, Flight


def calculate_duration(departure: str, arrival: str) -> int:
    """Рассчитывает продолжительность перелёта в минутах."""
    fmt = "%Y-%m-%dT%H%M"
    start = datetime.strptime(departure, fmt)
    end = datetime.strptime(arrival, fmt)
    return int((end - start).total_seconds() / 60)


def get_flight_info(itinerary: Itinerary) -> Dict:
    """Извлекает информацию о перелёте."""
    if not itinerary.onward_flights:
        return None

    total_amount = itinerary.pricing.total_amount if itinerary.pricing else 0
    total_duration = sum(
        calculate_duration(flight.departure_time, flight.arrival_time)
        for flight in itinerary.onward_flights
    )
    total_stops = sum(flight.stops for flight in itinerary.onward_flights)

    return {
        "route": " → ".join(
            [flight.source for flight in itinerary.onward_flights] + [itinerary.onward_flights[-1].destination]),
        "total_amount": total_amount,
        "total_duration": total_duration,
        "total_stops": total_stops,
        "flights": itinerary.onward_flights
    }


def get_onward_flights(file_path: str) -> Dict:
    """Возвращает все варианты перелёта из DXB в BKK."""
    data = parse_xml(file_path)
    flights_info = [get_flight_info(itinerary) for itinerary in data if get_flight_info(itinerary)]

    if not flights_info:
        return {"error": "No flights found"}

    return {"onward_flights": flights_info}


def get_best_flights(file_path: str) -> Dict:
    data = parse_xml(file_path)
    flights_info = [get_flight_info(itinerary) for itinerary in data if get_flight_info(itinerary)]

    if not flights_info:
        return {"error": "No flights found"}

    # Самый дешёвый
    cheapest = min(flights_info, key=lambda x: x["total_amount"])
    # Самый дорогой
    most_expensive = max(flights_info, key=lambda x: x["total_amount"])
    # Самый быстрый
    fastest = min(flights_info, key=lambda x: x["total_duration"])
    # Самый долгий
    slowest = max(flights_info, key=lambda x: x["total_duration"])
    # Оптимальный (баланс цены и времени)
    optimal = min(
        flights_info,
        key=lambda x: (x["total_amount"] / 1000) + (x["total_duration"] / 60)  # Нормализация
    )

    return {
        "cheapest": cheapest,
        "most_expensive": most_expensive,
        "fastest": fastest,
        "slowest": slowest,
        "optimal": optimal
    }


def compare_flights(file1_path: str, file2_path: str) -> Dict:
    data1 = parse_xml(file1_path)
    data2 = parse_xml(file2_path)

    flights_info1 = [get_flight_info(itinerary) for itinerary in data1 if get_flight_info(itinerary)]
    flights_info2 = [get_flight_info(itinerary) for itinerary in data2 if get_flight_info(itinerary)]

    comparison = []
    for flight1 in flights_info1:
        flight2 = next((f for f in flights_info2 if f["route"] == flight1["route"]), None)
        comparison.append({
            "route": flight1["route"],
            "file1_total_amount": flight1["total_amount"],
            "file2_total_amount": flight2["total_amount"] if flight2 else None,
            "file1_total_duration": flight1["total_duration"],
            "file2_total_duration": flight2["total_duration"] if flight2 else None,
            "file1_total_stops": flight1["total_stops"],
            "file2_total_stops": flight2["total_stops"] if flight2 else None
        })

    # Добавляем маршруты, которые есть только во втором файле
    for flight2 in flights_info2:
        if not any(f["route"] == flight2["route"] for f in flights_info1):
            comparison.append({
                "route": flight2["route"],
                "file1_total_amount": None,
                "file2_total_amount": flight2["total_amount"],
                "file1_total_duration": None,
                "file2_total_duration": flight2["total_duration"],
                "file1_total_stops": None,
                "file2_total_stops": flight2["total_stops"]
            })

    return {"comparison": comparison}
