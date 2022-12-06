import nextcord
from nextcord import Interaction, Member
from nextcord.application_command import SlashOption
from nextcord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import database_functions

# Variables:
userinfracs = {}
bad_words = ("kkr", "kanker", "kk", "nigger", "neger", "nigr", "negr", "nigga", "nig")
GUILD_IDS = (1039988764925251614,)
load_dotenv()

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="|", intents=intents)

# Code:
async def badwords(message, infrac, author_id):
    database_functions.infractions(user_id=author_id, type="addW", infrac=infrac)
    embedr = nextcord.Embed(
        color=nextcord.Color.brand_red(),
        title="Woah! Rustig aan joh!",
        description="Dat woord wordt niet getolereerd, het bericht is verwijderd en je hebt een waarschuwing gekregen.",
    )
    await message.reply(embed=embedr)


async def clearinfracs(user, user_name, interaction):
    database_functions.infractions(user_id=user, type="removeW", infrac=all)
    embedr = nextcord.Embed(
        color=nextcord.Color.blurple(),
        title=f"Alle overtredingen van {user_name} zijn verwijderd!",
        description="Tip: je aan de regels houden werkt echt!",
    )
    await interaction.response.send_message(embed=embedr)
