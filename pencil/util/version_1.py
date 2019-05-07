from pencil import db


def create_row_list(container, model):

    for content in container:
        column = model.query.filter_by(name=content).first()

        if column is None:
            column = model(l)
            db.session.add(column)
            db.session.commit()

        yield column


def add_record(value, model):

    print(type(model))
    column = model.query.filter_by(name=value).first()

    if column is None:
        column = model(value)
        db.session.add(column)
        db.session.commit()

        return column

    return column


def add_record2(value, model):

    column = model.query.filter_by(score=value).first()

    if column is None:
        column = model(value)
        db.session.add(column)
        db.session.commit()

        return column

    return column
