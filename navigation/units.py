# -*- coding: utf-8 -*-

from copy import copy
from decimal import Decimal, Context, setcontext
from math import asin
from math import atan2
from math import cos
from math import pi
from math import pow
from math import sin
from math import sqrt
from math import radians


MULTIPLIER = {
    "KM": Decimal(1.852),
    "MILE": Decimal(1.15078)
}

DEGREE_IN_MINUTES = Decimal(60)
DEGREE_IN_SECONDS = Decimal(3600)
EARTH_RADIUS_IN_NAUTICAL_MILES = Decimal(3443.9184665)
EARTH_RADIUS_IN_KM = Decimal(6378.137)
HALF_TURN = Decimal(180)
ONE_TURN = Decimal(360)
ONE_RADIAN = Decimal((Decimal(pi) / HALF_TURN))

decimal_context = Context(prec=16)
setcontext(decimal_context)


class Time(object):
    """
    Represents a duration, defaults to seconds.
    """

    def __init__(self, seconds):
        """

        :param seconds: Seconds to instantiate Time object.
        :type seconds: int Non-zero integer.
        """
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
        """
        :return: The Time in seconds.
        :rtype: Decimal
        """

        return self._seconds

    @property
    def in_minutes(self):
        """
        :return: The Time in minutes.
        :rtype: Decimal
        """
        return Decimal(self._seconds / 60)

    @property
    def in_hours(self):
        """
        :return: The Time in hours.
        :rtype: Decimal
        """
        return Decimal((self._seconds / 60) / 60)


class Distance(object):
    """
    Represents a distance, defaults to nautical miles.
    """

    def __init__(self, nautical_miles):
        """
        :param nautical_miles: The distance in Nautical Miles.
        """
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
        """
        :return: The Distance in Nautical Miles.
        :rtype: Decimal
        """
        return Decimal(self._nautical_miles)

    @property
    def in_km(self):
        """
        :return: The Distance in Kilometers.
        :rtype: Decimal
        """
        return Decimal(copy(self._nautical_miles) * MULTIPLIER.get("KM"))

    @property
    def in_miles(self):
        """
        :return: The Distance in Statute Miles.
        :rtype: Decimal
        """
        return Decimal(copy(self._nautical_miles) * MULTIPLIER.get("MILE"))


class Speed(object):
    """
    Represents speed of travel, defaults to knots.
    """

    def __init__(self, speed_in_knots):
        """
        :param speed_in_knots: The speed to travel in Knots.
        """
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
        """
        :return: The speed in nautical miles per hour.
        :rtype: Decimal
        """
        return self._speed_in_knots

    @property
    def in_kmh(self):
        """
        :return: The speed in kilometers per hour.
        :rtype: Decimal
        """
        return Decimal(copy(self._speed_in_knots) * MULTIPLIER.get("KM"))

    @property
    def in_mph(self):
        """
        :return: The speed in miles per hour.
        :rtype: Decimal
        """
        return Decimal(copy(self._speed_in_knots) * MULTIPLIER.get("MILE"))


