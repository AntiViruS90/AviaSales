from lxml import etree
from exceptions import FileNotFoundError, InvalidXMLFormatError, MissingFieldError
from models import Flight, Pricing, Itinerary


def parse_xml(file_path):
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except etree.XMLSyntaxError:
        raise InvalidXMLFormatError(f"Invalid XML format in file: {file_path}")

    itineraries = []
    for flight in root.findall(".//Flights"):
        try:
            onward_flights = flight.find(".//OnwardPricedItinerary/Flights")
            return_flights = flight.find(".//ReturnPricedItinerary/Flights")
            pricing = flight.find(".//Pricing")

            itinerary = Itinerary(
                onward_flights=parse_flights(onward_flights),
                return_flights=parse_flights(return_flights),
                pricing=parse_pricing(pricing)
            )
            itineraries.append(itinerary)
        except Exception as e:
            raise MissingFieldError(f"Error parsing flight data: {str(e)}")

    return itineraries


def parse_flights(flights):
    if flights is None:
        return None
    return [parse_flight(flight) for flight in flights.findall(".//Flight")]


def parse_flight(flight):
    try:
        return Flight(
            carrier=flight.find("Carrier").text,
            flight_number=flight.find("FlightNumber").text,
            source=flight.find("Source").text,
            destination=flight.find("Destination").text,
            departure_time=flight.find("DepartureTimeStamp").text,
            arrival_time=flight.find("ArrivalTimeStamp").text,
            class_=flight.find("Class").text,
            stops=int(flight.find("NumberOfStops").text)
        )
    except AttributeError as e:
        raise MissingFieldError(f"Missing required field in flight data: {str(e)}")


def parse_pricing(pricing):
    if pricing is None:
        return None
    try:
        return Pricing(
            currency=pricing.get("currency"),
            total_amount=float(pricing.find(".//ServiceCharges[@ChargeType='TotalAmount']").text)
        )
    except AttributeError as e:
        raise MissingFieldError(f"Missing required field in pricing data: {str(e)}")
