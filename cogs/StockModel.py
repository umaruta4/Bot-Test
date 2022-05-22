import math
import random
import matplotlib.pyplot as plt
import json
import time

import discord
from discord.ext import commands
import asyncio

from PIL import Image


DATA_DIR = "./cogs/data/stockmodel/"
GAMEDATA_DIR = DATA_DIR + "gamedata.json"
LETTER_TO_NUMBER = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5}


def friendly_name(string):
    return string.replace(" ", "").lower()

def tag_user(user_id):
    return '<@!' + str(user_id) + '>'

def percent_compare(curr, prev):
    if prev == 0:
        return (":question:", 0)
    if curr < prev:
        symbol = ":small_red_triangle_down:"
        percent = round(100 * ( prev - curr ) / prev, 1)
    else:
        symbol = ":arrow_up:"
        percent = round(100 * ( curr - prev ) / prev, 1)
    return (symbol, percent)

# hardcoded, no reason to unhardcode: TRENDS_SHIFT_RATE = 0.1
# to un-hardcode, replace /10 with *TRENDS_SHIFT_RATE

def first_time():

    with open(GAMEDATA_DIR, 'r') as f:
        gamedata = json.load(f)
        
    a_stock = {"name": "a",
               "value": 1000,
               "trends": 0,
               "upwards": 1,
               "extremity": 11,
               "history": []}

    b_stock = {"name": "b",
               "value": 1000,
               "trends": 0,
               "upwards": 1,
               "extremity": 11,
               "history": []}

    c_stock = {"name": "c",
               "value": 1000,
               "trends": 0,
               "upwards": 1,
               "extremity": 11,
               "history": []}

    d_stock = {"name": "d",
               "value": 1000,
               "trends": 0,
               "upwards": 1,
               "extremity": 11,
               "history": []}

    e_stock = {"name": "e",
               "value": 1000,
               "trends": 0,
               "upwards": 1,
               "extremity": 11,
               "history": []}

    f_stock = {"name": "f",
               "value": 1000,
               "trends": 0,
               "upwards": 1,
               "extremity": 11,
               "history": []}

    system = {}
    system["stocks"] = [a_stock, b_stock, c_stock, d_stock, e_stock, f_stock]
    system["current_time"] = time.time()
    system["current_tick"] = 0

    gamedata = {"system": system}

    with open(GAMEDATA_DIR, 'w') as f:
        json.dump(gamedata, f)


DICTIONARY = {"default": {"a": "A KOIN", "b": "B KOIN", "c": "C KOIN", "d": "D KOIN", "e": "E KOIN", "f": "F KOIN"},
              "funck": {"a": "AYUKOIN", "b": "COWKOIN", "c": "FONKOIN", "d": "MOFKOIN", "e": "SCTKOIN", "f": "YUUKOIN"}
              }

INTERPRETATOR = {"funck": {"ayu": "a", "cow": "b", "fon": "c", "mof": "d", "sct": "e", "yuu": "f",
                           "a": "a", "c": "b", "f": "c", "m": "d", "s": "e", "y": "f",
                           "ayukoin": "a", "cowkoin": "b", "fonkoin": "c", "mofkoin": "d", "sctkoin": "e", "yuukoin": "f",
                           "ayucoin": "a", "cowcoin": "b", "foncoin": "c", "mofcoin": "d", "sctcoin": "e", "yuucoin": "f",
                           }
                 }

def tick_stock(stock, amount):
    for i in range(amount):
        tick(stock)
    return

def print_stock(stock, stock_name, dictionary_type):
    name = stock["name"]
    history = stock["history"]
    
    timelst = []
    l = - len(history)
    while l < 0:
        l += 1
        timelst.append(l)
        
    plt.plot(timelst, history, color='red', marker='o')
    plt.title(DICTIONARY[dictionary_type][name], fontsize=18)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.grid(True)
    plt.savefig(stock_name)
    plt.clf()
    #plt.show()
    return


