import googlemaps
 
 
API_KEY = "AIzaSyB9sbMLbqXku6vRNwk3fiUkRN0G42OM6N0"
client = googlemaps.Client(API_KEY)
 
class Point:
    def __init__(self, id, name, coordinates):
        self.id = id
        self.name = name
        self.coordinates = coordinates

class Road:
    def __init__(self, id, origin_id, destination_id, distance):
        self.id = id
        self.origin_id = origin_id 
        self.destination_id = destination_id
        self.distance = distance
        

p1 = Point(1, "lublin", "51.2465, 22.5684")
p2 = Point(2, "Warszawa", "52.2297, 21.0122")
p3 = Point(3, "Lodz", "51.7833, 19.4667")
p4 = Point(4, "Chelm", "51.0835, 23.2817" )
p5 = Point(5, "Krasnystaw", "39.5426, 116.2350")

points = {p1, p2, p3, p4, p5}

roads = []
for p in points:
    for destination in points:
        if p != destination:
            directions_result = client.directions(origin= p.coordinates, 
                                                        destination=p.coordinates, 
                                                        mode = "driving", 
                                                        avoid="ferries")

            distance =directions_result[0]['legs'][0]['distance']
            print("from", p.name, "to", destination.name, distance['value'])
            roads.append(Road(1, p.id, destination.id, distance['value']))

def first(points):
    return next(iter(points))

def distance(a, x, roads):
    for r in roads:
        if r.origin_id == a.id and r.destination_id == x.id:
            return r.distance

def nearest_neighbour(a, points):
    return min(points, key=lambda x: distance(a,x, roads))

def nn_tour():
    start = first(points)
    tour = [start]
    unvisited = points - {start}
    while unvisited: 
        c = nearest_neighbour(tour[-1], unvisited)
        tour.append(c)
        unvisited.remove(0)
    return tour

nn = nn_tour(points)
for n in nn:
    print(n.name)
# classy na bazy danychx
 
# waw = "52.2505562,20.9781065"
# lbn = "51.2426387,22.5554689"
 
# directions_result = client.directions(origin=waw,
#                                       destination=lbn,
#                                       mode="driving",
#                                       avoid="ferries")
 
 
print(directions_result[0]['legs'][0]['distance'])
 