import json
import MySQL.commands as database
import flags_data.flags as flags

try:
    pl = json.load(open("language\\pl.json", 'r', encoding="utf-8"))
    en = json.load(open("language\\en.json", 'r', encoding="utf-8"))
    language = {"PL": pl, "EN": en}
    langstr = {"PL": "Polski", "EN": "English"}
except FileNotFoundError:
    print("[BOT]: Error: language files not found! get them from here: ")
    input("Press enter to close.")
    exit()


class Player:
    def __init__(self, player_id):
        self.player_id: str = player_id
        self.data = database.get_player_data(player_id=player_id)
        self.check_user()
        self.lang: dict = language[self.data[0]]
        self.lang_flags: dict = flags.language_flags[self.data[1]]
        self.points: int = self.data[2]
        self.langstr: str = langstr[self.data[1]]

    def add_points(self, value: int):
        value += self.points
        database.add_points(value=value, player_id=self.player_id)

    def check_user(self):
        if not self.data:
            database.create_user(player_id=self.player_id)
            self.data = database.get_player_data(player_id=self.player_id)

    def change_lang(self, lang: str):
        self.lang = language[lang.upper()]
        database.set_lang(player_id=self.player_id, lang=lang, lang_type="lang")

    def change_flag_lang(self, lang: str):
        self.lang_flags = flags.language_flags[lang.upper()]
        database.set_lang(player_id=self.player_id, lang=lang, lang_type="flags_lang")
        self.langstr: str = langstr[self.data[1]]
