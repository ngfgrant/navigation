# -*- coding: utf-8 -*-

from copy import copy
from decimal import Decimal, Context, setcontext
from math import asin
from math import atan2
from math import cos
from math import pi
from math import sin
from math import radians


MULTIPLIER = {
    "KM": Decimal(1.852),
    "MILE": Decimal(1.15078)
}

DEGREE_IN_MINUTES = Decimal(60)
DEGREE_IN_SECONDS = Decimal(3600)
EARTH_RADIUS_IN_KM = Decimal(6378.137)
HALF_TURN = Decimal(180)
ONE_TURN = Decimal(360)
ONE_RADIAN = Decimal((Decimal(pi) / HALF_TURN))

decimal_context = Context(prec=16)
setcontext(decimal_context)


class Time(object):
    def __init__(self, seconds):
        if not isinstance(seconds, int):
            raise TypeError(
                "Time must be given in seconds as an integer")
        if seconds < 1:
            raise ValueError("Time must be a positive, non-zero integer")
        self._seconds = seconds

    def __str__(self):
        return "Time: {} seconds".format(self._seconds)

    @property
    def in_seconds(self):
        return self._seconds

    @property
    def in_minutes(self):
        return Decimal(self._seconds / 60)

    @property
    def in_hours(self):
        return Decimal((self._seconds / 60) / 60)


class Distance(object):
    def __init__(self, nautical_miles):
        try:
            decimal_nm = Decimal(nautical_miles)
        except Exception as e:
            print(e)
        if not isinstance(decimal_nm, Decimal):
            raise TypeError("Invalid value for distance, must be decimal")
        if decimal_nm < 0:
            raise ValueError(
                "Distance must be a value greater than or equal to zero")
        self._nautical_miles = nautical_miles

    def __str__(self):
        return "Distance: {} Nautical Miles".format(self._nautical_miles)

    @property
    def in_nautical_miles(self):
        return Decimal(self._nautical_miles)

    @property
    def in_km(self):
        return Decimal(copy(self._nautical_miles) * MULTIPLIER.get("KM"))

    @property
    def in_miles(self):
        return Decimal(copy(self._nautical_miles) * MULTIPLIER.get("MILE"))


class Speed(object):
    def __init__(self, speed_in_knots):
        decimal_speed = Decimal(speed_in_knots)

        if not isinstance(decimal_speed, Decimal):
            raise TypeError("Speed value invalid, must be of type Decimal")
        if speed_in_knots < 0:
            raise ValueError("Speed must be greater than or equal to 0.")
        self._speed_in_knots = decimal_speed

    def __str__(self):
        return "Speed: {} knots".format(self._speed_in_knots)

    @property
    def in_knots(self):
        return self._speed_in_knots

    @property
    def in_kmh(self):
        return Decimal(copy(self._speed_in_knots) * MULTIPLIER.get("KM"))

    @property
    def in_mph(self):
        return Decimal(copy(self._speed_in_knots) * MULTIPLIER.get("MILE"))


