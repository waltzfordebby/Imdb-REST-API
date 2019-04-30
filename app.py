from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Init app
app = Flask(__name__)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://waltzfordebby:password@localhost/imdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)


# Movie Class/Model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True, unique=True)
    year = db.Column(db.String(20), nullable=True)
    rating = db.Column(db.String(10), nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.Text, nullable=True)
    imdb_score = db.Column(db.Float, nullable=True)
    metascore = db.Column(db.Integer, nullable=True)
    synopsis = db.Column(db.Text, nullable=True)
    vote = db.Column(db.Integer, nullable=True)
    gross = db.Column(db.Integer, nullable=True)
    director = db.Column(db.Text, nullable=True)
    stars = db.Column(db.Text, nullable=True)

    def __init__(self, name, year, rating, runtime, genre, imdb_score, metascore, synopsis, vote, gross, director, stars):
        self.name = name
        self.year = year
        self.rating = rating
        self.runtime = runtime
        self.genre = genre
        self.imdb_score = imdb_score
        self.metascore = metascore
        self.synopsis = synopsis
        self.vote = vote
        self.gross = gross
        self.director = director
        self.stars


# Movie Schema
class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "year", "rating", "runtime", "genre",
                  "imdb_score", "metascore", "synopsis", "vote", "gross", "director", "stars")


# Init Schema
movie_schema = MovieSchema(strict=True)
movies_schema = MovieSchema(many=True, strict=True)


# Get All Movies
@app.route("/movie", methods=["GET"])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies)

    return jsonify(result.data)


# Get Single Movie
@app.route("/movie/<id>", methods=["GET"])
def get_movie(id):
    movie = Movie.query.get(id)
    return movie_schema.jsonify(movie)


# Create Movie
@app.route("/movie", methods=["POST"])
def add_movie():
    name = request.json["name"]
    year = request.json["year"]
    rating = request.json["rating"]
    runtime = request.json["runtime"]
    genre = request.json["genre"]
    imdb_score = request.json["imdb_score"]
    metascore = request.json["metascore"]
    synopsis = request.json["synopsis"]
    vote = request.json["vote"]
    gross = request.json["gross"]
    director = request.json["director"]
    stars = request.json["stars"]

    new_movie = Movie(name, year, rating, runtime, genre, imdb_score,
                      metascore, synopsis, vote, gross, director, stars)

    db.session.add(new_movie)
    db.session.commit()

    return movie_schema.jsonify(new_movie)


# Update Movie
@app.route("/movie/<id>", methods=["PUT"])
def update_movie(id):
    movie = Movie.query.get(id)

    name = request.json["name"]
    year = request.json["year"]
    rating = request.json["rating"]
    runtime = request.json["runtime"]
    genre = request.json["genre"]
    imdb_score = request.json["imdb_score"]
    metascore = request.json["metascore"]
    synopsis = request.json["synopsis"]
    vote = request.json["vote"]
    gross = request.json["gross"]
    director = request.json["director"]
    stars = request.json["stars"]

    movie.name = name
    movie.year = year
    movie.rating = rating
    movie.runtime = runtime
    movie.genre = genre
    movie.imdb_score = imdb_score
    movie.metascore = metascore
    movie.synopsis = synopsis
    movie.vote = vote
    movie.gross = gross
    movie.director = director
    movie.stars = stars

    db.session.commit()

    return movie_schema.jsonify(movie)


# Delete Movie
@app.route("/movie/<id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()

    return movie_schema.jsonify(movie)


# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found"}), 404)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
