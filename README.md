# Nuking Discord Server Bot/Nuke Bot
* C-REAL is currently the **FASTEST** and **FREE** open source nuke bot out here. All commands will be focused on nuking-related.

* We have combined threading, queue, requests, and discord.py API to make the commands run as fast as possible. If you are seeing rate limiting logged in your console while using this script, then that is simply because <ins>it runs too fast</ins>.

* Python version 3.8.0 or higher is required if you are going to run the file from source code.

* Update log: [here](news.txt)

* [All 49 commands](manual.md)

```
[addEmoji] [autoNick] [autoStatus] [addVoiceChannel] 
[addCategory] [addRole] [addChannel] [banAll] [ban] 
[bans] [categoryBomb] [checkRolePermissions] [clear] 
[changeStatus] [channels] [categories] [connect] 
[channelBomb] [deleteCategory] [deleteCC] [deleteEmoji] 
[disableCommunityMode] [deleteAllRoles] [deleteAllChannels] 
[deleteAllEmojis] [deleteAllWebhooks] [deleteRole] [deleteChannel] 
[deleteVoiceChannel] [emojis] [help] [joinNuke] 
[kaboom] [leave] [leaveAll] [link] [members] [moveRole] 
[nuke] [off] [roleTo] [roles] [roleBomb] [si] [sn] 
[servers] [unban] [voiceChannels] [webhook]
```

# IMPORTANT: 
* We will not take any responsibility over whatever you are going to do with this bot.
* The bot will still have to obey the [server limitings](https://discordia.me/en/server-limits) because of that in discord, there are rate limitings. You will see a lot of rate limiting in the console while using some commands. (because the bot is too fast on creating or deleting.)
* Also, since we are using HTTP requests, unlike other nuke bot out there, C-REAL spam creating channel, role, and category(CRC) can create beyond the 250 limit for CRC that the old nuking bots have.

## Messages
* cyxl: Hi!

* Message to those coding masters out there, if you see something we can improve in our code, feel free to make a pull request. This will really help us a lot. ╰(✿´⌣\`✿)╯♡

* TKperson: I got the idea of creating the C-REAL bot from [Cerealwithnomilk](https://www.youtube.com/channel/UCxX7O68badw2sBbcvQK0wBQ); the bot is named after this guy.

## Common errors
1. PrivilegedIntentsRequired (non-selfbot users only)
[![9977.png](https://i.postimg.cc/9fjCQNsh/9977.png)](https://postimg.cc/gx4fM4YS)
Solution: Watch https://youtu.be/DXnEFoHwL1A?t=44 starting from 0:44 to turn on the required 2 buttons. (In the future, I'm going to make this requirement optional)

2. Unreadable json formatting
[![886.png](https://i.postimg.cc/766cH3P4/886.png)](https://postimg.cc/PLgKK88V)
Solution: This error means that you have an/multiple error(s) in your default.json file, it can be caused by missing/extra commas, brakets, quotes, and the like. You can use https://jsonlint.com/?code= to check your `default.json` file.

3. Litterary crashed when opening c-realv2.py or c-realv2.exe
Causes: It might be caused by anti virus that quarantined this program, old versions of python (needs to be v3.8.0 or higher), old versions of packages (update your discord.py with pip!), didn't install any required packages at all.
Solution: Update everything to the latest version, and try turning off anti virus. If you are still having an issue, you should report it in this github page right away.

## Immigrate from verision 2.3.x to 2.4.0
1. Make a new folder named "data" next to your c-realv2.exe or c-realV2.py file
2. put your old default.json into the data folder
3. start running the bot again.

## Setting up 2.4
* If you have any question about what to do about 2.4 when setting up you can make a new issue in the github page.
* Version 2.4.0 should be very easy to understand, all you have to do in this version is to be able to run the c-realv2.py/exe file. And for configuration just use the .config command for more information.

## Guides for versions below 2.4.0 only. No guides for version 2.4 yet.
### Setup/config
[![setup](http://img.youtube.com/vi/ovEj9Rjq2sQ/0.jpg)](http://www.youtube.com/watch?v=ovEj9Rjq2sQ "setup")
### Setup with GUI (if you don't like setting up with a text editor)
[![setting up with builder.html](http://img.youtube.com/vi/DXnEFoHwL1A/0.jpg)](http://www.youtube.com/watch?v=DXnEFoHwL1A "setting up with builder.html")
### Nuke and kaboom commands
[![nuke/kaboom](http://img.youtube.com/vi/GTs3mvyoh5U/0.jpg)](http://www.youtube.com/watch?v=GTs3mvyoh5U "nuke/kaboom")
### How to perform webhook spams
[![webhooks attack script showcasing](http://img.youtube.com/vi/0jFdbY9Q2HQ/0.jpg)](http://www.youtube.com/watch?v=0jFdbY9Q2HQ "webhooks")
### check permission command and some other commands
[![other1](http://img.youtube.com/vi/gGxeg3lyNDQ/0.jpg)](http://www.youtube.com/watch?v=gGxeg3lyNDQ "other1")
### Other commands part 2
[![other2](http://img.youtube.com/vi/IBOahDX1QHg/0.jpg)](http://www.youtube.com/watch?v=IBOahDX1QHg "other2")

## Problems/issues
* If you are experiencing crashing, please report it to "issues" on the [github page](https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot).
* If the bot doesn't respond to any of the commands, check if the console is in highlighting/mark mode. If it's highlighting/mark mode, click the console then press any key on your keyboard, and it'll resolve.
* If you see a bunch of white worded errors displaying in the console, and then crashed that means it's 90% a bug. So please make a new issue about it.
