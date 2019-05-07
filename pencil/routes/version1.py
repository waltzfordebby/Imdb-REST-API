from flask import Blueprint, request, jsonify, abort, make_response
from pencil.models.version_1 import *
from pencil.schemas.version_1 import *
from pencil.util.version_1 import create_record_list, add_record_string, add_record_integer


pencil = Blueprint("pencil", __name__)


# Get All Movies
@pencil.route("/pencil/api/v1.0/movies", methods=["GET"])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies)

    return jsonify(result.data), 200

# Get Single Movie
@pencil.route("/pencil/api/v1.0/movies/<id>", methods=["GET"])
def get_movie(id):
    movie = Movie.query.get(id)

    if movie is None:
        abort(404)

    return movie_schema.jsonify(movie), 200

# Create Movie
@pencil.route("/pencil/api/v1.0/movies", methods=["POST"])
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

    year = add_record_string(r_year, Year)
    rating = add_record_string(r_rating, Rating)
    imdb_score = add_record_integer(r_imdb_score, ImdbScore)
    meta_score = add_record_integer(r_metascore, MetaScore)
    genre_container = list(create_record_list(r_genres, Genre))
    director_container = list(create_record_list(r_directors, Director))
    star_container = list(create_record_list(r_stars, Star))

    movie = Movie.query.filter_by(name=r_name).first()

    if movie is None:
        movie = Movie(r_name, r_runtime, r_synopsis, r_vote, r_gross,
                      year, rating, imdb_score, meta_score)
        db.session.add(movie)
        db.session.commit()

        for genre_content in genre_container:
            movie.genres.append(genre_content)

        for director_content in director_container:
            movie.directors.append(director_content)

        for star_content in star_container:
            movie.stars.append(star_content)

        db.session.commit()

    return movie_schema.jsonify(movie), 201


# Update Movie
@pencil.route("/pencil/api/v1.0/movies/<id>", methods=["PUT"])
def update_movie(id):
    movie = Movie.query.get(id)

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

    year = add_record_string(r_year, Year)
    rating = add_record_string(r_rating, Rating)
    imdb_score = add_record_integer(r_imdb_score, ImdbScore)
    meta_score = add_record_integer(r_metascore, MetaScore)
    genre_container = list(create_row_list(r_genres, Genre))
    director_container = list(create_row_list(r_directors, Director))
    star_container = list(create_row_list(r_stars, Star))

    if movie is None:
        abort(404)

    movie.name = r_name
    movie.runtime = r_runtime
    movie.synopsis = r_synopsis
    movie.vote = r_vote
    movie.gross = r_gross
    movie.year = year
    movie.rating = rating
    movie.imdb_score = imdb_score
    movie.meta_score = meta_score

    for genre_content in genre_container:
        movie.genres.append(genre_content)

    for director_content in director_container:
        movie.directors.append(director_content)

    for star_content in star_container:
        movie.stars.append(star_content)

    db.session.commit()

    return movie_schema.jsonify(movie)


@pencil.route("/pencil/api/v1.0/movies/<id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get(id)

    if movie is None:
        abort(404)

    db.session.delete(movie)
    db.session.commit()

    return movie_schema.jsonify(movie)
