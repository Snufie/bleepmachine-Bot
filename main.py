import nextcord
from nextcord import Interaction, Member
from nextcord.application_command import SlashOption
from nextcord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Variables

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

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

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
    welcome_channel = nextcord.utils.get(guild.channels, name="welcome")
    if welcome_channel is None:
        print('No channel named "welcome" found')
        return

    await welcome_channel.send(f"Welkom in {guild.name} {member.mention}!")


@bot.command(aliases=["pong"])
async def ping(ctx):
    await ctx.reply(f"Pong!\nLatentie: {round(bot.latency * 1000)}ms")


@bot.command()
async def deez(ctx):
    await ctx.reply("NUTS!!!")


@bot.slash_command(guild_ids=GUILD_IDS)
async def mark(
    interaction: Interaction,
    mark: float = SlashOption(
        required=True, min_value=1.0, max_value=10.0, description="Jouw cijfer"
    ),
    subject=SlashOption(
        required=True,
        choices=mark_choices,
        description="Het vak",
    ),
):
    """Voer je punt in"""
    print("beans")

    await interaction.response.send_message(
        f"{interaction.user.mention} heeft een {mark} gehaald voor {subject}!"
    )


@bot.slash_command(guild_ids=GUILD_IDS)
async def slash(interaction: Interaction):
    """Epic"""
    await interaction.response.send_message("Slash Command!")


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
