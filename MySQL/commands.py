import MySQL.database as db
from typing import Tuple


def get_player_data(player_id: str) -> Tuple[str, int]:
    db.cursor.execute(f"SELECT lang, flags_lang, points FROM `userdata` WHERE player_ID='{player_id}'")
    return db.cursor.fetchall()[0]


def add_points(player_id: str, value: int):
    db.cursor.execute(f"UPDATE `userdata` SET `points` = {value} WHERE player_ID='{player_id}'")
    db.user_data.commit()


def create_user(player_id: str):
    db.cursor.execute(f"INSERT INTO `userdata` (`player_ID`, `lang`, `flags_lang`, `points`) "
                      f"VALUES ('{player_id}', 'EN', 'EN', '0')")
    db.user_data.commit()


def set_lang(player_id: str, lang: str, lang_type: str):
    db.cursor.execute(f"UPDATE `userdata` SET `{lang_type}` = '{lang}' WHERE `userdata`.`player_ID` = '{player_id}'")
    db.user_data.commit()

