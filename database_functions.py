from pymongo.database import Database
from dotenv import load_dotenv
import os
from statistics import mean
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure

# import matplotlib

load_dotenv()

# user_id = interaction.user.id
try:
    client = MongoClient(os.getenv("MONGO_URL"))
except ConnectionFailure:
    print("Failed to connect to MongoDB")
    exit()


RQ_COLLECTIONS = ["punten"]


def add_user_db(user_id: int) -> Database:
    """
    Add a new user database

    Args:
        user_id (int): The user ID (Discord, in this case)

    Returns:
        Database: The newly created database, or if it already exists, the existing one
    """

    # Check if a database for the user already exists, if so, return it
    if str(user_id) in client.list_database_names():
        return client.get_database(str(user_id))

    new_database = client[str(user_id)]

    # Add every required collection to the database
    for collection in RQ_COLLECTIONS:
        new_database.create_collection(collection)

    return new_database


# Test
# print(add_user_db(user_id).name)


def add_punt(
    user_id: int, punt: float, vak: str, type: str = "", *, special_event: str = "N/A"
):
    # TODO: Add compatibilty for date

    if isinstance(punt, int) or punt > 10.0 or punt < 1.0:
        # Mark is invalid
        return False

    if not str(user_id) in client.list_database_names():
        user_db = add_user_db(user_id)
    else:
        user_db = client.get_database(str(user_id))

    pt_coll = user_db.get_collection("punten")
    document = pt_coll.insert_one(
        {"punt": punt, "vak": vak, "special_event": special_event, "type": type}
    )

    return document.inserted_id


# Test


def get_avg(user_id: int, vak: str = None):
    # TODO: Add support for graph, graph will be only possible with more than 3 marks for a subject
    db = client.get_database(str(user_id))
    col = db.get_collection("punten")
    qry = col.find({"vak": vak})
    if len(qry) == 0:
        return None
    return round(mean(doc["punt"] for doc in qry), 1)


def showmark(user_id: int, vak: str = None, all: bool = False):
    db = client.get_database(str(user_id))
    col = db.get_collection("punten")
    qry = col.find({"vak": vak})
    qry2 = qry(doc["punt"] for doc in qry)
    if all == True:
        qry = col.find("punt")


# Test
# print(get_mark(user_id, avg=True, vak="WiskundeB"))


def edit_punt(user_id: int, punt_id: str, new_punt: float, new_vak: str):
    pass


def remove_punt(user_id: int, punt_id: str):
    # NOTE: Admin only
    pass


def clear_punt_client(user_id: int):
    # NOTE: Admin only, with "are you sure" question
    pass
