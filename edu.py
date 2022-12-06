import nextcord
from nextcord import Interaction, Member
from nextcord.application_command import SlashOption
from nextcord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import database_functions

# Variables:
returnable = None
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

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True

GUILD_IDS = (1039988764925251614,)
bot = commands.Bot(command_prefix="|", intents=intents)
load_dotenv()

# Code:


async def mark(user, mark, type, subject, interaction):
    database_functions.add_punt(
        user_id=int(user),
        punt=mark,
        vak=subject,
        type=type,
    )
    channel = nextcord.utils.get(interaction.guild.channels, name="punte")
    await interaction.response.send_message(
        f"{interaction.user.mention} heeft een {mark} gehaald voor {subject}!"
    )
    return


async def average(interaction, subject):
    avgvalue = database_functions.get_avg(user_id=interaction.user.id, vak=subject)
    if avgvalue == None:
        await interaction.response.send_message(
            f"Je hebt nog geen punt voor {subject}",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            f"{interaction.user.mention}. Je staat een {avgvalue} gemiddeld voor {subject}"
        )