def tick(stock):
    MAX_TRENDS = 4.5 # 4.0 # 5 # 4.5

    MULT_PER_TRENDS = 0.11 # 0.13 # 0.1 # 0.11

    EXTREMITY_MIN_SHIFT = 2 # 1 # 2 # 2
    EXTREMITY_MAX_SHIFT = 5 # 4 # 5 # 5

    MIN_EXTREMITY = 5 # 3 # 5 # 5
    MAX_EXTREMITY = 23 # 20 # 25 # 23
    
    value = stock["value"]
    trends = stock["trends"]
    upwards = stock["upwards"]
    extremity = stock["extremity"]

    increment = random.randint(EXTREMITY_MIN_SHIFT, EXTREMITY_MAX_SHIFT)
    if extremity < MIN_EXTREMITY + EXTREMITY_MAX_SHIFT:
        extremity = extremity + increment
    elif extremity > MAX_EXTREMITY - EXTREMITY_MAX_SHIFT:
        extremity = extremity - increment
    else:
        extremity = extremity + increment * random.choice((-1, 1))
    stock["extremity"] = extremity

    trends = trends + random.uniform(0.2, extremity / 10) * upwards
    stock["trends"] = trends

    if trends <= - MAX_TRENDS + MAX_EXTREMITY / 10:
        stock["upwards"] = 1
    elif trends >= MAX_TRENDS - MAX_EXTREMITY / 10:
        stock["upwards"] = -1

    if trends > 0:
        direction = 1
    else:
        direction = -1
    modify_linear = random.uniform(-1, math.fabs(trends)+1) * direction
    modify_mult = 1.01 + math.fabs(modify_linear) * MULT_PER_TRENDS
    if modify_linear > 0:
        value = value * modify_mult
    else:
        value = value / modify_mult
    stock["value"] = value

    history = stock["history"]
    history.append(value)
    if len(history) > 41:
        history.pop(0)
    stock["history"] = history

    # replace to True to debug
    if False:
        if modify_linear > 0:
            print("Value: {}, Trend: {}, Lin: {}, Mult: {}, Extre: {}".format(
                round(value, 2), round(trends, 2), round(modify_linear, 2), round(modify_mult, 3), extremity))
        else:
            print("Value: {}, Trend: {}, Lin: {}, Div: {}, Extre: {}".format(
                round(value, 2), round(trends, 2), round(modify_linear, 2), round(modify_mult, 3), extremity))

    #print("Stock price: {}".format(round(value, 5)))

def tick_system(system):
    current_time = system["current_time"]
    current_tick = system["current_tick"]
    old_tick = current_tick
    
    while current_time < time.time():
        current_time += 90
        current_tick += 1
        for stock in system["stocks"]:
            tick(stock)

    system["current_time"] = current_time
    system["current_tick"] = current_tick
    return current_time - time.time()# time to next update


def force_tick(system, amount):
    for i in range(amount):
        for stock in system["stocks"]:
            tick(stock)
    system["current_tick"] += amount
    return

# generates image as out.png if necessary
def generate_image(system, dictionary_type):
    dir_a = DATA_DIR + "a.png"
    dir_b = DATA_DIR + "b.png"
    dir_c = DATA_DIR + "c.png"
    dir_d = DATA_DIR + "d.png"
    dir_e = DATA_DIR + "e.png"
    dir_f = DATA_DIR + "f.png"
    dir_out = DATA_DIR + "out.png"
    #alphabet = ["a.png", "b.png", "c.png", "d.png", "e.png", "f.png"]
    alphabet = [dir_a, dir_b, dir_c, dir_d, dir_e, dir_f]
    time_to_update = tick_system(system)
    stocks = system["stocks"]
    for i in range(6):
        print_stock(stocks[i], alphabet[i], dictionary_type)

    a = Image.open(dir_a)
    b = Image.open(dir_b)
    c = Image.open(dir_c)
    d = Image.open(dir_d)
    e = Image.open(dir_e)
    f = Image.open(dir_f)
    
    n = Image.new('RGB', (1280,1440))
    n.paste(a, (0, 0))
    n.paste(b, (640, 0))
    n.paste(c, (0, 480))
    n.paste(d, (640, 480))
    n.paste(e, (0, 960))
    n.paste(f, (640, 960))

    n.save(dir_out)
    return time_to_update

with open(GAMEDATA_DIR, 'r') as f:
    data = json.load(f)
    if not data:
        first_time()
    
## async
with open(GAMEDATA_DIR, 'r') as f:
    dummy_gamedata = json.load(f)
    gamedata = {}
    for rubbish in dummy_gamedata:
        if rubbish != "system":
            gamedata[int(rubbish)] = dummy_gamedata[rubbish]
    gamedata["system"] = dummy_gamedata["system"]
    del dummy_gamedata

#force_tick(gamedata["system"], 200)


#########################################################################
############### COMMAND CLASS ###########################################
#########################################################################

