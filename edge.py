# Susan Harrison - 000854062
# C950 OA
# edge for graph.py
class Edge(object):
    def __init__(self, location, weight=0.0):
        self.location = location
        self.identifier = location.identifier
        self.weight = weight
