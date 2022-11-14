import json
import random
import nextcord
import nextcord.ui
from nextcord.ext import commands
import player
import asyncio
from buttons import Zoom, EasyMode

intents = nextcord.Intents.default()
# noinspection PyDunderSlots,PyUnresolvedReferences
intents.message_content = True
# noinspection PyDunderSlots,PyUnresolvedReferences
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents, activity=nextcord.Game("Wziumolandia"))


@bot.event
async def on_ready():
    print("Bot został uruchmiony.")


@bot.slash_command(description="easy mode", dm_permission=True)
async def easymode(interaction: nextcord.Interaction):
    gamer = player.Player(player_id=str(interaction.user.id))
    flag = random.choice(gamer.lang_flags)
    view = EasyMode(correct=flag['name'],
                    flags=gamer.lang_flags,
                    player_lang=gamer.lang,
                    flag_code=flag['code'],
                    id_of_player=str(interaction.user.id))
    embed = nextcord.Embed(type="rich",
                           colour=nextcord.Colour.green(),
                           title=f"{gamer.lang['easy_tittle']}")
    embed.add_field(name=f"{gamer.lang['good_luck']}",
                    value=f"{gamer.lang['flag_random']} :flag_{flag['code'].lower()}:\n"
                          f"{gamer.lang['guess_easy']}\n"
                          f"{gamer.lang['answers_lang']}**{gamer.langstr}**")
    await interaction.send(embed=embed, ephemeral=True, view=view)
    try:
        await bot.wait_for("interaction", timeout=15)
    except asyncio.TimeoutError:
        embed = nextcord.Embed(type="rich",
                               colour=nextcord.Colour.red(),
                               title=f"{gamer.lang['easy_tittle']}")
        embed.add_field(name=f"{gamer.lang['timeout']}",
                        value=f"{gamer.lang['answer_is']} {flag['name']}")
        await interaction.send(embed=embed, ephemeral=True)
        view.stop()
    await view.wait()


@bot.slash_command(description="hard mode", dm_permission=True)
async def hardmode(interaction: nextcord.Interaction):
    gamer = player.Player(player_id=str(interaction.user.id))
    flag = random.choice(gamer.lang_flags)
    embed = nextcord.Embed(type="rich",
                           colour=nextcord.Colour.green(),
                           title=f"{gamer.lang['hard_tittle']}")
    embed.add_field(name=f"{gamer.lang['good_luck']}",
                    value=f"{gamer.lang['flag_random']} :flag_{flag['code'].lower()}:\n "
                          f"{gamer.lang['guess']}\n"
                          f"{gamer.lang['answers_lang']}**{gamer.langstr}**")
    view = Zoom(flag['code'], gamer.lang)
    await interaction.send(embed=embed, view=view, ephemeral=True)
    while True:
        try:
            answer = await bot.wait_for("message", timeout=15, check=None)
            if answer.author.id == interaction.user.id:
                if answer.content.lower() == flag['name'].lower():
                    embed = nextcord.Embed(type="rich",
                                           colour=nextcord.Colour.green(),
                                           title=f"{gamer.lang['hard_tittle']}")
                    embed.add_field(name=f"{gamer.lang['good_job']}",
                                    value=f"{gamer.lang['good_answer']}")
                    await interaction.send(embed=embed, ephemeral=True)
                    gamer.add_points(random.randint(5, 8))
                    break
                embed = nextcord.Embed(type="rich",
                                       colour=nextcord.Colour.red(),
                                       title=f"{gamer.lang['hard_tittle']}")
                embed.add_field(name=f"{gamer.lang['bad_answer']}",
                                value=f"{gamer.lang['answer_is']} {flag['name']}")
                await interaction.send(embed=embed, ephemeral=True)
                break
            continue
        except asyncio.TimeoutError:
            embed = nextcord.Embed(type="rich",
                                   colour=nextcord.Colour.red(),
                                   title=f"{gamer.lang['hard_tittle']}")
            embed.add_field(name=f"{gamer.lang['timeout']}",
                            value=f"{gamer.lang['answer_is']} {flag['name']}")
            await interaction.send(embed=embed, ephemeral=True)
            break
    view.stop()


@bot.slash_command(description="Change language")
async def lang(interaction: nextcord.Interaction,
               language: str = nextcord.SlashOption(
                   name="lang",
                   choices=["Polski", "English"],
                   required=True)):
    new_lang = {"Polski": "PL", "English": "EN"}
    executer = player.Player(player_id=str(interaction.user.id))
    executer.change_lang(lang=new_lang[language])
    embed = nextcord.Embed(type="rich",
                           colour=nextcord.Colour.green(),
                           title=f"{executer.lang['lang_change_title']}")
    embed.add_field(name=f"{executer.lang['lang_change']}",
                    value=f"{executer.lang['new_lang']}{language}")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command(description="Change flags names language")
async def lang_flag(interaction: nextcord.Interaction,
                    language: str = nextcord.SlashOption(
                        name="lang",
                        choices=["Polski", "English"],
                        required=True)):
    executer = player.Player(player_id=str(interaction.user.id))
    new_lang = {"Polski": "PL", "English": "EN"}
    executer.change_flag_lang(lang=new_lang[language])
    embed = nextcord.Embed(type="rich",
                           colour=nextcord.Colour.green(),
                           title=f"{executer.lang['lang_change_title']}")
    embed.add_field(name=f"{executer.lang['flag_lang']}",
                    value=f"{executer.lang['new_lang']}{language}")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command(description="Check how many points someone has")
async def points(interaction: nextcord.Interaction,
                 member: nextcord.Member = nextcord.SlashOption(name="user", required=False)):
    executer = player.Player(player_id=interaction.user.id)
    if not member:
        embed = nextcord.Embed(type="rich",
                               colour=nextcord.Colour.green(),
                               title=f"{executer.lang['points']}")
        embed.add_field(name=f"{executer.lang['player_points']}",
                        value=f"{executer.points}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        info = player.Player(player_id=member.id)
        embed = nextcord.Embed(type="rich",
                               colour=nextcord.Colour.green(),
                               title=f"{executer.lang['points']}")
        embed.add_field(name=f"{executer.lang['player_points_other']} **{member.name}**",
                        value=f"{info.points}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

if __name__ == "__main__":
    with open("config/config.json") as config:
        cfg = json.load(config)
        bot.run(cfg["Bot"]["Bot_token"])
