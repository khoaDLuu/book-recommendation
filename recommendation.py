import pickle
import requests
import pandas as pd

from pathlib import Path
from models import Buy, Book


DATASET = None
AUTHOR_LK_MODEL = None


def get_recommendations(user_id: int, recs_per_book: int) -> list:
    return list(
        recommendations_for_user(
            user_id, load_dataset(), load_author_lk_model(), n=recs_per_book
        )
    )


def recommendations_for_user(user_id: int, dataset, kernel, n: int) -> set:
    user_bought_buys = bought_buys(user_id)
    return set(
        [  # quick
            rec_book_id
            for book_id in user_bought_buys
            for rec_book_id in recommendations_from_book(
                book_id_to_index(book_id, dataset),
                dataset,
                kernel,
                n,
            )["id"]
            if book_id_to_index(book_id, dataset) > 0
        ]
    )


def recommendations_from_book(book_idx: int, dataset, kernel, n: int, threshold: float = .1):
    sim = sorted(
        list(enumerate(kernel[book_idx])),
        key=lambda x: x[1],
        reverse=True,
    )
    index = [i[0] for i in sim if i[0] != book_idx and i[1] > threshold]

    similar_author = dataset.index.isin(index)
    same_cluster = dataset.cluster == dataset.iloc[book_idx]['cluster']
    return dataset.loc[similar_author & same_cluster].sort_values(by='score', ascending=False).head(n)


def book_id_to_index(book_id: int, dataset) -> int:
    print(dataset.columns)
    print(dataset.head())
    print(book_id)
    try:
        print(dataset["id"])
        return int(dataset[dataset["id"] == book_id].index[0])
    except IndexError:
        return -1


def book_index_to_id(book_idx: int, dataset) -> int:
    return int(dataset["id"][book_idx])


def bought_buys(user_id: int) -> list:
    results = Buy.query.filter_by(user_id=user_id).with_entities(Buy.book_id).all()
    return [book_id for book_id, *_ in results]


def load_dataset(file_name: str = "data_product_v3.csv"):
    file_path = f"/tmp/{file_name}"
    if not file_exists(file_path):
        pull_dataset()

    global DATASET
    if DATASET is None:
        DATASET = pd.read_csv(file_path, sep=',', index_col=[0])
    return DATASET


def load_author_lk_model(file_name: str = "author_lk_model.pickle"):
    file_path = f"/tmp/{file_name}"
    if not file_exists(file_path):
        pull_author_lk_model()

    global AUTHOR_LK_MODEL
    if AUTHOR_LK_MODEL is None:
        with open(file_path, 'rb') as f:
            AUTHOR_LK_MODEL = pickle.load(f)
    return AUTHOR_LK_MODEL


def pull_dataset():
    url = "https://drive.google.com/uc?export=download&id=19A8Qq1mrne0SPfEvpw-w7H39wr-tKPvm"
    file_name = "data_product_v3.csv"
    pull_resource(url, file_name)


def pull_author_lk_model():
    url = "https://drive.google.com/uc?export=download&id=1hoiCdcjJLJLjJGzK-ZAEtC2zjiNAS9DK"
    file_name = "author_lk_model.pickle"
    pull_resource(url, file_name)


def pull_resource(url, file_name: str):
    resource_file = requests.get(url).content
    with open(f"/tmp/{file_name}", "wb") as f:
        f.write(resource_file)


def file_exists(file_name: str):
    return Path(f"/tmp/{file_name}").is_file()
