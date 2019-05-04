from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
from models.version_1 import *
from schemas.version_1 import *


# Init app
app = Flask(__name__)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://waltzfordebby:password@localhost/imdb2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["JSON_SORT_KEYS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)


# Get All Movies
@app.route("/pencil/api/v1.0/movies", methods=["GET"])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies)

    return jsonify(result.data)


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

    imdb_score = ImdbScore.query.filter_by(score=r_imdb_score).first()

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

        for genre_content in genre_container:
            movie.genres.append(genre_content)

        for director_content in director_container:
            movie.directors.append(director_content)

        for star_content in star_container:
            movie.stars.append(star_content)

        db.session.commit()

    r_star_container = []
    for star in movie.stars:
        r_star_container.append({"id": star.id, "name": star.name})

    r_director_container = []
    for director in movie.stars:
        r_director_container.append({"id": director.id, "name": director.name})

    r_genre_container = []
    for genre in movie.genres:
        r_genre_container.append({"id": genre.id, "name": genre.name})

    return movie_schema.jsonify(movie)

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
