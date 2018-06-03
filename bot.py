#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By @jesuscirino
from util.aux import get_body
import discord
from discord.ext import commands

import steem

import json
import asyncio
import pickle
import argparse
import os
import datetime
from math import log10

parser = argparse.ArgumentParser()
parser.add_argument("token", help="set a discord bot token", type=str)
args   = parser.parse_args()
TOKEN = args.token

TIMEFORMAT = '%Y-%m-%d-%H-%M-%S'


description = '''An sample bot to Lince projet automatization'''
bot = commands.Bot(command_prefix='ñ', description=description, max_messages=100000)

def save(text, file_name ):
   with open(file_name, 'a') as bf:
       bf.write(str(text) + '\n')

def mk(text):
    return "```markdown\n{} ```".format(str(text))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----------')
    #await bot.change_presence(status=discord.Status.invisible)

@bot.command(pass_context=True)
async def t(ctx, id_m:str):
    """broadcast comments """
    pass

@bot.command(pass_context=True)
async def rep(ctx, id_m:str, file_name:str):
    """Get Reports """
    list_lines = []
    counter = 0
    m    = ctx.message
    time = None
    tmp = await bot.say(mk('find message id...'))
    async for log in bot.logs_from(m.channel, limit=10000):
        if log.id == id_m:
            time = log.timestamp
        counter += 1
    await bot.edit_message(tmp, mk('{} messages found.'.format(counter)))
    if time is None:
        await bot.edit_message(tmp, mk('not message found with id: {}'.format(id_m)))
        return
    else:
        await bot.edit_message(tmp, mk('saving ......'))
        counter = 0
        async for log in bot.logs_from(m.channel, limit=10000):
            content  = log.content.strip(' ')
            t        = log.timestamp.strftime(TIMEFORMAT)
            list_aux = content.split()
            content  = ' '.join(list_aux) + ' '+ log.author.name + ' '+ str(t)
            save(content ,file_name)
            counter += 1
            if time >= log.timestamp:
                break
        await bot.edit_message(tmp, mk('{} messages saved'.format(counter)))

        with open(file_name, 'r+') as f:
            list_lines = f.readlines()[:]
            list_lines.reverse()
        with open(file_name, 'w') as f:
            f.writelines(list_lines)
        await bot.delete_message(tmp)

@bot.command(pass_context=True)
async def de(ctx, id_m:str):
    """Delete a bot message with an id"""
    m    = ctx.message
    async for log in bot.logs_from(m.channel, limit=10000):
        if log.id == id_m:
            await bot.delete_message(log)

@bot.command(pass_context=True)
async def gb(ctx, ini:str, top:str):
    """Show a report body for steemit
    from ini to top dates 
    Example: ñgb 17-11-19 17-11-20"""
    ch   = ctx.message.channel
    now  = os.getcwd()
    os.chdir(now+'/util')
    body = get_body(ini, top)
    with open('tablita.txt', 'w') as f:
        print(body,file=f)
    with open('tablita.txt', 'rb') as f:
        await bot.send_file(ch, f)
    os.chdir(now)

bot.run(TOKEN)
