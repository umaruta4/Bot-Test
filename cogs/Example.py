import discord
from discord.ext import commands
import os

# name of the feature
class Example(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # prefix for example feature
    @commands.group()
    async def ex(self, ctx):
        """ Just an example """
        if ctx.invoked_subcommand is None:
            await ctx.send("Do 'b!ex help'")

    # subcommand for ex prefix
    @ex.group()
    async def help(self, ctx):
        plugin_example = self.client.get_cog('PluginExample')
        if plugin_example is not None:
            plugin_example.hello()
            await plugin_example.what(ctx)

# called when this file is loaded
def setup(client):
    # load all plugins inside example folder
    for filename in os.listdir('./cogs/plugins/example'):
        if filename.endswith('.py'):
            client.load_extension('cogs.plugins.example.{}'.format(filename[:-3]))
    
    client.add_cog(Example(client))

# called when this file is unloaded
def teardown(client):
    # unload all plugins inside example folder
    for filename in os.listdir('./cogs/plugins/example'):
        if filename.endswith('.py'):
            client.unload_extension('cogs.plugins.example.{}'.format(filename[:-3]))

    client.remove_cog('Example')
