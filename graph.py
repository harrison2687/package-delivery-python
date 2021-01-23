# Susan Harrison - 000854062
# C950 OA
from hashtable import HashTable
from vertex import Vertex
from edge import Edge


class Graph(object):
    def __init__(self):
        self.vertices = HashTable(20)

    # creates a vertex from a location and adds it to the vertex hash table -> O(n) complexity
    def add_vertex(self, location):
        self.vertices.insert(location.identifier, Vertex(location))

    # creates a bi-directional weighted edge between two vertices -> O(n) complexity
    def add_weighted_edge(self, origin, destination, weight):
        self.vertices.find(origin.identifier).add_edge(Edge(destination, weight))
        self.vertices.find(destination.identifier).add_edge(Edge(origin, weight))

    # finds the vertex matching the location -> O(n) complexity
    def find_vertex(self, location):
        return self.vertices.find(location.identifier)

    # finds the distance between two vertices -> O(n) complexity
    def find_distance(self, origin, target):
        return self.vertices.find(origin.identifier).distance_to(target)

    # finds the distance between a location and package destination
    # used for priority list sorting
    def distance_to_deliver(self, location):
        def distance_to(package):
            return self.vertices.find(location.identifier).distance_to(package.destination)

        return distance_to

    # sets up the next closest location the truck should drive to
    def distance_from(self, origin):
        def distance_to(destination):
            return self.vertices.find(origin.identifier).distance_to(destination)

        return distance_to
