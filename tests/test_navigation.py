import unittest

from decimal import Decimal

from navigation.units import Time
from navigation.units import Distance
from navigation.units import Speed
from navigation.units import Coordinate
from navigation.units import Waypoint
from navigation.units import CompassBearing
from navigation.units import SpeedDistanceTime
from navigation.units import Leg
from navigation.units import Route


class TestTime(unittest.TestCase):

    def test_time_is_integer(self):
        time = Time(200)
        self.assertIsInstance(time.in_seconds, int)

    def test_time_fails_to_instantiate_with_float(self):
        with self.assertRaises(TypeError):
            Time(20.01)

    def test_time_fails_to_instantiate_with_negative_value(self):
        with self.assertRaises(ValueError):
            Time(-20)

    def test_time_fails_to_instantiate_with_zero_value(self):
        with self.assertRaises(ValueError):
            Time(0)

    def test_time_in_minutes_is_correct(self):
        time = Time(60)
        self.assertEqual(time.in_minutes, 1)

    def test_time_in_hours_is_correct(self):
        time = Time(5400)  # 1.5 hours
        self.assertEqual(time.in_hours, 1.5)


class TestDistance(unittest.TestCase):
    def test_distance_instantiates_with_float(self):
        distance = Distance(19.2345)
        self.assertIsInstance(distance.in_nautical_miles, Decimal)
        self.assertEqual(distance.in_nautical_miles, 19.2345)

    def test_distance_instantiates_with_integer(self):
        distance = Distance(10)
        self.assertIsInstance(distance, Distance)
        self.assertEqual(distance.in_nautical_miles, 10)

    def test_distance_fails_to_instantiate_with_negative_number(self):
        with self.assertRaises(ValueError):
            Distance(-2.0)

    def test_distance_instantiates_with_zero_value(self):
        distance = Distance(0)
        self.assertIsInstance(distance, Distance)
        self.assertEqual(distance.in_nautical_miles, 0)

    def test_distance_instantiates_with_less_than_one_greater_than_0(self):
        distance = Distance(0.2)
        self.assertIsInstance(distance, Distance)
        self.assertEqual(distance.in_nautical_miles, 0.2)

    def test_distance_converts_to_km(self):
        distance = Distance(10)
        self.assertAlmostEqual(distance.in_km, Decimal(18.52))

    def test_distance_converts_to_miles(self):
        distance = Distance(20)
        self.assertAlmostEqual(distance.in_miles, Decimal(23.0156))

    def test_distance_instantiates_with_string_number_value(self):
        distance = Distance('10.60')
        self.assertIsInstance(distance, Distance)


class TestSpeed(unittest.TestCase):
    def test_speed_instantiates_with_float(self):
        speed = Speed(10.2345)
        self.assertIsInstance(speed, Speed)
        self.assertEqual(speed.in_knots, 10.2345)

    def test_speed_instantiates_with_int(self):
        speed = Speed(10)
        self.assertIsInstance(speed, Speed)
        self.assertEqual(speed.in_knots, 10)

    def test_speed_instantiates_with_zero_value(self):
        speed = Speed(0)
        self.assertIsInstance(speed, Speed)
        self.assertEqual(speed.in_knots, 0)

    def test_speed_in_knots_converts_to_kph(self):
        speed = Speed(10)
        self.assertEqual(speed.in_kmh, Decimal(
            18.52).quantize(Decimal('10.13')))

    def test_speed_in_knots_converts_to_mph(self):
        speed = Speed(20)
        self.assertEqual(speed.in_mph, Decimal(
            23.0156).quantize(Decimal('12.3456')))