class StockModel(commands.Cog):

    @commands.group()
    async def sm(self, ctx):
        if ctx.invoked_subcommand is None:
            self.help(ctx)

    @sm.group()
    async def help(self, ctx):
        txt = "Command List for KOIN game:\n"
        txt += "`!koin` to see available koins\n"
        txt += "`!bal` to check your balance\n"
        txt += "`!bal @someone` to check someone else's balance\n"
        txt += "`!buy d 15000` to spend $15000 to buy D KOIN\n"
        txt += "`!sell d` to sell all of your D KOIN\n"
        txt += "`!sell d 1.75` to sell 1.75 D KOIN\n"
        await ctx.send(txt)

    @sm.group()
    async def register(self, ctx, *args):
        user_id = ctx.message.author.id
        
        if user_id in gamedata:
            await ctx.send("Could not register: {} is already registered.".format(gamedata[user_id]["name"]))
            
        else:
            d = {}
            d['name'] = ctx.message.author.name
            d['money'] = 100000
            d['stocks'] = {}
            d['stocks']['a'] = 0
            d['stocks']['b'] = 0
            d['stocks']['c'] = 0
            d['stocks']['d'] = 0
            d['stocks']['e'] = 0
            d['stocks']['f'] = 0
            d['lastworth'] = {}
            d['lastworth']['a'] = 0
            d['lastworth']['b'] = 0
            d['lastworth']['c'] = 0
            d['lastworth']['d'] = 0
            d['lastworth']['e'] = 0
            d['lastworth']['f'] = 0
            d['lastseen'] = {}
            d['lastseen']['a'] = 1000
            d['lastseen']['b'] = 1000
            d['lastseen']['c'] = 1000
            d['lastseen']['d'] = 1000
            d['lastseen']['e'] = 1000
            d['lastseen']['f'] = 1000
            d['dictionary_type'] = 'default'
            gamedata[user_id] = d
            txt = 'You have successfully registered! You have $100000.\n'
            txt += '`!koin` to see available koins\n'
            txt += "`!bal` to check your (or someone else's) balance\n"
            txt += "`!buy d 15000` to spend $15000 to buy D KOIN\n"
            txt += "`!sell d` to sell all of your D KOIN\n"
            txt += "`!sell d 1.75` to sell 1.75 D KOIN\n"
            # txt += '`$changename (name)` to change your name.\n'+'Your current name is {}'.format(d['name'])
            await ctx.send(txt)

    @sm.group()
    async def koin(self, ctx, *args):
        user_id = ctx.message.author.id
        if user_id not in gamedata:
            await ctx.send('You need to register first with `!register`')
            return
        user_dict = gamedata[user_id]
        dictionary_type = user_dict["dictionary_type"]
        system = gamedata["system"]
        time_to_update = generate_image(system, dictionary_type)
        txt = "Prices will update in {} seconds\n".format(round(time_to_update, 1))
        for stock in system["stocks"]:
            initial = stock["name"]
            stock_name = DICTIONARY[dictionary_type][initial]
            value = stock["value"]
            lastseen = user_dict['lastseen'][initial]
            symbol, percent = percent_compare(value, lastseen)
            txt += "{} {} {} {}% ({})\n".format(stock_name, value, symbol, percent, round(lastseen, 1))
            user_dict['lastseen'][initial] = value
        
        await ctx.send(file=discord.File(DATA_DIR + "out.png"))
        await ctx.send(txt[:-1])


    @sm.group()
    async def bal(self, ctx, *args):
        user_id = ctx.message.author.id
        if user_id not in gamedata:
            await ctx.send('You need to register first with `!register`')
            return
        if len(args) == 0:
            to_check = user_id
        else:
            arg = 3 if args[0][2] == '!' else 2
            try:
                to_check = int(args[0][arg:-1])
            except:
                txt = "Integer Error: You need to tag someone check their balance, or just do `!bal` to check your own."
                await ctx.send(txt)
                return
        if to_check not in gamedata:
            txt = "Invalid input: A valid discord ID was interpreted but they are not registered.\n"
            txt += "If you attempted to tag a person, you can ask them to `!register`"
            await ctx.send(txt)
            return
        system = gamedata["system"]
        tick_system(system)
        user_dict = gamedata[to_check]
        dictionary_type = user_dict["dictionary_type"]
        networth = user_dict["money"]
        txt = "Balance of {}: ${}\n".format(user_dict["name"], networth)
        stocks = system["stocks"]
        convertdict = DICTIONARY[dictionary_type]
        i = 0
        for letter in ('a', 'b', 'c', 'd', 'e', 'f'):
            stock_name = convertdict[letter]
            stock_amount = user_dict['stocks'][letter]
            lastworth = user_dict['lastworth'][letter]
            exchange_rate = stocks[i]["value"]
            i += 1
            worth = exchange_rate * stock_amount
            symbol, percent = percent_compare(worth, lastworth)
            txt += "{} {} (Worth ${}) {} {}%\n".format(stock_name, stock_amount, round(worth, 1), symbol, percent)
            networth += worth
        txt += "Total net worth: ${}".format(networth)
        await ctx.send(txt)

    @sm.group()
    async def funck(self, ctx, *args):
        user_id = ctx.message.author.id
        if user_id not in gamedata:
            await ctx.send('You need to register first with `!register`')
            return
        user_dict = gamedata[user_id]
        user_dict["dictionary_type"] = "funck"
        await ctx.send("youre now funck")

    @sm.group()
    async def unfunck(self, ctx, *args):
        user_id = ctx.message.author.id
        if user_id not in gamedata:
            await ctx.send('You need to register first with `!register`')
            return
        user_dict = gamedata[user_id]
        user_dict["dictionary_type"] = "default"
        await ctx.send("youre now not funck anymore \:(")


    async def buy_error(self, ctx, money, additional_error=""):
        txt = additional_error
        txt += "You have ${}\n".format(round(user_dict["money"], 2))
        txt += "Example usage: `!buy d 15000` to spend $15000 to buy D KOIN\n"
        await ctx.send(txt)

    @sm.group()
    async def buy(self, ctx, *args):
        user_id = ctx.message.author.id
        if user_id not in gamedata:
            await ctx.send('You need to register first with `!register`')
            return
        user_dict = gamedata[user_id]
        if len(args) != 2:
            await self.buy_error(ctx, user_dict["money"])
            return
        dictionary_type = user_dict["dictionary_type"]
        stock_name = args[0]
        try:
            amount = float(args[1])
        except:
            await self.buy_error(ctx, user_dict["money"],
                            "You have entered an invalid amount of money.\n")
            return
        if dictionary_type == "default":
            try:
                initial = stock_name[0].lower()
            except:
                await self.buy_error(ctx, user_dict["money"],
                                "You did not enter a koin name.\n")
                return
            if initial not in LETTER_TO_NUMBER:
                await self.buy_error(ctx, user_dict["money"],
                                "You did not enter the correct koin name a-f.\n")
                return
        else:
            if friendly_name(stock_name) not in INTERPRETATOR[dictionary_type]:
                await self.buy_error(ctx, user_dict["money"],
                                "You did not enter the correct koin name. Do `!koin` to see the koin names.\n")
                return
            initial = INTERPRETATOR[dictionary_type][friendly_name(stock_name)]
        stock_name = DICTIONARY[dictionary_type][initial]
        if user_dict["money"] < amount:
            await ctx.send("Not enough money: You only have ${} and cannot buy ${} worth of {}.".format(user_dict["money"], amount, stock_name))
            return
        # finally error checks complete lol
        tick_system(gamedata["system"])
        exchange_rate = gamedata["system"]["stocks"][LETTER_TO_NUMBER[initial]]["value"]
        stock_amount = amount / exchange_rate
        user_dict['stocks'][initial] += stock_amount
        user_dict['lastworth'][initial] += amount
        user_dict['money'] -= amount
        ret = "You have bought {} {} for ${}.\n".format(stock_amount, stock_name, amount)
        ret += "Exchange rate: ${} for 1 {}.\n".format(exchange_rate, stock_name)
        ret += "Now you have ${}.".format(user_dict["money"])
        await ctx.send(ret)
    '''
    @client.command(pass_context=True)
    async def forcetick(ctx, *args):
        user_id = ctx.message.author.id
        if user_id not in gamedata:
            await ctx.send('You need to register first with `!register`')
            return
        try:
            amount = int(args[0])
        except:
            await ctx.send('You need to input a number')
            return
        if amount > 200:
            await ctx.send('Max 200 please')
            return
        force_tick(gamedata['system'], amount)
        await ctx.send("You have force ticked {} times".format(amount))
        #await koin(ctx)
    '''
    async def sell_error(self, ctx, additional_error=""):
        txt = additional_error
        txt += "Do `!inv` to see your KOIN. Example usage:\n"
        txt += "`!sell d` to sell all of your D KOIN\n"
        txt += "`!sell d 1.75` to sell 1.75 D KOIN\n"
        await ctx.send(txt)

    @sm.group()
    async def sell(self, ctx, *args):
        user_id = ctx.message.author.id
        if user_id not in gamedata:
            await ctx.send('You need to register first with `!register`')
            return
        user_dict = gamedata[user_id]
        if len(args) not in (1, 2):
            await self.sell_error(ctx)
            return
        dictionary_type = user_dict["dictionary_type"]
        stock_name = args[0]
        if len(args) == 2:
            try:
                amount = float(args[1])
            except:
                await self.sell_error(ctx,
                                 "You have entered an invalid amount.\n")
                return
        if dictionary_type == "default":
            try:
                initial = stock_name[0].lower()
            except:
                await self.sell_error(ctx, 
                                 "You did not enter a koin name.\n")
                return
            if initial not in LETTER_TO_NUMBER:
                await self.sell_error(ctx, 
                                 "You did not enter the correct koin name a-f.\n")
                return
        else:
            if friendly_name(stock_name) not in INTERPRETATOR[dictionary_type]:
                await self.sell_error(ctx, 
                                 "You did not enter the correct koin name. Do `!koin` to see the koin names.\n")
                return
            initial = INTERPRETATOR[dictionary_type][friendly_name(stock_name)]
        stock_name = DICTIONARY[dictionary_type][initial]
        user_have_amount = user_dict["stocks"][initial]
        if len(args) == 1:
            amount = user_have_amount
        if user_have_amount < amount:
            await ctx.send("Not enough {}: You only have {} {} and cannot sell {} {}.".format(stock_name, user_have_amount, stock_name, amount, stock_name))
            return
        # finally error checks complete lol
        tick_system(gamedata["system"])
        exchange_rate = gamedata["system"]["stocks"][LETTER_TO_NUMBER[initial]]["value"]
        money_amount = amount * exchange_rate
        worth_amount = user_dict['lastworth'][initial] * amount / user_have_amount
        user_dict['lastworth'][initial] -= worth_amount
        user_dict['stocks'][initial] -= amount
        user_dict['money'] += money_amount
        ret = "You have sold {} {} for ${}.\n".format(amount, stock_name, amount)
        ret += "Exchange rate: ${} for 1 {}.\n".format(exchange_rate, stock_name)
        if worth_amount < money_amount:
            ret += "Stonk! Your {} was worth ${} and you have made a profit:blush:\n".format(stock_name, worth_amount)
        else:
            ret += "Not stonk! Your {} was worth ${} and you have lost money:pensive:\n".format(stock_name, worth_amount)
        ret += "Now you have ${}.".format(user_dict["money"])
        await ctx.send(ret)

    @sm.group()
    async def pay(self, ctx, *args):
        try:
            amount = int(args[1])
        except:
            await ctx.send("Do !pay @someone (amount), for example `!pay @yuusei 100`.")
            return
        if amount <= 0:
            await ctx.send("You must transfer positive value!")
            return
        arg = 3 if args[0][2] == '!' else 2
        victim_id = int(args[0][arg:-1])
        if victim_id not in gamedata:
            await ctx.send("Error: Discord ID {} was not registered. If you tagged someone, tell them to `!register`".format(victim_id))
            return
        user_dict = gamedata[ctx.message.author.id]
        victim_dict = gamedata[victim_id]
        if user_dict['money'] < amount:
            await ctx.send("You don't have enough money to pay ${} . You only have ${}".format(amount, user_dict['money']))
        else:
            user_dict['money'] -= amount
            victim_dict['money'] += amount
            await ctx.send("You have paid ${} to {}. Now you have ${}".format(amount, args[0], user_dict['money']))

    @sm.group()
    async def save(self, ctx, *args):
        with open(GAMEDATA_DIR, 'w') as f:
            json.dump(gamedata, f)
        await ctx.send("saved")


