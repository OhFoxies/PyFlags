import MySQL.database as db
from typing import Tuple


# Returns data about user with given ID.
def get_player_data(player_id: str) -> Tuple[str, int] or None:
    command = "SELECT lang, flags_lang, points FROM `userdata` WHERE player_ID=%s"
    values = (player_id,)
    db.cursor.execute(command, values)
    try:
        return db.cursor.fetchall()[0]
    except IndexError:
        return None


# Adds an given amount of points to current points of user.
def add_points(player_id: str, value: int):
    command = "UPDATE `userdata` SET `points` = %s WHERE player_ID=%s"
    values = (value, player_id)
    db.cursor.execute(command, values)
    db.user_data.commit()


# Creates a new tuple with informations about new user.
def create_user(player_id: str):
    command = "INSERT INTO `userdata` (`player_ID`, `lang`, `flags_lang`, `points`) VALUES (%s, %s, %s, %s)"
    values = (player_id, 'EN', 'EN', '0')
    db.cursor.execute(command, values)
    db.user_data.commit()


# Changes an given language type of given user.
def set_lang(player_id: str, lang: str, lang_type: str):
    command = f"UPDATE `userdata` SET `{lang_type}` = '{lang}' WHERE `player_ID` = %s"
    values = (player_id,)
    db.cursor.execute(command, values)
    db.user_data.commit()

