import discord
from discord.ext import commands
from .Functions import *
import os
from .plugins import codeforce

subfile_dir =  "cogs/plugins/codeforce"

print(codeforce.user_info_handle('umaruto'))

class Codeforce(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group()
    async def cf(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Do b!cf help for list of commands for codeforce feature")

    @cf.group()
    async def help(self, ctx):
        await ctx.send("do b!cf handle")

    @cf.group()
    async def handle(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("handle register (hande_name)")

    @handle.group()
    async def register(self, ctx, *, handle_name):
        print(handle_name)
        handle = codeforce.Handle()
        if handle is not None:
            await handle.register_user(ctx, handle_name)

    @handle.group()
    async def remove(self, ctx, *, handle_name):
        #handle = self.client.get_cog("HandleCodeforce")
        handle = codeforce.Handle()
        if handle is not None:
            await handle.remove_user(ctx, handle_name)



def setup(client):
    load_dir(client, subfile_dir)
    client.add_cog(Codeforce(client))

def teardown(client):
    unload_dir(client, subfile_dir)
    cleint.remove_cog("Codeforce")
