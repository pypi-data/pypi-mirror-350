from math import atan2, cos, radians, sin, sqrt

class HaversineUtil:

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
            """
            Calculate the distance in kilometers between two GPS coordinates using the Haversine formula.

            Parameters:
            lat1 (float): Latitude of the first point.
            lon1 (float): Longitude of the first point.
            lat2 (float): Latitude of the second point.
            lon2 (float): Longitude of the second point.

            Returns:
            float: Distance in kilometers between the two points.
            """
            R = 6371.0  # Radius of the Earth in kilometers

            lat1_rad = radians(lat1)
            lon1_rad = radians(lon1)
            lat2_rad = radians(lat2)
            lon2_rad = radians(lon2)

            dlon = lon2_rad - lon1_rad
            dlat = lat2_rad - lat1_rad

            a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c

            return round(distance, 2)