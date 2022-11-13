import nextcord
import random
from typing import List

import player


class ZoomButton(nextcord.ui.Button):
    def __init__(self, flag: str, lang_dict: dict):
        self.lang = lang_dict
        self.code_flag = flag
        super().__init__(label=self.lang['zoom'], style=nextcord.ButtonStyle.green)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.send(f":flag_{self.code_flag}:".lower(), ephemeral=True)
        self.view.stop()


class Zoom(nextcord.ui.View):
    def __init__(self, flag: str, lang_dict: dict):
        super().__init__()
        self.flag = flag
        self.add_item(ZoomButton(flag=self.flag, lang_dict=lang_dict))


class EasyButton(nextcord.ui.Button):
    def __init__(self, label: str, is_correct: bool, flag_code: str, is_zoom: bool, style, player_lang: dict, correct,
                 id_of_player: str):
        super().__init__(label=label, style=style)
        self.player_lang = player_lang
        self.is_correct = is_correct
        self.flag_code = flag_code
        self.is_zoom = is_zoom
        self.correct = correct
        self.id = id_of_player

    async def callback(self, interaction: nextcord.Interaction):
        if self.is_correct:
            gamer = player.Player(player_id=self.id)
            embed = nextcord.Embed(type="rich",
                                   colour=nextcord.Colour.green(),
                                   title=f"{self.player_lang['easy_tittle']}")
            embed.add_field(name=f"{self.player_lang['good_job']}",
                            value=f"{self.player_lang['good_answer']}")
            await interaction.send(embed=embed, ephemeral=True)
            gamer.add_points(random.randint(1, 3))
            self.view.stop()
            self.view.clear_items()
        elif self.is_zoom:
            await interaction.send(f":flag_{self.flag_code}:".lower(), ephemeral=True)
        else:
            embed = nextcord.Embed(type="rich",
                                   colour=nextcord.Colour.red(),
                                   title=f"{self.player_lang['easy_tittle']}")
            embed.add_field(name=f"{self.player_lang['bad_answer']}",
                            value=f"{self.player_lang['answer_is']}{self.correct}")
            await interaction.send(embed=embed, ephemeral=True)
            self.view.stop()
            self.view.clear_items()


class EasyMode(nextcord.ui.View):
    def __init__(self, correct: str, flags: dict, player_lang: dict, flag_code: str, id_of_player: str):
        super().__init__()
        self.correct = correct
        self.flags = flags
        self.list_of_flags = self.random_flags()
        self.player_lang = player_lang
        self.flag_code = flag_code
        self.id = id_of_player
        for i in self.list_of_flags:
            self.add_item(EasyButton(label=i,
                                     is_correct=self.correct == i,
                                     is_zoom=False,
                                     flag_code=self.flag_code,
                                     style=nextcord.ButtonStyle.green,
                                     player_lang=self.player_lang,
                                     correct=self.correct,
                                     id_of_player=self.id))
        self.add_item(EasyButton(label=player_lang['zoom'],
                                 is_correct=False,
                                 is_zoom=True,
                                 flag_code=self.flag_code,
                                 style=nextcord.ButtonStyle.red,
                                 player_lang=self.player_lang,
                                 correct=self.correct,
                                 id_of_player=self.id))

    def random_flags(self) -> List[str]:
        all_flags = [self.correct]
        while True:
            if len(all_flags) == 4:
                break
            else:
                random_fla = random.choice(self.flags)
                if random_fla['name'] not in all_flags:
                    all_flags.append(random_fla['name'])
        random_flags = random.sample(all_flags, 4)
        return random_flags
