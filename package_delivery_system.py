# Susan Harrison - 000854062
# C950 OA
import csv
from datetime import timedelta

from package import Package
from location import Location
from hashtable import HashTable
from graph import Graph
from truck import Truck


class PackageDelivery(object):
    @staticmethod
    # this function will run the bulk of the package delivery program
    def run():
        graph = Graph()
        locations_hash = HashTable(20)
        packages_hash = HashTable(40)

        # opening and reading the location data from csv, then populating a hash table and graph with location data
        with open('DistanceNameData.csv') as csvfile:
            location_data = csv.reader(csvfile)

            # looping through location data -> O(n) complexity
            for data_row in location_data:
                location = Location(*data_row)

                # inserting location data into the hash table -> O(n) complexity
                locations_hash.insert(location.identifier, location)
                locations_hash.insert(location.address, location)

                # creating graph vertices -> O(n) complexity
                graph.add_vertex(location)

        all_packages = []
        high_priority = []
        low_priority = []

        with open('InputData.csv') as csvfile:
            package_data = csv.reader(csvfile)

            for data_row in package_data:
                package = Package(*(data_row+[locations_hash.find(data_row[1])]))

                all_packages.append(package)
                packages_hash.insert(package.identifier, package)

                # sorting through packages and divvying them up depending on priority levels
                # O(1) complexity
                if package.high_priority():
                    high_priority.append(package)
                else:
                    low_priority.append(package)

        # edge-creation between graph vertices
        with open('DistanceData.csv') as csvfile:
            distance_data = csv.reader(csvfile)

            # looping through csv file -> O(n^2) complexity
            for i, data_row in enumerate(distance_data):
                for j, data in enumerate(data_row):
                    if data != '':

                        # add a weighted edge to graph -> O(n) complexity
                        graph.add_weighted_edge(locations_hash.find(i),
                                                locations_hash.find(j),
                                                float(data))

        start_time = timedelta(hours=8)
        start_location = locations_hash.find(0)

        # limiting truck use to two trucks--truck 1 will make two trips since we have two drivers only
        trucks = [
            Truck(1, start_time, start_location),
            Truck(2, start_time, start_location)
        ]

        # list of leave times that are optimized for package distribution
        times_to_leave_hub = [
            timedelta(hours=8),
            timedelta(hours=9, minutes=5),
            timedelta(hours=10, minutes=20)
        ]

        # sort high and low priority lists based on distance from main hub -> O(n*log(n)) complexity
        high_priority = sorted(high_priority, key=graph.distance_to_deliver(start_location))
        low_priority = sorted(low_priority, key=graph.distance_to_deliver(start_location))

        count = 0
        truck_index = 0
        i = 0

        # while loop until packages are all delivered
        while count < len(all_packages):
            truck = trucks[truck_index]

            if i < len(times_to_leave_hub):
                leave_hub_at = times_to_leave_hub[i]
                truck.wait_at_hub(leave_hub_at)

            # filter priority list based on which packages a given truck can deliver -> O(n)
            filtered_high = [p for p in high_priority if truck.can_deliver(p)]

            # load up as many high priority packages as the truck can fit
            for package in filtered_high:
                # adding package to truck list -> O(1) complexity
                truck.add_package(package)
                count += 1

                if truck.is_full():
                    break

            # if truck isn't full after high priority packages, fill it up with nearby low priority packages
            if truck.is_full() is not True:
                filtered_low = [p for p in low_priority if truck.can_deliver(p)]
                for package in filtered_low:
                    truck.add_package(package)
                    count += 1

                    if truck.is_full():
                        break

            # using greedy algorithm, truck delivers packages in a route that is most optimized according to graph
            # O(n^2*log(n)) complexity
            truck.deliver_packages(graph, (len(all_packages) - count) > truck.max)
            i += 1
            truck_index = i % len(trucks)

        def total_distance(truck):
            return truck.total_distance

        return [sum(map(total_distance, trucks)), packages_hash, all_packages]
