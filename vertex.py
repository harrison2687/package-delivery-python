# vertex for graph.py
from hashtable import HashTable


class Vertex(object):
    def __init__(self, location):
        self.edges = HashTable()
        self.value = location

    # add edge to HashTable -> O(n) complexity
    def add_edge(self, edge):
        self.edges.insert(edge.identifier, edge)

    # find edge by id -> O(n) complexity
    def find_edge(self, edge_id):
        return self.edges.find(edge_id)

    # find distance to neighboring vertex -> O(n) complexity
    def distance_to(self, location):
        return self.edges.find(location.identifier).weight
