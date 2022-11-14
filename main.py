# This example requires the 'members' privileged intents

import nextcord
from nextcord import Interaction, Member
from nextcord.application_command import SlashOption
from nextcord.ext import commands
from dotenv import load_dotenv
import os
from typing import List

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
]

# Code

load_dotenv()

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

GUILD_IDS = os.getenv("GUILD_IDS")

bot = commands.Bot(command_prefix="|", intents=intents)


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

    await welcome_channel.send(f"Welcome to {guild.name} {member.mention}!")


@bot.command(aliases=["pong"])
async def ping(ctx):
    await ctx.reply(f"Pong!\nLatency: {round(bot.latency * 1000)}ms")


@bot.command()
async def deez(ctx):
    await ctx.reply("NUTS!!!")


@bot.slash_command(guild_ids=GUILD_IDS)
async def mark(
    interaction: Interaction,
    mark: float = SlashOption(required=True, description="Your mark"),
    subject=SlashOption(
        required=True,
        choices=mark_choices,
        description="The subject",
    ),
):
    """Enter your mark"""
    await interaction.response.send_message(f"Y {mark} for {subject}")


@bot.slash_command(guild_ids=GUILD_IDS)
async def slash(interaction: Interaction):
    """Epic"""
    await interaction.response.send_message("Slash Command!")


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
