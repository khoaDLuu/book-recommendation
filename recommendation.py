from models import Buy


def recommendations_for_user(user_id, num=20):
    # temp
    return books_from_buys(user_id)


def recommendations_from_book(book_idx, threshold=.1):
    return [""]


def books_from_buys(user_id):
    results = Buy.query.filter_by(user_id=user_id).with_entities(Buy.book_name).all()
    return [book_name for book_name, *_ in results]
