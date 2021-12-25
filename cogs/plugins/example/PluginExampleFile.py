import discord
from discord.ext import commands

class PluginExample(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def what(self, ctx):
        await ctx.send("I'm an example")

    def hello(self):
        print("Successfully called!")

def setup(client):
    client.add_cog(PluginExample(client))

def teardown(client):
    client.remove_cog('PluginExample')
