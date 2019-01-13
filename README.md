[![CircleCI](https://circleci.com/gh/ngfgrant/navigation/tree/master.svg?style=svg&circle-token=6bba4588eeb6ed5ebff6839646ce62293a1001d8)](https://circleci.com/gh/ngfgrant/navigation/tree/master) [![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=coverage)](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=coverage) [![Sonarcloud
Status](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=ncloc)](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=ncloc) [![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=sqale_rating)](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=sqale_rating)
[![Sonarcloud
Status](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=reliability_rating)](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=reliability_rating)
[![Sonarcloud
Status](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=security_rating)](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=security_rating)
[![Sonarcloud
Status](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=sqale_index)](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=sqale_index)
[![Sonarcloud
Status](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=vulnerabilities)](https://sonarcloud.io/api/project_badges/measure?project=ngfgrant_navigation&metric=vulnerabilities)

# Navigation

This module provides units of measurement and associated functions required for
navigating.

# Applications

There are many use-cases for this module including the original reason for
developing it - Search and Rescue. It's also useful if you are developing a GPS
application, or anything that needs to work with Latitude, Longitude, Routes
and Waypoints.

# Units

The following navigation units are provided:

- Speed

- Distance

- Time

- CompassBearing

- Coordinate (Latitude/Longitude)

- Waypoint

- Leg

- Route

# Install

```shell
$pip install pynavigation
```

# Example

```python
from pynavigation.units import Speed
from pynavigation.units import Distance
from pynavigation.units import SpeedDistanceTime
from pynavigation.units import CompassBearing
from pynavigation.units import Coordinate
from pynavigation.units import Waypoint

# Basic Units
speed = Speed(10)
distance = Distance(100)
sdt = SpeedDistanceTime(speed=speed, distance=distance)
bearing = CompassBearing(83)

# Positioning Units
latitude = Coordinate(56, 12, 34, "N")
longitude = Coordinate(2, 54, 19, "W")
waypoint = Waypoint(latitude, longitude)

# Routing Units
leg = Leg(sdt, waypoint, bearing)
legs = [leg]

route = Route(legs)

# Example methods

knots = speed.in_knots
time = sdt.time
latitude_in_decimal_format = latitude.as_decimal
longitude_from_decimal = Coordinate.from_decimal(-2.76543)

end_wpt = leg.end_waypoint
number_of_legs = route.number_of_legs
starting_point = route.start_waypoint


for leg in range(number_of_legs):
    current_leg = route.current_leg(leg)
    next_leg = route.next_leg(leg)
    previous_leg = route.previous_leg(leg)
```

# Contributing

See the [Contributing Guide](CONTRIBUTING.md)
