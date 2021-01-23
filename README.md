
# Package Delivery Application

This repo contains files for a package delivery console that provides the following options:

1. Look up individual package information
2. Look up the delivery status of all packages within a given time
3. Look up the total distance of the trucks traveled
4. Clear the console screen (to keep things tidy)
5. Exit the program

## Instructions for running

This program can be run through a terminal after the repo is downloaded by running the following command (note that python 3 should be installed):

```python
python main.py
```

## Algorithm Overview

This was primarily used as a study in data structures and algorithms.  Dijkstra's algorithm was used and combined with a graph data structure to find the shortest distance from point to point within a graph.  A priority algorithm was also combined with a list data structure to distribute the packages between the two required trucks in this scenario.  High priority (earlier delivery requirements) are sorted into the first truck and regular priority items are sorted into the second truck.
