

# Known issues

Selfbot - unable to detect all of the members in the server. Fetch members command will be added in 2.3 including mass DM.

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
* params: \[ChannelName#No spaces allowed] {CategoryName#Spaces allowed} 

### `addRole`

* aliases: `aRole`, `aR`
* description: Adds a role to the server you are connected to.
* params: \[roleName#Spaces allowed but you cannot of names end with numbers] {rolePermissions#Use a role permissions calculator, there's one provided in builder.html, and put it at the end of the roleName separated with space}

### `addEmoji`

* aliases: `aEmoji`, `aEm`
* description: Adds an emoji to the server you are connected to.
* params: 

### `addVoiceChannel`

* aliases: `aVoiceChannel`, `aVC`
* description: Adds a voiceChannel to the server you are connected to.
* params: 

### `addCategory`

* aliases: `aCat`, `aCa`
* description: Adds a category to the server you are connected to.
* params: 

### `ban`

* aliases: No command * aliases provided.
* description: Bans someone in the server you are connected to.
* params: 

### `banAll`

* aliases: No command * aliases provided.
* description: bans everyone it can in the connected server.
* params: 

### `bans`

* aliases: No command * aliases provided.
* description: Shows all the bans in the server that you are connected to.
* params: 

### `channelBomb`

* aliases: No command * aliases provided.
* description: Makes a ton of random channels in the connected server.
* params: 

### `categoryBomb`

* aliases: No command * aliases provided.
* description: Makes a ton of random categorys in the connected server.
* params: 

### `channels`

* aliases: `tc`, `textchannels`, `textchannel`, `channel`
* description: Shows the channels that are in the server you are connected to.
* params: 

### `checkRolePermissions`

* aliases: `check`, `crp`
* description: Checks a roles permissions.
* params: 

### `categories`

* aliases: `cat`, `category`
* description: Shows the categories that are in the server you are connected to.
* params: 

### `clear`

* aliases: `purge`
* description: Deletes a certain number of messages in a connected server
* params: 

### `changeStatus`

* aliases: `cs`
* description: Changes the status of the bot.
* params: 

### `connect`

* aliases: `con`
* description: Connects the bot to a server.
* params: 

### `deleteRole`

* aliases: `dRole`, `dR`
* description: Deletes a role in the server you are connected to.
* params: 

### `deleteChannel`

* aliases: `dChannel`, `dCh`
* description: Deletes a channel in the server you are connected to.
* params: 

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
* description: Deletes a CC in the server you are connected to.
* params: 

### `deleteEmoji`

* aliases: `dEm`
* description: Deletes a emoji in the server you are connected to.
* params: 

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
* params: 

### `help`

* aliases: `h`, `commands`
* description: Display all the commands. args: [Optional: type: all/names/command: default=names] [Optional: n: n of page]
* params: 

### `joinNuke`

* aliases: `nukeOnJoin`, `join nuke`
* description: When it joins the server it nukes immediately.
* params: 

### `kaboom`

* aliases: No command * aliases provided.
* description: Combines the channelBomb, categoryBomb, and the categoryBomb all into one command.
* params: 

### `leave`

* aliases: No command * aliases provided.
* description: Leaves the server you choose to leave.
* params: 

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
* description: Moves any role in the server you are connected to.
* params: 

### `nuke`

* aliases: No command * aliases provided.
* description: combines the banAll, deleteAllChannels, deleteAllEmojis, deleteAllRoles, deleteAllWebhooks commands into one big command. Also changes the connected servers name and icon. Plus, it runs commands inside of "after" after nuking.  
* params: 

### `off`

* aliases: `logout`, `logoff`, `shutdown`, `stop`
* description: Turns off the bot.
* params: \[]

### `roleBomb`

* aliases: No command * aliases provided.
* description: Makes a ton of random roles in the connected server.
* params: 

### `roles`

* aliases: `ro`, `role`
* description: Shows the roles that are in the server you are connected to.
* params: 

### `roleTo`

* aliases: No command * aliases provided.
* description: Gives a role to someone in the connected server.
* params: 

### `si`

* aliases: `serverIcon`, `changeServerIcon`
* description: Changes the server icon in the connected server.
* params: 

### `servers`

* aliases: `se`, `server`
* description: Shows the servers the bot is in.
* params: 

### `sn`

* aliases: `serverName`, `changeServerName`
* description: Changes the server name in the connected server.
* params: 

### `unban`

* aliases: No command * aliases provided.
* description: Unbans someone in the server you are connected to.
* params: 

### `voiceChannels`

* aliases: `vc`, `voicechannel`
* description: Shows the voiceChannels that are in the server you are conencted to.
* params: 

### `webhook`

* aliases: `webhooks`, `wh`
* description: Creates, Attacks, Lists all of the weebhooks in the connected server.
* params: 

