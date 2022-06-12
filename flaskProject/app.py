from datetime import datetime
from unicodedata import name
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import googlemaps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
API_KEY = "AIzaSyB9sbMLbqXku6vRNwk3fiUkRN0G42OM6N0"
client = googlemaps.Client(API_KEY)

class Klasa():
    def __init__(self, id, name, coordinates):
            self.id = id
            self.name = name
            self.coordinates = coordinates

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    coordinates = db.Column(db.String, nullable=False)

class Road(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    distance = db.Column(db.String, nullable=False)

db.create_all()

# p1 = Point(1, "lublin", "51.2465, 22.5684")
# p2 = Point(2, "Warszawa", "52.2297, 21.0122")
# p3 = Point(3, "Lodz", "51.7833, 19.4667")
# p4 = Point(4, "Chelm", "51.0835, 23.2817" )
# p5 = Point(5, "Krasnystaw", "39.5426, 116.2350")
# points = {p1, p2, p3, p4, p5}

def first(points):
    return next(iter(points))

def distance(a, x, roads):
    for r in roads:
        if r.name == a.id and r.destination == x.id:
            return r.distance

def nearest_neighbour(a, points, roads):
    return min(points, key=lambda x: distance(a,x, roads))

def nn_tour(points, roads):
    start = points[0]
    points = set(points)
    tour = [start]
    unvisited = points - {start}
    while unvisited: 
        c = nearest_neighbour(tour[-1], unvisited, roads)
        tour.append(c)
        unvisited.remove(c)
    return tour


# nn = nn_tour(points)
# for n in nn:
#     name = Point(name) 
#     print(n.name)
 

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        content = request.form.get('Mi  asto')
        content2 = request.form.get('Kordy')
        try:
            point = Point(name=content, coordinates=content2)
        except:
            return redirect('/')
        db.session.add(point)
        db.session.commit()
        return redirect('/')
    else:
        points = Point.query.all()
        roads = []
        for p in points:
            for destination in points:
                if p != destination:
                    distance = client.distance_matrix(p.coordinates, destination.coordinates)
                    roads.append(Road(name=p.id, destination=destination.id, distance=distance['rows'][0]['elements'][0]['distance']['value']))
        try:
            ok = nn_tour(points, roads)
        except:
            ok = 'Nie ma zadnych drog'
        return render_template("index.html", points=points, ok=ok)


@app.route('/fromDatabase')
def fromDatabase():
    query = Point.query.all()
    list = []
    list.append(Klasa('id', 'name', 'coordinates'))           
    return redirect('/')


@app.route("/delete")
def delete():
    id_get = request.args["id"]
    Point.query.filter_by(id=id_get).delete()
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)