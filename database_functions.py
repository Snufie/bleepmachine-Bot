from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
import os

load_dotenv()

user_id = 123456789

DB: MongoClient = MongoClient(os.getenv("MONGO_URL"))

RQ_COLLECTIONS = ["punten", "boontjes"]


def add_user_db(user_id: int) -> Database:
    """
    Add a new user database

    Args:
        user_id (int): The user ID (Discord, in this case)

    Returns:
        Database: The newly created database, or if it already exists, the existing one
    """

    # Check if a database for the user already exists, if so, return it
    if str(user_id) in DB.list_database_names():
        return DB.get_database(str(user_id))

    new_database = DB[str(user_id)]

    # Add every required collection to the database
    for collection in RQ_COLLECTIONS:
        new_database.create_collection(collection)

    return new_database


# Test
# print(add_user_db(user_id).name)


def add_punt(user_id: int, punt: float, vak: str, *, special_event: str = "N/A"):
    # TODO: Add compatibilty for date

    if isinstance(punt, int) or punt > 10.0 or punt < 1.0:
        # Mark is invalid
        return False

    if not str(user_id) in DB.list_database_names():
        user_db = add_user_db(user_id)
    else:
        user_db = DB.get_database(str(user_id))

    pt_coll = user_db.get_collection("punten")
    document = pt_coll.insert_one(
        {"punt": punt, "vak": vak, "special_event": special_event}
    )

    return document.inserted_id


# Test
add_punt(user_id, 6.9, "WisB")


def edit_punt(user_id: int, punt_id: str, new_punt: float, new_vak: str):
    pass


def remove_punt(user_id: int, punt_id: str):
    # NOTE: Admin only
    pass


def clear_punt_db(user_id: int, punt: float, vak: str):
    # NOTE: Admin only, with "are you sure" question
    pass
