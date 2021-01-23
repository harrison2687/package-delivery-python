# Susan Harrison - 000854062
# C950 OA
from datetime import timedelta


class Truck(object):
    # putting in some constraints according to the OA instructions
    # these numbers could be changed if the parameters of the delivery program change
    MAX_PACKAGES = 16
    DRIVING_SPEED_IN_MPH = 18.0
    SECONDS_PER_HOUR = 3600.0

    def __init__(self, identifier, start_time, start_location):
        self.identifier = identifier
        self.current_time = start_time
        self.start_location = start_location
        self.total_distance = 0
        self.max = self.MAX_PACKAGES
        self.packages = []
        self.locations = set()

    # adding packages to package list and the location to a locations set -> O(n) complexity
    def add_package(self, package):
        if len(self.packages) < self.max:
            self.packages.append(package)
            self.locations.add(package.destination)

            package.on_truck = True
            package.left_hub_at = self.current_time

    # helper method to determine if truck is full
    def is_full(self):
        return len(self.packages) == self.max

    def wait_at_hub(self, timestamp):
        self.current_time = timestamp

    # helper method to determine if a truck can deliver a package
    def can_deliver(self, package):
        return not package.on_truck and self.identifier in package.truck_availability \
               and self.current_time >= package.ready_at

    # using Dijkstra's Greedy Algorithm that sorts the truck's package list by distance according to a truck's
    # current location.  when the truck travels and drops off a package, it re-sorts the list based on
    # the next location, and repeats this until all packages have been delivered.
    #
    # time complexity of the algorithm: O(n^2*log(n))
    def deliver_packages(self, city_map, return_to_hub=True):
        current_location = self.start_location
        locations = list(self.locations)

        while self.packages:
            locations = sorted(locations, key=city_map.distance_from(current_location))
            closest_location = locations.pop(0)

            distance = city_map.find_distance(current_location, closest_location)
            time_to_deliver = self._time_to_travel(distance)
            delivered_at = self.current_time + timedelta(seconds=time_to_deliver)

            packages_at_location = [p for p in self.packages if p.destination.identifier == closest_location.identifier]
            for package in packages_at_location:
                package.delivered_at = delivered_at

                self.packages.remove(package)

            current_location = closest_location
            self.total_distance += distance
            self.current_time = delivered_at

        if return_to_hub:
            distance = city_map.find_distance(current_location, self.start_location)
            time_to_return = self._time_to_travel(distance)

            self.current_time = self.current_time + timedelta(seconds=time_to_return)
            self.total_distance += distance

            self.locations = set()

    # calculating how long it would travel
    def _time_to_travel(self, distance):
        return (distance / self.DRIVING_SPEED_IN_MPH) * self.SECONDS_PER_HOUR
