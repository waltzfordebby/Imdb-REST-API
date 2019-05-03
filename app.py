from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Init app
app = Flask(__name__)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://waltzfordebby:password@localhost/imdb2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

genres = db.Table("genres",
                  db.Column("movie_id", db.Integer, db.ForeignKey(
                      "movie.id"), primary_key=True),
                  db.Column("genre_id", db.Integer, db.ForeignKey(
                      "genre.id"), primary_key=True)
                  )

directors = db.Table("directors",
                     db.Column("movie_id", db.Integer, db.ForeignKey(
                         "movie.id"), primary_key=True),
                     db.Column("genre_id", db.Integer, db.ForeignKey(
                         "director.id"), primary_key=True)
                     )

stars = db.Table("stars",
                 db.Column("movie_id", db.Integer, db.ForeignKey(
                     "movie.id"), primary_key=True),
                 db.Column("genre_id", db.Integer, db.ForeignKey(
                     "star.id"), primary_key=True)
                 )


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    vote = db.Column(db.Integer, nullable=False)
    gross = db.Column(db.Integer, nullable=False)
    genres = db.relationship("Genre", secondary=genres,
                             lazy="subquery", backref=db.backref("movies", lazy=True))
    year_id = db.Column(db.Integer, db.ForeignKey("year.id"), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey(
        "rating.id"), nullable=False)
    imdb_score_id = db.Column(db.Integer, db.ForeignKey(
        "imdb_score.id"), nullable=False)
    meta_score_id = db.Column(db.Integer, db.ForeignKey(
        "meta_score.id"), nullable=False)
    directors = db.relationship("Director", secondary=directors,
                                lazy="subquery", backref=db.backref("movies", lazy=True))

    stars = db.relationship("Star", secondary=stars,
                            lazy="subquery", backref=db.backref("movies", lazy=True))

    def __init__(self, name, runtime, synopsis, vote, gross, year_id, rating_id, imdb_score_id, meta_score_id):
        self.name = name
        self.runtime = runtime
        self.synopsis = synopsis
        self.vote = vote
        self.gross = gross
        self.year_id = year_id
        self.rating_id = rating_id
        self.imdb_score_id = imdb_score_id
        self.meta_score_id = meta_score_id


class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), unique=True, nullable=False)
    movies = db.relationship("Movie", backref="year", lazy=True)

    def __init__(self, name):
        self.name = name


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(10), nullable=True)
    movies = db.relationship("Movie", backref="rating", lazy=True)

    def __init__(self, name):
        self.name = name


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class ImdbScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False, unique=True)
    movies = db.relationship("Movie", backref="imdb_score", lazy=True)

    def __init__(self, score):
        self.score = score


class MetaScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False, unique=True)
    movies = db.relationship("Movie", backref="meta_score", lazy=True)

    def __init__(self, score):
        self.score = score


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Star(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

# Movie Schema
# class MovieSchema(ma.Schema):
#     class Meta:
#         fields = ("id", "name", "year", "rating", "runtime", "genre",
#                   "imdb_score", "metascore", "synopsis", "vote", "gross", "director", "stars")


# # Init Schema
# movie_schema = MovieSchema(strict=True)
# movies_schema = MovieSchema(many=True, strict=True)


# # Get All Movies
# @app.route("/pencil/api/v1.0/movies", methods=["GET"])
# def get_movies():
#     all_movies = Movie.query.all()
#     result = movies_schema.dump(all_movies)

#     return jsonify(result.data)


# # Get Single Movie
# @app.route("/pencil/api/v1.0/movies/<id>", methods=["GET"])
# def get_movie(id):
#     movie = Movie.query.get(id)
#     return movie_schema.jsonify(movie)


# Create Movie
@app.route("/pencil/api/v1.0/movies", methods=["POST"])
def add_movie():
    genre_container = []
    director_container = []
    star_container = []

    r_name = request.json["name"]
    r_runtime = request.json["runtime"]
    r_synopsis = request.json["synopsis"]
    r_vote = request.json["vote"]
    r_gross = request.json["gross"]
    r_year = request.json["year"]
    r_rating = request.json["rating"]
    r_imdb_score = request.json["imdb_score"]
    r_metascore = request.json["metascore"]
    r_genres = request.json["genre"]
    r_directors = request.json["director"]
    r_stars = request.json["stars"]

    # new_movie = Movie(name, year, rating, runtime, genre, imdb_score,
    #                   metascore, synopsis, vote, gross, director, stars)

    year = Year.query.filter_by(name=r_year).first()

    if year is None:
        year = Year(r_year)
        db.session.add(year)
        db.session.commit()

    rating = Rating.query.filter_by(name=r_rating).first()

    if rating is None:
        rating = Rating(r_rating)
        db.session.add(rating)
        db.session.commit()

    imdb_score = MetaScore.query.filter_by(score=r_imdb_score).first()

    if imdb_score is None:
        imdb_score = ImdbScore(r_imdb_score)
        db.session.add(imdb_score)
        db.session.commit()

    meta_score = MetaScore.query.filter_by(score=r_metascore).first()

    if meta_score is None:
        meta_score = MetaScore(r_metascore)
        db.session.add(meta_score)
        db.session.commit()

    for r_genre in r_genres:

        genre = Genre.query.filter_by(name=r_genre).first()

        if genre is None:
            genre = Genre(r_genre)
            db.session.add(genre)
            db.session.commit()

        genre_container.append(genre)

    for r_director in r_directors:

        director = Director.query.filter_by(name=r_director).first()

        if director is None:
            director = Director(r_director)
            db.session.add(director)
            db.session.commit()

        director_container.append(director)

    for r_star in r_stars:

        star = Star.query.filter_by(name=r_star).first()

        if star is None:
            star = Star(r_star)
            db.session.add(star)
            db.session.commit()

        star_container.append(star)

    movie = Movie.query.filter_by(name=r_name).first()

    if movie is None:
        movie = Movie(r_name, r_runtime, r_synopsis, r_vote, r_gross,
                      year.id, rating.id, imdb_score.id, meta_score.id)
        db.session.add(movie)
        db.session.commit()

        for genre in genre_container:
            movie.genres.append(genre)

        for director in director_container:
            movie.directors.append(director)

        for star in star_container:
            movie.stars.append()

        db.session.commit()

    return movie

# # Update Movie
# @app.route("/pencil/api/v1.0/movies/<id>", methods=["PUT"])
# def update_movie(id):
#     movie = Movie.query.get(id)

#     name = request.json["name"]
#     year = request.json["year"]
#     rating = request.json["rating"]
#     runtime = request.json["runtime"]
#     genre = request.json["genre"]
#     imdb_score = request.json["imdb_score"]
#     metascore = request.json["metascore"]
#     synopsis = request.json["synopsis"]
#     vote = request.json["vote"]
#     gross = request.json["gross"]
#     director = request.json["director"]
#     stars = request.json["stars"]

#     movie.name = name
#     movie.year = year
#     movie.rating = rating
#     movie.runtime = runtime
#     movie.genre = genre
#     movie.imdb_score = imdb_score
#     movie.metascore = metascore
#     movie.synopsis = synopsis
#     movie.vote = vote
#     movie.gross = gross
#     movie.director = director
#     movie.stars = stars

#     db.session.commit()

#     return movie_schema.jsonify(movie)


# # Delete Movie
# @app.route("/pencil/api/v1.0/movies/<id>", methods=["DELETE"])
# def delete_movie(id):
#     movie = Movie.query.get(id)
#     db.session.delete(movie)
#     db.session.commit()

#     return movie_schema.jsonify(movie)


# # Error Handlers
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({"error": "Not Found"}), 404)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
