from pencil import db

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

    def __init__(self, name, runtime, synopsis, vote, gross, year, rating, imdb_score, meta_score):
        self.name = name
        self.runtime = runtime
        self.synopsis = synopsis
        self.vote = vote
        self.gross = gross
        self.year = year
        self.rating = rating
        self.imdb_score = imdb_score
        self.meta_score = meta_score


class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), unique=True, nullable=False)
    movies = db.relationship(
        "Movie", backref=db.backref("year", lazy="subquery"))

    def __init__(self, name):
        self.name = name


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(10), nullable=True)
    movies = db.relationship(
        "Movie", backref=db.backref("rating", lazy="subquery"))

    def __init__(self, name):
        self.name = name


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class ImdbScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.String(10), nullable=False, unique=True)
    movies = db.relationship(
        "Movie", backref=db.backref("imdb_score", lazy="subquery"))

    def __init__(self, score):
        self.score = score


class MetaScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False, unique=True)
    movies = db.relationship(
        "Movie", backref=db.backref("meta_score", lazy="subquery"))

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