class TestCoordinate(unittest.TestCase):
    def test_N_is_a_valid_compass_value(self):
        coordinate = Coordinate(56, 42, 10, "N")
        self.assertIsInstance(coordinate, Coordinate)
        self.assertEqual(coordinate.compass, "N")

    def test_B_is_not_a_valid_compass_value(self):
        with self.assertRaises(ValueError):
            Coordinate(56, 42, 10, "B")

    def test_coordinate_initailises_with_int_values(self):
        coordinate = Coordinate(56, 42, 10, "N")
        self.assertIsInstance(coordinate, Coordinate)
        self.assertIsInstance(coordinate.degrees, int)
        self.assertIsInstance(coordinate.minutes, int)
        self.assertIsInstance(coordinate.seconds, int)
        self.assertIsInstance(coordinate.compass, str)

    def test_latitude_is_generated_from_decimal_latitude(self):
        decimal_lat = 56.123456
        coordinate = Coordinate.latitude_from_decimal(decimal_lat)
        self.assertEqual(coordinate.waypoint, (56, 7, 24, "N"))

    def test_longitude_is_generated_from_decimal_longitude(self):
        decimal_long = 2.678999
        coordinate = Coordinate.longitude_from_decimal(decimal_long)
        self.assertEqual(coordinate.waypoint, (2, 40, 44, "E"))

    def test_waypoint_tuple_is_returned(self):
        coordinate = Coordinate(56, 42, 10, "N")
        self.assertIsInstance(coordinate.waypoint, tuple)

    def test_as_decimal_converts_from_north_lat(self):
        coordinate = Coordinate(56, 42, 10, "N")
        self.assertAlmostEqual(coordinate.as_decimal,
                               Decimal(56.70277777777778))

    def test_as_decimal_converts_from_south_lat(self):
        coordinate = Coordinate(56, 42, 10, "S")
        self.assertAlmostEqual(coordinate.as_decimal,
                               Decimal(-56.70277777777778))

    def test_as_decimal_converts_from_west_long(self):
        coordinate = Coordinate(2, 5, 19, "W")
        self.assertAlmostEqual(coordinate.as_decimal,
                               Decimal(-2.088611111111111))

    def test_as_decimal_converts_from_each_long(self):
        coordinate = Coordinate(10, 45, 19, "W")
        self.assertAlmostEqual(coordinate.as_decimal,
                               Decimal(-10.755277777777778))


class TestWaypoint(unittest.TestCase):
    def test_waypoint_initailises_with_coordinates(self):
        latitude = Coordinate(56, 42, 10, "S")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        self.assertIsInstance(waypoint, Waypoint)
        self.assertEqual(waypoint.latitude, latitude)
        self.assertEqual(waypoint.longitude, longitude)

    def test_waypoint_fails_to_initalise_with_incorrect_params(self):
        with self.assertRaises(TypeError):
            Waypoint(10.5, Coordinate(2, 5, 19, "W"))

    def test_waypoint_waypoint_is_coordinate_dict(self):
        latitude = Coordinate(56, 42, 10, "S")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        self.assertIsInstance(waypoint.waypoint, dict)
        self.assertEqual(waypoint.waypoint, {
                         "latitude": latitude, "longitude": longitude})

    def test_distance_between_two_waypoint(self):
        latitude_a = Coordinate(56, 42, 10, "S")
        longitude_a = Coordinate(2, 5, 19, "W")
        latitude_b = Coordinate(56, 50, 10, "S")
        longitude_b = Coordinate(2, 6, 19, "W")

        wpt_a = Waypoint(latitude_a, longitude_a)
        wpt_b = Waypoint(latitude_b, longitude_b)

        distance = Waypoint.distance_between(wpt_a, wpt_b)
        self.assertAlmostEqual(distance.quantize(Decimal('.001')), Decimal(8.033))


class TestCompassBearing(unittest.TestCase):
    def test_compass_bearing_initailises_with_int(self):
        bearing = CompassBearing(12)
        self.assertIsInstance(bearing, CompassBearing)
        self.assertEqual(bearing.bearing, 12)

    def test_compass_bearing_can_not_be_negative_value(self):
        with self.assertRaises(ValueError):
            CompassBearing(-1)

    def test_compass_bearing_can_not_be_greater_than_360(self):
        with self.assertRaises(ValueError):
            CompassBearing(361)

    def test_compass_bearing_can_be_0(self):
        bearing = CompassBearing(0)
        self.assertIsInstance(bearing, CompassBearing)
        self.assertEqual(bearing.bearing, 0)


