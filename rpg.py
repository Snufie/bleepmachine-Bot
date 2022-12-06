import nextcord
from nextcord import Interaction, Member
from nextcord.application_command import SlashOption
from nextcord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import database_functions
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

try:
    from PIL import Image
except ImportError:
    pass

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
    "miles_travelled": 0,
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


def prepare_map():
    map = Image.open("map2.png")
    gridLineWidth = 100
    fig = plt.figure(
        figsize=(
            float(map.size[1]) / gridLineWidth,
            float(map.size[0]) / gridLineWidth,
        ),
        dpi=gridLineWidth,
    )
    axes = fig.add_subplot(111)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    gridInterval = 50.0
    gridIntervalx = 50.0
    location = plticker.MultipleLocator(base=gridInterval)
    locationx = plticker.MultipleLocator(base=gridIntervalx)
    axes.xaxis.set_major_locator(locationx)
    axes.yaxis.set_major_locator(location)
    axes.grid(which="both", axis="both", linestyle="-", color="k")
    axes.imshow(map)
    fig.savefig("map.png", dpi=gridLineWidth)


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
            userrpg=user_rpg,
            user=user_id1,
            user_name=user_name,
            interact=ctx,
        )


class vars:
    Ctx = None
    User = None
    User_rpg = None
    User_name = None


class rpgsetup:
    async def start(self, userrpg, user, user_name, interact) -> None:
        vars.Ctx = interact
        vars.User = user
        vars.User_rpg = userrpg
        vars.User_name = user_name
        print(vars.Ctx, vars.User, vars.User_name, vars.User_rpg)
        user_rpg_db = client.get_database(str(interact.author.id))
        user_rpg_coll = user_rpg_db.get_collection("rpg")
        if user_rpg_coll.count_documents({}) < 2:
            user_rpg_coll.insert_one(
                {"name": "rpg_vars", "user_rpg": vars.User_rpg, "user": vars.User}
            )
        elif user_rpg_coll.count_documents({}) == 2:
            user_rpg_coll.find_one_and_update(
                {"name": "rpg_vars"},
                {"$set": {"user_rpg": vars.User_rpg}, "$set": {"user": vars.User}},
            )
        await rpgmain.intro(
            user=vars.User,
            user_name=vars.User_name,
            user_rpg=vars.User_rpg,
            ctx=vars.Ctx,
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

    async def openinventory(user, user_name, user_rpg, ctx):
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
        await thread.send(embed=rpg_inv_embed)

    async def worldtravel(user, user_name, user_rpg, ctx):
        location = user_rpg.get("current_location")
        channel: nextcord.TextChannel = nextcord.utils.get(
            ctx.guild.channels, name="rpg"
        )
        user_name_thread = str(user_name).replace("#", "")
        thread = nextcord.utils.get(channel.threads, name=f"{user_name_thread}'s RPG")
        prepare_map()
        await thread.send(file=nextcord.File("map.png"))


class rpg_db:
    def get_rpg_db(user_id):
        user_rpg_db = client.get_database(str(user_id))
        user_rpg_coll = user_rpg_db.get_collection("rpg")
        user_rpg_doc = user_rpg_coll.find_one({"name": "playerstats"})
        return user_rpg_doc
