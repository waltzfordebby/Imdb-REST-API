from flask import Blueprint, request, jsonify, abort, make_response
from pencil.models.version_1 import *
from pencil.schemas.version_1 import *
from pencil.util.version_1 import create_row_list, add_record, add_record2


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

    year = add_record(r_year, Year)
    rating = add_record(r_rating, Rating)
    imdb_score = add_record2(r_imdb_score, ImdbScore)
    meta_score = add_record2(r_metascore, MetaScore)
    genre_container = list(create_row_list(r_genres, Genre))
    director_container = list(create_row_list(r_directors, Director))
    star_container = list(create_row_list(r_stars, Star))

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
