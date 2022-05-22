import requests
import discord
from discord.ext import commands
import mysql.connector
from .CodeforceDbFunctions import CodeforceDbConn

# can be optimized
def user_info_handle(handle_name):
    req = requests.get("https://codeforces.com/api/user.info?handles={}".format(handle_name))
    res = req.json()
    return res


class Handle:
    def __init__ (self):
        self.user_db = CodeforceDbConn()

    async def register_user(self, ctx, handle_name):
        print(handle_name)
        if self.user_db.get_user_id(ctx.message.author.id):
            await ctx.send("You're already in the database!")
            return None
        
        if self.user_db.get_handle(handle_name):
            await ctx.send("Handle already exist in database!")
            return None
        
        res = user_info_handle(handle_name)
        if res['status'] == 'FAILED':
            print("FAILED")
            await ctx.send(res['comment'])
        else:
            fields = ['user_id', 'guild_id', 'handle']
            values = (ctx.message.author.id, ctx.message.guild.id, handle_name)
            self.user_db.insert('user_handle', fields, values)
            await ctx.send("Bergasil didaftarkan!")

    async def remove_user(self, ctx, handle_name):
        user = self.user_db.get_handle(handle_name)
        if user:
            user_id = ctx.message.author.id
            print(type(user_id))
            print(type(user['user_id']))
            if user['user_id'] == user_id:
                self.user_db.remove_handle(handle_name)
                await ctx.send("Successfully removed!")
            else:
                await ctx.send("The user you're trying to remove is not yours!")
        else:
            await ctx.send("User doesn't exist in database!")
                


def setup(client):
    client.add_cog(HandleCodeforce(client))
    pass

def teardown(client):
    client.remove_cog("HandleCodeforce")
    pass

    
