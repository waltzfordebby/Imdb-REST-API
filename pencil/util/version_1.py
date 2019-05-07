from pencil import db


def create_record_list(container, model):

    for content in container:
        column = model.query.filter_by(name=content).first()

        if column is None:
            column = model(content)
            db.session.add(column)
            db.session.commit()

        yield column


def add_record_string(value, model):

    column = model.query.filter_by(name=value).first()

    if column is None:
        column = model(value)
        db.session.add(column)
        db.session.commit()

        return column

    return column


def add_record_integer(value, model):

    column = model.query.filter_by(score=value).first()

    if column is None:
        column = model(value)
        db.session.add(column)
        db.session.commit()

        return column

    return column