class TestSpeedDistanceTime(unittest.TestCase):
    def test_sdt_raises_error_if_less_two_values(self):
        speed = Speed(10)
        with self.assertRaises(ValueError):
            SpeedDistanceTime(speed=speed)

    def test_sdt_intailises_with_speed_and_distance(self):
        speed = Speed(10)
        distance = Distance(20)
        sdt = SpeedDistanceTime(speed=speed, distance=distance)
        self.assertIsInstance(sdt, SpeedDistanceTime)
        self.assertEqual(sdt.time.in_seconds, 7200)

    def test_sdt_initailises_with_speed_and_time(self):
        speed = Speed(10)
        time = Time(20)
        sdt = SpeedDistanceTime(speed=speed, time=time)
        self.assertIsInstance(sdt, SpeedDistanceTime)
        self.assertEqual(sdt.distance.in_nautical_miles, 200)

    def test_sdt_initailises_with_distance_and_time(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        self.assertIsInstance(sdt, SpeedDistanceTime)
        self.assertEqual(sdt.speed.in_knots, 0.5)


class TestLeg(unittest.TestCase):
    def test_leg_fails_to_initailise_without_bearing(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "S")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)

        with self.assertRaises(ValueError):
            Leg(sdt, waypoint)

    def test_leg_fails_to_initailise_without_valid_waypoint(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        waypoint = (10.123456, 2.324567)
        bearing = CompassBearing(190)
        with self.assertRaises(TypeError):
            Leg(sdt, waypoint, bearing)

    def test_leg_fails_to_initailise_without_valid_bearing(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        waypoint = (10.123456, 2.324567)
        bearing = 190
        with self.assertRaises(TypeError):
            Leg(sdt, waypoint, bearing)

    def test_end_waypoint_is_generate_correctly(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)

        expected_end_wpt = Waypoint(
            Coordinate(56, 32, 20, "N"),
            Coordinate(2, 8, 27, "W")
        )
        leg = Leg(sdt, waypoint, bearing)

        self.assertIsInstance(leg.end_waypoint, Waypoint)
        self.assertAlmostEqual(leg.end_waypoint.latitude.as_decimal,
                               expected_end_wpt.latitude.as_decimal)
        self.assertAlmostEqual(leg.end_waypoint.longitude.as_decimal,
                               expected_end_wpt.longitude.as_decimal)

    def test_reverse_bearing_is_correct(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        reverse_bearing = CompassBearing(10)
        leg = Leg(sdt, waypoint, bearing)

        self.assertIsInstance(leg.end_waypoint, Waypoint)
        self.assertEqual(leg.reverse_bearing.bearing, reverse_bearing.bearing)


class TestRoute(unittest.TestCase):
    def test_route_is_intialised_with_legs(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        legs = [leg]
        route = Route(legs)

        self.assertIsInstance(route, Route)

    def test_route_fails_to_instantiate_with_no_legs(self):
        legs = None
        with self.assertRaises(TypeError):
            Route(legs)

    def test_route_fails_to_instantiate_with_invalid_legs(self):
        legs = [1, 2, 3]
        with self.assertRaises(TypeError):
            Route(legs)

    def test_route_returns_legs(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        legs = [leg]
        route = Route(legs)

        self.assertIsInstance(route, Route)
        self.assertEqual(route.legs, legs)

    def test_route_returns_correct_number_of_legs(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        legs = [leg]
        route = Route(legs)

        self.assertIsInstance(route, Route)
        self.assertEqual(route.number_of_legs, 1)

    def test_get_current_leg_of_route(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        legs = [leg]
        route = Route(legs)

        self.assertIsInstance(route, Route)
        self.assertEqual(route.current_leg(0), leg)

    def test_get_current_leg_bad_index(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        legs = [leg]
        route = Route(legs)

        self.assertIsInstance(route, Route)
        with self.assertRaises(IndexError):
            route.current_leg(1)

    def test_next_leg_of_route(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        leg2 = Leg(sdt, waypoint, bearing)
        legs = [leg, leg2]
        route = Route(legs)

        self.assertIsInstance(route, Route)
        self.assertEqual(route.next_leg(0), leg2)

    def test_next_leg_of_route_does_not_exist(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        legs = [leg]
        route = Route(legs)

        self.assertIsInstance(route, Route)
        with self.assertRaises(IndexError):
            route.next_leg(0)

    def test_previous_leg(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        leg2 = Leg(sdt, waypoint, bearing)
        legs = [leg, leg2]
        route = Route(legs)

        self.assertIsInstance(route, Route)
        self.assertEqual(route.previous_leg(1), leg)

    def test_previous_leg_of_route_does_not_exist(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        legs = [leg]
        route = Route(legs)

        self.assertIsInstance(route, Route)
        with self.assertRaises(IndexError):
            route.previous_leg(2)

    def test_starting_waypoint_exists(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        legs = [leg]
        route = Route(legs)

        self.assertIsInstance(route, Route)
        self.assertEqual(route.start_waypoint, waypoint)

    def test_end_waypoint_exists(self):
        distance = Distance(10)
        time = Time(20)
        sdt = SpeedDistanceTime(distance=distance, time=time)
        latitude = Coordinate(56, 42, 10, "N")
        longitude = Coordinate(2, 5, 19, "W")
        waypoint = Waypoint(latitude, longitude)
        waypoint2 = Waypoint(latitude, longitude)
        bearing = CompassBearing(190)
        leg = Leg(sdt, waypoint, bearing)
        leg2 = Leg(sdt, waypoint2, bearing)
        legs = [leg, leg2]
        route = Route(legs)

        self.assertIsInstance(route.end_waypoint, Waypoint)
        self.assertEqual(str(route.end_waypoint), str(leg2.end_waypoint))


if __name__ == '__main__':
    unittest.main()
