#unitBot.py

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks

# Allowable units, ignore
siunits = ['nm','nanometer','mm','milimeter','cm','centimeter','m','meter','metre','km','kilometer','gram','g','kilogram','kg']

# All conversions, relative to 1mm/1g
length_units = {
    'nm':.000001,
    'nanometer':.000001,
    'mm':1,
    'milimeter':1,
    'cm':10,
    'centimeter':10,
    'm':1000,
    'meter':1000,
    'metre':1000,
    'km':1000000,
    'kilometer':1000000,
    '\"':25.4,
    'in':25.4,
    'inch':25.4,
    'inches':25.4,
    'endmill':25.4, # currently treats endmill keyword as inches
    'ft':304.8,
    '\'':304.8,
    'foot':304.8,
    'feet':304.8,
    'yd':914.4,
    'yard':914.4,
    'yards':914.4,
    'mi':1609000,
    'mile':1609000,
    'miles':1609000,
    'cubit':457.2,
    'cubits':457.2,
    'micron': .001,
    'microns': .001,
    'parsec': 3.086e+19,
    'parsecs': 3.086e+19,
    'banana': 190.5,
    'bananas': 190.5,

}

mass_units = {
    'lbs': 453.59,
    'lb': 453.59,
    'ton': 907184.74,
    'elephant':7000000,
    'elephants': 7000000,
    'ounce': 28.3495,

}

#Needed for fraction support, cast isn't great

def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


def convert_length(val, inp, out = 'mm'):
    std = convert_to_float(val)*length_units[inp]/length_units[out]
    ret = std
    un = 'mm'
    if std >= 100:
        un = 'cm'
        ret = std/length_units[un]
    if std >= 1000:
        un = 'm'
        ret = std/length_units[un]
    if std >= 1000000:
        un = 'km'
        ret = std/length_units[un]
    return str(round(ret, 4)) + un


def convert_mass(val, inp, out = 'mm'):
    std = convert_to_float(val)*mass_units[inp]/mass_units[out]
    ret = std
    un = 'g'
    if std >= 1000:
        un = 'kg'
        ret = std/mass_units[un]
    return str(round(ret, 4)) + un

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

    if '.convert' in message.content:
        msgs = await message.channel.history(limit=4).flatten()
        last = None
        for msg in msgs:
            if message.author == client.user:
                return

            words = msg.content.split()
            for i, w in enumerate(words):
                # for space split:
                if w in length_units.keys() or w.rstrip(w[-1]) in length_units.keys():
                    if w not in siunits:
                        response = '`' + words[i-1] + ' ' + w + ' = ' + str(convert_length(words[i-1], w)) + '`'

                if w in mass_units.keys() or w.rstrip(w[-1]) in mass_units.keys():
                    if w not in siunits:
                        response = '`' + words[i-1] + ' ' + w + ' = ' + str(convert_mass(words[i-1], w)) + '`'
                    
                # for no space:
                for u in length_units.keys():
                    if u in w:
                        val = w[:-len(u)]
                        try:
                            if u not in siunits:
                                response = '`' + val + ' ' + u + ' = ' + str(convert_length(val, u)) + '`'
                        except:pass

                for u in mass_units.keys():
                    if u in w:
                        val = w[:-len(u)]
                        try:
                            if u not in siunits:
                                response = '`' + val + ' ' + u + ' = ' + str(convert_mass(val, u)) + '`'
                        except:pass

            try:
                if response != last:
                    await message.channel.send(response)
                    last = response
            except: pass


#################

    if '!gif saunders' in message.content:
        await message.channel.send('https://cdn.discordapp.com/attachments/833543996210675772/839284254608719872/w09w28.gif')

#    if 'machine monitoring' in message.content:
#        await message.channel.send('Here\'s a really good recommendation! https://www.machinemetrics.com')

client.run(TOKEN)