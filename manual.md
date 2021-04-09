

# Known issues

Selfbot - unable to detect all of the members in the server. Fetch members command will be added in 2.4 or later including mass DM.

# Commands documnet

All commands are not case sensitive.

\[a] - required argument

{a} - optional argument

\[a='1'] or {a='1'} - a is set to '1' by default.

[a#This is a comment] or {a#This is a comment}

\[] - no arguement is needed

# descriptions will be written out soon...
### `addChannel`

* aliases: `aCh`, `aChannel`
* description: Adds a channel to the server you are connected to.
* params: \[name#No spaces allowed] {category=None#Spaces allowed} 

### `addRole`

* aliases: `aRole`, `aR`
* description: Adds a role to the server you are connected to.
* params: \[roleName#Spaces allowed but you cannot of names end with numbers] {rolePermissions#Use a role permissions calculator, there's one provided in builder.html, and put it at the end of the roleName separated with space}

### `addEmoji`

* aliases: `aEmoji`, `aEm`
* description: Adds an emoji to the server you are connected to.
* params: \[item#You can use a link, discord custom emojis, or your computer file path] {name#No spaces; this is only required when you are using a link in the first arg}

### `addVoiceChannel`

* aliases: `aVoiceChannel`, `aVC`
* description: Adds a voiceChannel to the server you are connected to.
* params: \[name#No spaces] {category=None#Spaces allowed}

### `addCategory`

* aliases: `aCat`, `aCa`
* description: Adds a category to the server you are connected to.
* params: \[name#Spaces allowed]

### `ban`

* aliases: No command * aliases provided.
* description: Bans someone in the server you are connected to.
* params: \[user#Ping, id, or just username. If there are 2 or more same usernames, the script will always pick the one that comes first]

### `banAll`

* aliases: No command * aliases provided.
* description: bans everyone it can in the connected server.
* params: \[]

### `bans`

* aliases: No command * aliases provided.
* description: Shows all the bans in the server that you are connected to.
* params: {pageNumber=1}

### `channelBomb`

* aliases: No command * aliases provided.
* description: Makes a ton of random channels in the connected server.
* params: \[numberOfBombs#The number of channels you want to create] \[bombType#It can only be b64, an, or fixed]

### `categoryBomb`

* aliases: No command * aliases provided.
* description: Makes a ton of random categorys in the connected server.
* params: \[numberOfBombs#The number of categories you want to create] \[bombType#It can only be b64, an, or fixed]

### `channels`

* aliases: `tc`, `textchannels`, `textchannel`, `channel`
* description: Shows the channels that are in the server you are connected to.
* params: {pageNumber=1}

### `checkRolePermissions`

* aliases: `check`, `crp`
* description: Checks the total roles permission you have.
* params: \[user#Ping, id, or just username. If there are 2 or more same usernames, the script will always pick the one that comes first]

### `categories`

* aliases: `cat`, `category`
* description: Shows the categories that are in the server you are connected to.
* params: {pageNumber=1}

### `clear`

* aliases: `purge`
* description: Deletes a certain number of messages in a the channel you are using this command in.
* params: {numberOfMessages=All#Leave this blank if you want all message in that channel to be deleted, but seriously deleting the channel would be much easier}

### `changeStatus`

* aliases: `cs`
* description: Changes the status of the bot.
* params: \[status#offline, invisible, dnd (or do_not_disturb), online, or idle.]

### `connect`

* aliases: `con`
* description: Connects the bot to a server.
* params: \{server#id or server name, and unicode username is allowed. If you are using this command in the server you want to connect to, you don't have to put an argument here if that's the case}

### `deleteRole`

* aliases: `dRole`, `dR`
* description: Deletes a role in the server you are connected to.
* params: \[role#name or id]

### `deleteChannel`

* aliases: `dChannel`, `dCh`
* description: Deletes a channel in the server you are connected to.
* params: \[channel#name or id]

### `deleteVoiceChannel`

* aliases: `dVC`, `dVoiceChannel`
* description: Deletes a voiceChannel in the server you are connected to.
* params: 

### `deleteCategory`

* aliases: `dCat`, `dCategory`
* description: Deletes a category in the server you are connected to.
* params: 

### `deleteCC`

* aliases: `dCC`
* description: Deletes a channel, voice channel, or category in the server you are connected to.
* params: \[name#or id]

### `deleteEmoji`

* aliases: `dEm`
* description: Deletes a emoji in the server you are connected to.
* params: \[emoji#name or id]

### `disableCommunityMode`

* aliases: `dCM`, `dCommunityMode`
* description: Disables community mode in the server you are connected to.
* params: None

### `deleteAllRoles`

* aliases: `dar`, `dAllRoles`
* description: Deletes all roles in the connected server.
* params: \[]

### `deleteAllChannels`

* aliases: `dac`, `dAllChannels`
* description: Deletes all channels in the connected server.
* params: \[]

### `deleteAllEmojis`

* aliases: `dae`, `dAllEmoji`
* description: Deletes all emojis in the connected server.
* params: \[]

### `deleteAllWebhooks`

* aliases: `daw`, `dAllWebhooks`
* description: Deletes akk webhooks in the connected server.
* params: \[]

### `emojis`

* aliases: No command * aliases provided.
* description: Shows the emojis that are in the server you are connected to.
* params: {pageNumber=1}

### `help`

* aliases: `h`, `commands`
* description: Display all the commands. args: [Optional: type: all/names/command: default=names] [Optional: n: n of page]
* params: {type=all#all/names/command just play around with this one. It should be very easy to understand.} {pageNumber=1#for type command}

### `joinNuke`

* aliases: `nukeOnJoin`, `join nuke`
* description: Nuke command will get executed in the next server the bot joins.
* params: [boolean#True or false. True means turn it on. And false means turn it off]

### `kaboom`

* aliases: No command * aliases provided.
* description: Combines the channelBomb, categoryBomb, and the categoryBomb all into one command.
* params: \[numberOfBombs#The number of channels, categories, and roles you want to create] \[bombType#It can only be b64, an, or fixed]

### `leave`

* aliases: No command * aliases provided.
* description: Leaves the server you choose to leave.
* params: {server#name or id. If no arg is provided then the bot will leave the server it's connecting to}

### `leaveAll`

* aliases: No command * aliases provided.
* description: Leaves all servers it is in.
* params: \[]

### `link`

* aliases: `l`
* description: Sends an invite code for the bot.
* params: \[]

### `moveRole`

* aliases: `mRole`, `mR`
* description: Moves the given role in hierarchy(If you have the permissions) in the server you are connected to.
* params: \[role#name or id. Spaces are allowed] \[position#position in hierarchy. The last space separated argument will be counted has the position]

### `nuke`

* aliases: No command * aliases provided.
* description: combines the banAll, deleteAllChannels, deleteAllEmojis, deleteAllRoles, deleteAllWebhooks commands into one big command. Also changes the connected servers name and icon. Plus, it runs commands inside of "after" after nuking.  
* params: {useAfter=True#True or false. If you don't want to execute the after commands you entered in the config file you can set this to false}

### `off`

* aliases: `logout`, `logoff`, `shutdown`, `stop`
* description: Turns off the bot.
* params: \[]

### `roleBomb`

* aliases: No command * aliases provided.
* description: Makes a ton of random roles in the connected server.
* params: \[numberOfBombs#The number of roles you want to create] \[bombType#It can only be b64, an, or fixed]

### `roles`

* aliases: `ro`, `role`
* description: Shows the roles that are in the server you are connected to.
* params: {pageNumber=1}

### `roleTo`

* aliases: No command * aliases provided.
* description: Gives a role to someone in the connected server.
* params: \[user#id or ping only] \[role#name or id]

### `si`

* aliases: `serverIcon`, `changeServerIcon`
* description: Changes the server icon in the connected server.
* params: \[item#You can use a link, discord custom emojis, or your computer file path]

### `servers`

* aliases: `se`, `server`
* description: Shows the servers the bot is in.
* params: {pageNumber=1}

### `sn`

* aliases: `serverName`, `changeServerName`
* description: Changes the server name in the connected server.
* params: \[name#Unicode is allowed]

### `unban`

* aliases: No command * aliases provided.
* description: Unbans someone in the server you are connected to.
* params: \[user#name, id, or ping]

### `voiceChannels`

* aliases: `vc`, `voicechannel`
* description: Shows the voiceChannels that are in the server you are conencted to.
* params: {pageNumber=1}

### `webhook`

* aliases: `webhooks`, `wh`
* description: Creates, Attacks, Lists all of the weebhooks in the connected server.
* params: {pageNumber=1}