class Coordinate(object):
    """
    Represents a partial point on the surface of the earth, such as latitude or longitude.
    """

    def __init__(self, degrees, minutes, seconds, compass):
        """
        :param degrees: The arc degree of the Coordinate.
        :type degrees: int

        :param minutes: The arc minutes of the Coordinate
        :type minutes: int

        :param seconds: The arc seconds of the Coordinate
        :type seconds: int

        :param compass: Give direction for latitude/longitude. Allowed values N, S, E, W.
        :type compass: str
        """
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
        """
        :param decimal: The decimal representation of latitude. E.g. 56.12345.
        :return: The Coordinate in Degrees Minutes Seconds format.
        """
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
        """
        :param decimal: The decimal representation of latitude. E.g. -2.12345.
        :return: The Coordinate in Degrees Minutes Seconds format.
        """
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
        """
        :return: The Degrees componenet of the Coordinate.
        :rtype: Decimal
        """
        return self._degrees

    @property
    def minutes(self):
        """
        :return: The Minutes componenet of the Coordinate.
        :rtype: Decimal
        """
        return self._minutes

    @property
    def seconds(self):
        """
        :return: The Seconds componenet of the Coordinate.
        :rtype: Decimal
        """
        return self._seconds

    @property
    def compass(self):
        """
        :return: The Compass direction componenet of the Coordinate. I.e. N/S E/W.
        :rtype: str
        """
        return self._compass

    @property
    def waypoint(self):
        """
        :return: The waypoint in Degrees, Minutes, Seconds, Compass format.
        :rtype: tuple
        """
        return (self._degrees, self._minutes, self._seconds, self._compass)

    @property
    def as_decimal(self):
        """
        :return: The Coordinate in decimal format. E.g. -2.6789.
        :rtype: Decimal
        """
        decimal = Decimal(
            abs(self._degrees) +
            (self._minutes / DEGREE_IN_MINUTES) +
            (self._seconds / DEGREE_IN_SECONDS)
        )

        if self._compass is "W" or self._compass is "S":
            return -decimal
        else:
            return decimal

    @property
    def as_decimal_seconds(self):
        """
        :return: The Coordinate in Degrees, Minutes, Decimal-Seconds format.
        :rtype: tuple
        """
        return (self._degrees, self._minutes, (self._seconds/60), self._compass)


class Waypoint(object):
    """
    Represents a single point on the surface of the earth. Consists of two Coordinates.
    """

    def __init__(self, latitude, longitude):
        """
        :param latitude: The latitude of the Waypoint.
        :type latitude: Coordinate

        :param longitude: The longitude of the Waypoint.
        :type longitude: Coordinate
        """
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
        """
        :return: The latitude Coordinate.
        :rtype: Coordinate
        """
        return self._latitude

    @property
    def longitude(self):
        """
        :return: The longitude Coordinate.
        :rtype: Coordinate
        """
        return self._longitude

    @property
    def waypoint(self):
        """
        :return: The Waypoint containing the latitude and longitude Coordinates.
        :rtype: dict
        """
        return {
            "latitude": self.latitude,
            "longitude": self._longitude
        }

    @classmethod
    def distance_between(self, wpt_a, wpt_b):
        """
        :param wpt_a: The Waypoint to measure from.
        :type wpt_a: Waypoint

        :param wpt_b: The Waypoint to measure to.
        :type wpt_b: Waypoint

        :return: The distance in Nautical Miles between Waypoint A and Waypoint B.
        :rtype: Decimal
        """
        a = Decimal(
            pow(sin((radians(wpt_a.latitude.as_decimal) -
                     radians(wpt_b.latitude.as_decimal)) / 2), 2) +
            cos(radians(wpt_a.latitude.as_decimal)) *
            cos(radians(wpt_b.latitude.as_decimal)) *
            pow(sin((radians(wpt_a.longitude.as_decimal) -
                     radians(wpt_b.longitude.as_decimal))/2), 2)
        )
        c = Decimal(2 * atan2(sqrt(a), sqrt(1-a)))
        return EARTH_RADIUS_IN_NAUTICAL_MILES * c


class CompassBearing(object):
    """
    Represents a heading on a compass rose.
    """

    def __init__(self, bearing):
        """
        :param bearing: The compass bearing to set. Must be between 0-360.
        :type bearing: int
        """
        if not isinstance(bearing, int) or isinstance(bearing, Decimal):
            raise TypeError("Bearing must be an integer.")

        if bearing < 0 or bearing > ONE_TURN:
            raise ValueError(
                "Bearing value must be between 0-{}.".format(ONE_TURN))
        self._bearing = bearing

    def __str__(self):
        return "Bearing: {}\u00b0".format(self._bearing)

    @property
    def bearing(self):
        """
        :return: The Compass Bearing.
        :rtype: Decimal
        """
        return Decimal(self._bearing)


