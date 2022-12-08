import nextcord
from nextcord import Interaction, Member
from nextcord.application_command import SlashOption
from nextcord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import database_functions

# Variables:

ranks = {
    "1": "Rookie",
    "2": "Nomad",
    "3": "Explorer",
    "4": "Adventurer",
    "5": "Journeyman",
    "6": "Mercenary",
    "7": "Raider",
    "8": "Hero",
    "9": "Legendary",
    "10": "Mythical",
    "11": "Dragon Lord",
}


base_coll = {
    "name": "playerstats",
    "health": 100,
    "level": 0,
    "xp": 0,
    "xp_to_next_level": 10,
    "coins": 0,
    "melee": "Wooden Sword",
    "ranged": "Slingshot",
    "mount": "Mule",
    "current_location": "Newvault",
    "rank": ranks.get("1"),
}

# world_map = img.imread("./img/map.png")

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True

GUILD_IDS = (1039988764925251614,)
bot = commands.Bot(command_prefix="|", intents=intents)

try:
    client = MongoClient(os.getenv("MONGO_URL"))
except ConnectionFailure:
    print("Failed to connect to MongoDB")
    exit()

# Code:


class fasttravel(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Travel to..", style=nextcord.ButtonStyle.grey)
    async def settraveldest(self, button: nextcord.ui.Button, interaction=Interaction):
        await rpgmain.setdestination(ctx=interaction)
        self.value = True


async def rpg(ctx, base):
    user_id = str(ctx.author.id)
    user_id1 = ctx.author.id
    # print(user_id1)
    user_name = ctx.author
    # print(user_id)
    if not str(user_id) in client.list_database_names():
        user_rpg_db = database_functions.add_user_db(user_id)
        user_rpg_coll = user_rpg_db.get_collection("rpg")
        await ctx.send("Run the command again, your database was just created!")
    else:
        user_rpg_db = client.get_database(user_id)
        user_rpg_coll = user_rpg_db.get_collection("rpg")
        if "rpg" not in user_rpg_db.list_collection_names():
            user_rpg_coll = user_rpg_db.create_collection("rpg")
            await ctx.send("Created a new save!")
            user_rpg = user_rpg_coll.insert_one(base)
            await ctx.reply("Your save is set up!")
        elif user_rpg_coll.count_documents({}) == 0:
            user_rpg = user_rpg_coll.insert_one(base)
            await ctx.reply("Your save is created!")
        elif (
            user_rpg_coll.count_documents({}) == 2
            or user_rpg_coll.count_documents({}) == 1
        ):
            await ctx.reply("Fetching your data...")
            user_rpg = user_rpg_coll.find_one({"name": "playerstats"})
            # print(user_rpg)

        await rpgsetup.start(
            self=rpgsetup,
            interact=ctx,
        )


class rpgsetup:
    async def start(self, interact) -> None:
        user_rpg_db = client.get_database(str(interact.author.id))
        user_rpg_coll = user_rpg_db.get_collection("rpg")
        await rpgmain.intro(
            user=interact.author.id,
            user_name=interact.author,
            user_rpg=user_rpg_coll.find_one({"name": "playerstats"}),
            ctx=interact,
        )


class rpgmain:
    async def intro(user, user_name, user_rpg, ctx):
        channel: nextcord.TextChannel = nextcord.utils.get(
            ctx.guild.channels, name="rpg"
        )
        await channel.send("Starting session...")
        user_name_thread = str(user_name).replace("#", "")
        thread = nextcord.utils.get(channel.threads, name=f"{user_name_thread}'s RPG")
        # print(thread)
        # print(channel.threads)
        # print(user_name_thread)
        if thread == None:
            thread = await channel.create_thread(
                name=f"{user_name}'s RPG",
            )
            # print(thread)
            # print(channel.threads)
        await thread.send(f"{ctx.author.mention}")
        rpg_inv_embed = nextcord.Embed(
            color=nextcord.Color.teal(),
            title=f"**{user_name}'s inventory**",
            description="Your inventory",
        )
        rpg_inv_embed.add_field(
            name="Health:", value=user_rpg.get("health"), inline=True
        )
        rpg_inv_embed.add_field(name="Level:", value=user_rpg.get("level"), inline=True)
        rpg_inv_embed.add_field(name="Coins:", value=user_rpg.get("coins"), inline=True)
        rpg_inv_embed.add_field(name="XP:", value=user_rpg.get("xp"), inline=True)
        rpg_inv_embed.add_field(
            name="XP to level up:", value=user_rpg.get("xp_to_next_level"), inline=True
        )
        rpg_inv_embed.add_field(
            name="Melee Weapon:", value=user_rpg.get("melee"), inline=True
        )
        rpg_inv_embed.add_field(
            name="Ranged Weapon:", value=user_rpg.get("ranged"), inline=True
        )
        rpg_inv_embed.add_field(name="Mount:", value=user_rpg.get("mount"), inline=True)
        await thread.send(embed=rpg_inv_embed)
        await thread.send(
            "From now on you can use the RPG commands in this thread! You don't need to use |RPG again unless the thread becomes inactive."
        )

    async def openinventory(ctx):
        user = ctx.author.id
        user_name = ctx.author
        user_r = client.get_database(str(user))
        user_rp = user_r.get_collection("rpg")
        user_rpg = user_rp.find_one({"name": "playerstats"})
        channel: nextcord.TextChannel = nextcord.utils.get(
            ctx.guild.channels, name="rpg"
        )
        user_name_thread = str(user_name).replace("#", "")
        thread = nextcord.utils.get(channel.threads, name=f"{user_name_thread}'s RPG")
        rpg_inv_embed = nextcord.Embed(
            color=nextcord.Color.teal(),
            title=f"**{user_name}'s inventory**",
            description="Your inventory",
        )
        rpg_inv_embed.add_field(
            name="Health:", value=user_rpg.get("health"), inline=True
        )
        rpg_inv_embed.add_field(name="Level:", value=user_rpg.get("level"), inline=True)
        rpg_inv_embed.add_field(name="Coins:", value=user_rpg.get("coins"), inline=True)
        rpg_inv_embed.add_field(name="XP:", value=user_rpg.get("xp"), inline=True)
        rpg_inv_embed.add_field(
            name="XP to level up:", value=user_rpg.get("xp_to_next_level"), inline=True
        )
        rpg_inv_embed.add_field(
            name="Melee Weapon:", value=user_rpg.get("melee"), inline=True
        )
        rpg_inv_embed.add_field(
            name="Ranged Weapon:", value=user_rpg.get("ranged"), inline=True
        )
        rpg_inv_embed.add_field(name="Mount:", value=user_rpg.get("mount"), inline=True)
        await thread.send(embed=rpg_inv_embed)

    async def worldtravel(ctx):
        user = ctx.author.id
        user_name = ctx.author
        user_r = client.get_database(str(user))
        user_rp = user_r.get_collection("rpg")
        user_rpg = user_rp.find_one({"name": "playerstats"})
        location = user_rpg.get("current_location")
        channel: nextcord.TextChannel = nextcord.utils.get(
            ctx.guild.channels, name="rpg"
        )
        user_name_thread = str(user_name).replace("#", "")
        thread = nextcord.utils.get(channel.threads, name=f"{user_name_thread}'s RPG")
        view = fasttravel()
        await thread.send(file=nextcord.File(f"img/map_{location}.png"), view=view)
        await view.wait()

    async def setdestination(ctx):
        locations_db = client.get_database("RPG")
        locations_coll = locations_db.get_collection("locations")
        rpg_locations = locations_coll.find_one({"_id": "Kingdom of Mospelia"})
        print(rpg_locations)
        print(rpg_locations["cities"]["rich"])
        rpg_citydesc = locations_coll.find_one({"_id": "mospelia_citydesc"})
        embedr = nextcord.Embed(
            color=nextcord.Color.brand_green(),
            title="**Set your travel destination**",
            description="Check the following destinations and choose yours.",
        )
        embedr.add_field(
            name=rpg_locations["cities"]["capital"],
            value=rpg_citydesc[(str(rpg_locations["cities"]["capital"]).lower())],
        )
        embedr.add_field(
            name=rpg_locations["cities"]["rich"],
            value=rpg_citydesc[(str(rpg_locations["cities"]["rich"]).lower())],
        )
        embedr.add_field(
            name=rpg_locations["cities"]["trade_port"],
            value=rpg_citydesc[(str(rpg_locations["cities"]["trade_port"]).lower())],
        )
        embedr.add_field(
            name=rpg_locations["cities"]["religion"],
            value=rpg_citydesc[(str(rpg_locations["cities"]["religion"]).lower())],
        )
        embedr.add_field(
            name=rpg_locations["cities"]["generic1"],
            value=rpg_citydesc[(str(rpg_locations["cities"]["generic1"]).lower())],
        )
        embedr.add_field(
            name=rpg_locations["cities"]["generic2"],
            value=rpg_citydesc[(str(rpg_locations["cities"]["generic2"]).lower())],
        )
        embedr.add_field(
            name=rpg_locations["cities"]["generic3"],
            value=rpg_citydesc[(str(rpg_locations["cities"]["generic3"]).lower())],
        )
        await ctx.response.send_message(embed=embedr)