class Coordinate(object):
    def __init__(self, degrees, minutes, seconds, compass):
        VALID_COMPASS = ["N", "E", "S", "W"]
        if not isinstance(degrees, int) and isinstance(minutes, int)\
                and isinstance(seconds, int):
            raise TypeError("Degrees, minutes and seconds must be integers")
        if compass not in VALID_COMPASS:
            raise ValueError("Compass value must be: {}".format(VALID_COMPASS))
        self._degrees = degrees
        self._minutes = minutes
        self._seconds = seconds
        self._compass = compass

    def __str__(self):
        return "{}\u00b0 {}\' {}\" {}".format(
            self._degrees, self._minutes, self._seconds, self._compass
        )

    @classmethod
    def latitude_from_decimal(cls, decimal):
        d = int(decimal)
        m = int((Decimal(decimal) - Decimal(d)) * DEGREE_IN_MINUTES)
        s = int((Decimal(decimal) - Decimal(d) - Decimal(m) /
                 DEGREE_IN_MINUTES) * DEGREE_IN_SECONDS)
        if(d < 0):
            c = "S"
        else:
            c = "N"

        return cls(d, abs(m), abs(s), c)

    @classmethod
    def longitude_from_decimal(cls, decimal):
        d = int(decimal)
        m = int((Decimal(decimal) - Decimal(d)) * DEGREE_IN_MINUTES)
        s = int((Decimal(decimal) - Decimal(d) - Decimal(m) /
                 DEGREE_IN_MINUTES) * DEGREE_IN_SECONDS)
        if(d < 0):
            c = "W"
        else:
            c = "E"

        return cls(d, abs(m), abs(s), c)

    @property
    def degrees(self):
        return self._degrees

    @property
    def minutes(self):
        return self._minutes

    @property
    def seconds(self):
        return self._seconds

    @property
    def compass(self):
        return self._compass

    @property
    def waypoint(self):
        return (self._degrees, self._minutes, self._seconds, self._compass)

    @property
    def as_decimal(self):
        decimal = Decimal(
            abs(self._degrees) +
            (self._minutes / DEGREE_IN_MINUTES) +
            (self._seconds / DEGREE_IN_SECONDS)
        )

        if self._compass is "W" or self._compass is "S":
            return -decimal
        else:
            return decimal


class Waypoint(object):
    def __init__(self, latitude, longitude):
        if not isinstance(latitude, Coordinate) \
                and isinstance(longitude, Coordinate):
            raise TypeError("latitude and longitude must be Coordinates")
        self._latitude = latitude
        self._longitude = longitude

    def __str__(self):
        return "Latitude: {}, Longitude: {}".format(
            self._latitude, self._longitude
        )

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def waypoint(self):
        return {
            "latitude": self.latitude,
            "longitude": self._longitude
        }


class CompassBearing(object):
    def __init__(self, bearing):
        if not isinstance(bearing, int):
            raise TypeError("Bearing must be an integer.")

        if bearing < 0 or bearing > ONE_TURN:
            raise ValueError(
                "Bearing value must be between 0-{}.".format(ONE_TURN))
        self._bearing = bearing

    def __str__(self):
        return "Bearing: {}\u00b0".format(self._bearing)

    @property
    def bearing(self):
        return Decimal(self._bearing)


class SpeedDistanceTime(object):
    def __init__(self, speed=None, distance=None, time=None):
        self._speed = None
        self._distance = None
        self._time = None

        if speed is None and distance is None:
            raise ValueError(
                "Not enough information provided for \
                        SpeedDistanceTimeCalculation")

        if speed is None and time is None:
            raise ValueError(
                "Not enough information provided for \
                        SpeedDistanceTimeCalculation")

        if time is None and distance is None:
            raise ValueError(
                "Not enough information provided for \
                        SpeedDistanceTimeCalculation")

        if speed is None and distance is None and time is None:
            ValueError("No information provided for SpeedDistanceTime")

        if speed is not None and not isinstance(speed, Speed):
            raise TypeError("Speed must be of type Speed.")
        else:
            self._speed = speed

        if distance is not None and not isinstance(distance, Distance):
            raise TypeError("Distance must be of type Distance.")
        else:
            self._distance = distance

        if time is not None and not isinstance(time, Time):
            raise TypeError("Time must be of type Time.")
        else:
            self._time = time

        self._complete_values()

    def _complete_values(self):
        if self._speed and self._distance and not self._time:
            time = self._distance.in_nautical_miles / self._speed.in_knots
            self._time = Time(int(time * 60 * 60))
        if self._speed and self._time and not self._distance:
            distance = self._speed.in_knots * self._time.in_seconds
            self._distance = Distance(distance)
        if self._distance and self._time and not self._speed:
            speed = self._distance.in_nautical_miles / self._time.in_seconds
            self._speed = Speed(speed)

    @property
    def speed(self):
        return self._speed

    @property
    def distance(self):
        return self._distance

    @property
    def time(self):
        return self._time


