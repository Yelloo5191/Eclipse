import discord
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()


intents = discord.Intents.all()
intents.message_content = True


PREFIX = os.getenv("PREFIX")
TOKEN = os.getenv('TOKEN')
owners = [304024578009595907, 219323433719300105]
guilds = [837808972902957128, 996816323013259365, 982118812805636136]
client = commands.Bot(intents=intents, owner_ids=set(
    owners), case_insensitive=True, command_prefix=commands.when_mentioned_or(PREFIX), debug_guilds=guilds)

print('------')
for filename in os.listdir('./utils/cogs'):
    if filename.endswith('.py'):
        print(f'Loading utils.cogs.{filename[:-3]}...')
        client.load_extension(f'utils.cogs.{filename[:-3]}')
        print(f'Loaded utils.cogs.{filename[:-3]}')
print('------')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     await client.process_commands(message)


@client.command()
async def ping(ctx):
    embed = discord.Embed(
        title="Ping!", description=f"{ctx.author.mention} pong!")
    embed.add_field(name="Ping", value=f"{round(client.latency * 1000)}ms")
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="Bot Latency")
    await ctx.send(embed=embed)
    await ctx.guild.create_role(name="white", color=discord.Color(0xFFFFFF))

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client.run(TOKEN)
