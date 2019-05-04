from flask import request, jsonify, abort, make_response, Blueprint
from pencil.models.version_1 import *
from pencil.schemas.version_1 import *


pencil = Blueprint("pencil", __name__)


# Get All Movies
@pencil.route("/pencil/api/v1.0/movies", methods=["GET"])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies)

    return jsonify(result.data)


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
