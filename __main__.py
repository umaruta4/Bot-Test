import discord
import os
from discord.ext import commands
import sys

TOKEN = sys.argv[1]
client = commands.Bot(command_prefix='b!')

def is_owner(ctx):
    return ctx.author.id == 245879813816975360

@client.event
async def on_ready():
    print("I'm Ready!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found!")
    print(error)


@client.command()
@commands.check(is_owner)
async def load(ctx, extension):
    client.load_extension('cogs.{}'.format(extension))

@client.command()
@commands.check(is_owner)
async def unload(ctx,extension):
    client.unload_extension('cogs.{}'.format(extension))

@client.command()
@commands.check(is_owner)
async def load_pack(ctx, extension):
    for filename in os.listdir('./cogs/{}'.format(extension)):
        if filename.endswith('.py'):
            client.load_extension('cogs.{}.{}'.format(extension,filename[:-3]))

@client.command()
@commands.check(is_owner)
async def unload_pack(ctx,*, extension):
    ex = extension.split(' ')
    _dir = '/'.join(ex)
    path = '.'.join(ex)
    for filename in os.listdir('./cogs/{}'.format(_dir)):
        if filename.endswith('.py'):
            client.unload_extension('cogs.{}.{}'.format(path,filename[:-3]))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension('cogs.{}'.format(filename[:-3]))

client.run(TOKEN)