# master
'''
for user in gamedata:
    if user != "system":
        gamedata[user]['lastworth'] = {}
        gamedata[user]['lastworth']['a'] = 0
        gamedata[user]['lastworth']['b'] = 0
        gamedata[user]['lastworth']['c'] = 0
        gamedata[user]['lastworth']['d'] = 0
        gamedata[user]['lastworth']['e'] = 0
        gamedata[user]['lastworth']['f'] = 0
        gamedata[user]['lastseen'] = {}
        gamedata[user]['lastseen']['a'] = 1000
        gamedata[user]['lastseen']['b'] = 1000
        gamedata[user]['lastseen']['c'] = 1000
        gamedata[user]['lastseen']['d'] = 1000
        gamedata[user]['lastseen']['e'] = 1000
        gamedata[user]['lastseen']['f'] = 1000
'''
async def auto_save():
    while True: # not client.is_closed:
        #print(gamedata)
        #print('###')
        with open(GAMEDATA_DIR, 'w') as f:
            json.dump(gamedata, f)
        await asyncio.sleep(60)
'''
if True:
    client.loop.create_task(auto_save())
    client.run(TOKEN)
'''
task = ""
def setup(client):
    global task
    task = client.loop.create_task(auto_save())
    client.add_cog(StockModel(client))

def teardown(client):
    global task
    task.cancel()
    client.remove_cog("StockModel")
    