class Leg(object):
    def __init__(self, sdt, start_waypoint, bearing=None):
        self._sdt = None
        self._start_waypoint = None

        if bearing is None:
            raise ValueError("Bearing Requires a value")

        if not isinstance(bearing, CompassBearing):
            raise TypeError("Bearing provided not of type Bearing.")
        self._bearing = bearing

        if not isinstance(start_waypoint, Waypoint):
            raise TypeError("Waypoint provided is not of type Waypoint.")
        self._start_waypoint = start_waypoint

        self._speed = sdt.speed
        self._time = sdt.time
        self._distance = sdt.distance
        self._end_waypoint = self._generate_end_waypoint()

    def __str__(self):
        return(
            "{}\n"
            "{}\n"
            "{}\n"
            "{}\n"
            "Start Waypoint: {}\n"
            "End Waypoint: {}\n".format(
                self._bearing,
                self._speed,
                self._distance,
                self._time,
                self._start_waypoint,
                self._end_waypoint
            )
        )

    @property
    def start_waypoint(self):
        return self._start_waypoint

    @property
    def end_waypoint(self):
        return self._end_waypoint

    @property
    def bearing(self):
        return self._bearing

    @property
    def speed(self):
        return self._speed

    @property
    def distance(self):
        return self._distance

    @property
    def time(self):
        return self._time

    @property
    def reverse_bearing(self):
        return CompassBearing(
            int(
                (self._bearing.bearing + HALF_TURN) % ONE_TURN
            )
        )

    def _generate_end_waypoint(self):
        end_latitude = self._generate_end_latitude(self._start_waypoint)
        end_longitude = self._generate_end_longitude(
            self._start_waypoint, end_latitude)

        end_wpt_lat = Coordinate.latitude_from_decimal(end_latitude)
        end_wpt_long = Coordinate.longitude_from_decimal(end_longitude)

        return Waypoint(end_wpt_lat, end_wpt_long)

    def _generate_end_latitude(self, start_waypoint):
        start_lat = self.start_waypoint.latitude.as_decimal
        angle_distance = self._distance.in_km/EARTH_RADIUS_IN_KM
        bearing_in_radians = radians(self._bearing.bearing)
        wpt = (
            Decimal(asin(
                (sin(radians(start_lat)) * cos(angle_distance)) +
                (cos(radians(start_lat)) * sin(angle_distance) *
                 cos(bearing_in_radians))
            )) / ONE_RADIAN
        )

        return wpt

    def _generate_end_longitude(self, start_waypoint, end_latitude):
        start_lat = self.start_waypoint.latitude.as_decimal
        start_long = self.start_waypoint.longitude.as_decimal
        angle_distance = self._distance.in_km/EARTH_RADIUS_IN_KM
        bearing_in_radians = radians(self._bearing.bearing)

        wpt = start_long + Decimal(atan2(
            (
                sin(bearing_in_radians) *
                sin(angle_distance) *
                cos(radians(start_lat))
            ),
            (
                cos(angle_distance) -
                sin(radians(start_lat)) * sin(radians(end_latitude))
            )
        )) / ONE_RADIAN

        normalised_longitude = (wpt + 540) % ONE_TURN - HALF_TURN
        return normalised_longitude


class Route(object):
    def __init__(self, legs=None):

        if not self._legs_is_valid(legs):
            raise TypeError("Legs list must contain only Leg objects.")
        self._legs = legs

    def _legs_is_valid(self, legs):
        for leg in legs:
            if not isinstance(leg, Leg):
                return False
        return True

    @property
    def legs(self):
        return self._legs

    def current_leg(self, current_leg_index):
        try:
            return self._legs[current_leg_index]
        except IndexError:
            print("There is no current leg.")
            raise

    def next_leg(self, current_leg_index):
        try:
            return self._legs[current_leg_index + 1]
        except IndexError:
            print("There is no next leg.")
            raise

    def previous_leg(self, current_leg_index):
        try:
            return self._legs[current_leg_index - 1]
        except IndexError:
            print("There is no previous leg")
            raise

    @property
    def number_of_legs(self):
        return len(self._legs)

    @property
    def start_waypoint(self):
        try:
            return self._legs[0].start_waypoint
        except IndexError:
            print("There is no starting waypoint.")
            raise

    @property
    def end_waypoint(self):
        try:
            return self._legs[-1].end_waypoint
        except IndexError:
            print("There is no end leg.")
            raise
