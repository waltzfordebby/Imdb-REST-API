from pencil import ma

# Year Schema


class YearSchema(ma.Schema):
    class Meta:
        fields = ["id", "name"]


# Init Schema
year_schema = YearSchema(strict=True)
years_schema = YearSchema(many=True, strict=True)


# Rating Schema
class RatingSchema(ma.Schema):
    class Meta:
        fields = ["id", "name"]


# Init Schema
rating_schema = RatingSchema(strict=True)
ratings_schema = RatingSchema(many=True, strict=True)


# ImdbScore Schema
class ImdbScoreSchema(ma.Schema):
    class Meta:
        fields = ["id", "score"]


# Init Schema
imdb_score_schema = ImdbScoreSchema(strict=True)
imdb_scores_schema = ImdbScoreSchema(many=True, strict=True)


# MetaScore Schema
class MetaScoreSchema(ma.Schema):
    class Meta:
        fields = ["id", "score"]


# Init Schema
meta_score_schema = MetaScoreSchema(strict=True)
meta_scores_schema = MetaScoreSchema(many=True, strict=True)


# Genre Schema
class GenreSchema(ma.Schema):
    class Meta:
        fields = ["id", "name"]


# Init Schema
genre_schema_ = GenreSchema(strict=True)
genres_schema = GenreSchema(many=True, strict=True)


# Director Schema
class DirectorSchema(ma.Schema):
    class Meta:
        fields = ["id", "name"]


# Init Schema
director_schema = DirectorSchema(strict=True)
directors_schema = DirectorSchema(many=True, strict=True)


# Director Schema
class DirectorSchema(ma.Schema):
    class Meta:
        fields = ["id", "name"]


# Init Schema
director_schema = DirectorSchema(strict=True)
directors_schema = DirectorSchema(many=True, strict=True)


# Star Schema
class StarSchema(ma.Schema):
    class Meta:
        fields = ["id", "name"]


# Init Schema
star_schema = StarSchema(strict=True)
stars_schema = StarSchema(many=True, strict=True)


# Movie Schema
class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "runtime", "synopsis",
                  "vote", "gross", "year", "rating", "imdb_score", "meta_score", "genres", "directors", "stars")

    year = ma.Nested(YearSchema)
    rating = ma.Nested(RatingSchema)
    imdb_score = ma.Nested(ImdbScoreSchema)
    meta_score = ma.Nested(MetaScoreSchema)
    genres = ma.List(ma.Nested(GenreSchema))
    directors = ma.List(ma.Nested(DirectorSchema))
    stars = ma.List(ma.Nested(StarSchema))


# Init Schema
movie_schema = MovieSchema(strict=True)
movies_schema = MovieSchema(many=True, strict=True)
