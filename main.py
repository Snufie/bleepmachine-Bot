import nextcord
from nextcord import Interaction, Member
from nextcord.application_command import SlashOption
from nextcord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import database_functions
import moderation
import edu
import rpg


# Variables

userinfracs = {}

mark_choices = [
    "Wiskunde A",
    "Wiskunde B",
    "Wiskunde C",
    "Wiskunde D",
    "Engels",
    "Nederlands",
    "Duits",
    "Frans",
    "Informatica",
    "Geschiedenis",
    "Biologie",
    "Aardrijkskunde",
    "Scheikunde",
    "Natuurkunde",
    "CKV",
    "Maatschappijleer",
    "Levensbeschouwing",
]

mark_se_choices = {
    "Punt uit toetsweek": "TW{tw_num}",
    "Praktische Opdracht": "PO",
    "Examen": "exam",
    "Tentamen": "tent",
    "Proefwerk": "PW",
    "Mondelinge Overhoring": "MO",
    "Schriftelijke Overhoring": "SO",
}

bad_words = ("kkr", "kanker", " kk ", "nigger", "neger", "nigr", "negr", "nigga", "nig")
exceptions_bw = ("kankerpatiënt", "heeft kanker")
welcomechannels = ["welcome", "welkom", "entrance", "ingang", "joins"]
# discuser = list(nextcord.Guild.members)
# print(discuser)

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True

try:
    client = MongoClient(os.getenv("MONGO_URL"))
except ConnectionFailure:
    print("Failed to connect to MongoDB")
    exit()

GUILD_IDS = (1039988764925251614,)
bot = commands.Bot(command_prefix="|", intents=intents)

# Code
load_dotenv()

# client = MongoClient(os.getenv("MONGO_URL"))
# db = client.test
# people = db.people
# testDocument = {
#    "test": "balls",
#    "test2": "bigger balls",
#    "Bigger": "Huge ballingus",
#    "5": 564,
# }
# people.insert_one(testDocument)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_member_join(member: Member):
    guild = member.guild
    welcome_channel = nextcord.utils.get(guild.channels, name=welcomechannels)
    if welcome_channel is None:
        print('No channel named "welcome" found')
        return

    await welcome_channel.send(f"Welkom in {guild.name} {member.mention}!")


@bot.listen("on_message")
async def badwords(message: nextcord.Message):
    if message.author == bot.user:
        return
    msg = message.content.strip(" ")
    print(msg)
    if any(word in msg for word in bad_words):
        infrac = "Ongeoorloofd taalgebruik"
        await moderation.badwords(
            message=message, infrac=infrac, author_id=message.author.id
        )


@bot.slash_command(guild_ids=GUILD_IDS)
async def clearinfracs(
    interaction: Interaction,
    user: nextcord.Member = SlashOption(
        required=True,
        description="The user to remove the infractions from",
    ),
):
    user1 = user.id
    print(user1)
    await moderation.clearinfracs(user=user1, user_name=user, interaction=interaction)


@bot.command(aliases=["pong"])
async def ping(ctx):
    await ctx.reply(f"Pong!\nLatentie: {round(bot.latency * 1000)}ms")


@bot.command()
async def deez(ctx):
    await ctx.reply("NUTS!!!")


@bot.command()
async def RPG(ctx):
    # await ctx.reply("E")
    await rpg.rpg(ctx=ctx, base=rpg.base_coll)
    await ctx.reply("balls")


@bot.command()
async def RPG_inventory(ctx):
    await rpg.rpgmain.openinventory(
        user=rpg.vars.User,
        user_name=rpg.vars.User_name,
        user_rpg=rpg.vars.User_rpg,
        ctx=ctx,
    )


@bot.command()
async def RPG_map(ctx):
    await rpg.rpgmain.worldtravel(
        user=rpg.vars.User,
        user_name=rpg.vars.User_name,
        user_rpg=rpg.rpg_db.get_rpg_db(user_id=ctx.author.id),
        ctx=ctx,
    )


@bot.slash_command(guild_ids=GUILD_IDS)
async def mark(
    interaction: Interaction,
    mark: float = SlashOption(
        required=True,
        min_value=1.0,
        max_value=10.0,
        description="Jouw cijfer",
        name="mark",
    ),
    subject=SlashOption(
        required=True, choices=mark_choices, description="Het vak", name="subject"
    ),
    type=SlashOption(
        required=False, choices=mark_se_choices, description="Type punt", name="type"
    ),
):
    await edu.mark(
        user=interaction.user.id,
        mark=mark,
        type=type,
        subject=subject,
        interaction=interaction,
    )


@bot.slash_command(guild_ids=GUILD_IDS)
async def average(
    interaction: Interaction,
    subject: str = SlashOption(
        choices=mark_choices,
        description="Het vak waar je het gemmiddelde van wilt, leeg geeft het gemiddelde van alles",
        required=True,
        name="subject",
    ),
):
    await edu.average(interaction=interaction, subject=subject)


@bot.slash_command(guild_ids=GUILD_IDS)
async def showmark(
    interaction: Interaction,
    allmarks: bool = SlashOption(
        description="Wil je alle cijfers laten zien?", required=True, name="allmarks"
    ),
    subject: str = SlashOption(
        choices=mark_choices,
        description="Voor welk vak je je punten wil zien",
        required=False,
        name="subject",
    ),
):
    pass


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
