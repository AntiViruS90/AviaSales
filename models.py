from pydantic import BaseModel
from typing import List, Optional


class Flight(BaseModel):
    carrier: str
    flight_number: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    class_: str
    stops: int


class Pricing(BaseModel):
    currency: str
    total_amount: float


class Itinerary(BaseModel):
    onward_flights: Optional[List[Flight]]
    return_flights: Optional[List[Flight]]
    pricing: Optional[Pricing]