class SpeedDistanceTime(object):
    """
    Given partial Speed, Distance or Time information this object completes the
    missing values to aid navigational calculations.
    """

    def __init__(self, speed=None, distance=None, time=None):
        """
        Must have two of the three parameters: Speed, Distance or Time.
        The missing parameter is calculated.

        :param speed: The Speed travelled at (optional)
        :type speed: Speed
        :param distance: The Distance to travel (optional)
        :type distance: Distance
        :param time: The time to travel (optional)
        :type time: Time
        """
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
        """
        :return: The speed to travel at.
        :rtype: Speed
        """
        return self._speed

    @property
    def distance(self):
        """
        :return: The distance to travel.
        :rtype: Distance
        """
        return self._distance

    @property
    def time(self):
        """
        :return: The time to travel for.
        :rtype: Time
        """
        return self._time


class Leg(object):
    """
    Represents a course to travel. Has a single starting point and a single end point.
    """

    def __init__(self, sdt, start_waypoint, bearing=None):
        """
        :param sdt: The SpeedDistanceTime object for the Leg.
        :type sdt: SpeedDistanceTime

        :param start_waypoint: The starting Waypoint for the Leg.
        :type start_waypoint: Waypoint

        :param bearing: The bearing (direction) for the Leg (optional).
        :type bearing: CompassBearing
        """
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
        """
        :return: The starting Waypoint.
        :rtype: Waypoint
        """
        return self._start_waypoint

    @property
    def end_waypoint(self):
        """
        :return: The end Waypoint.
        :rtype: Waypoint
        """
        return self._end_waypoint

    @property
    def bearing(self):
        """
        :return: The bearing of the Leg.
        :rtype: CompassBearing
        """
        return self._bearing

    @property
    def speed(self):
        """
        :return: The speed of the Leg.
        :rtype: Speed
        """
        return self._speed

    @property
    def distance(self):
        """
        :return: The distance of the Leg.
        :rtype: Distance
        """
        return self._distance

    @property
    def time(self):
        """
        :return: The time of the Leg.
        :rtype: Time
        """
        return self._time

    @property
    def reverse_bearing(self):
        """
        :return: The reciprocal bearing of the Leg.
        :rtype: CompassBearing
        """
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
    """
    Represents a series of legs that join between their start and end points.
    """

    def __init__(self, legs=None):
        """
        :param legs: A list of Legs to form the Route.
        :type legs: list
        """
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
        """
        :return: The list of Legs in the Route.
        :rtype: list
        """
        return self._legs

    def current_leg(self, current_leg_index):
        """
        :param current_leg_index: The position in the list of the Leg.
        :type current_leg_index: int
        :return: The leg at position current_leg_index.
        :rtype: Leg
        """
        try:
            return self._legs[current_leg_index]
        except IndexError:
            print("There is no current leg.")
            raise

    def next_leg(self, current_leg_index):
        """
        :param current_leg_index: The position in the list of the Leg.
        :type current_leg_index: int
        :return: The next Leg after the Leg at current_leg_index.
        :rtype: Leg
        """
        try:
            return self._legs[current_leg_index + 1]
        except IndexError:
            print("There is no next leg.")
            raise

    def previous_leg(self, current_leg_index):
        """
        :param current_leg_index: The position in the list of the Leg.
        :type current_leg_index: int
        :return: The Leg preceeding the Leg at current_leg_index.
        :rtype: Leg
        """
        try:
            return self._legs[current_leg_index - 1]
        except IndexError:
            print("There is no previous leg")
            raise

    @property
    def number_of_legs(self):
        """
        :return: The number of Legs in the Route.
        :rtype: int
        """
        return len(self._legs)

    @property
    def start_waypoint(self):
        """
        :return: The starting Waypoint of the first Leg.
        :rtype: Waypoint
        """
        try:
            return self._legs[0].start_waypoint
        except IndexError:
            print("There is no starting waypoint.")
            raise

    @property
    def end_waypoint(self):
        """
        :return: The end Waypoint of the final Leg.
        :rtype: Waypoint
        """
        try:
            return self._legs[-1].end_waypoint
        except IndexError:
            print("There is no end leg.")
            raise
