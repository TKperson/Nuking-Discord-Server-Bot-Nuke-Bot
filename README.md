# Nuking Discord Server Bot/Nuke Bot

### note update on this bot: We might start to work on the during breaks (too much school in the last few months). I'm sorry if you are having problems while using this bot. Once again, the bot is depended on whether if you configured the bot right or wrong.
And remember to check if the bot has the permission to use the command you want it to perform. Good luck!

Update 12/22/2020: C-REAL V2 is here. More descriptions will be added soon.

## C-REAL bot
* If you need extra help dm cyxl#9986 on discord.
* C-REAL bot has 47 commands:
```
[addEmoji] [autoNick] [addCategory] [addRole] [addVoiceChannel] 
[addChannel] [ban] [bans] [banAll] [connect] [categories] 
[checkRolePermissions] [clear] [changeStatus] [channelBomb] 
[categoryBomb] [channels] [deleteAllRoles] [deleteAllChannels] 
[deleteAllEmojis] [deleteAllWebhooks] [deleteRole] [deleteChannel] 
[deleteVoiceChannel] [deleteCategory] [deleteCC] [deleteEmoji] 
[emojis] [help] [joinNuke] [kaboom] [leave] [leaveAll] [link] 
[members] [moveRole] [nuke] [off] [roleTo] [roleBomb] [roles] 
[servers] [si] [sn] [unban] [voiceChannels] [webhook]
```

## About the bot
I got idea of creating the C-REAL bot from [Cerealwithnomilk](https://www.youtube.com/channel/UCxX7O68badw2sBbcvQK0wBQ) and the bot is named after that guy.And a shout out to cyxl#9986 for helping me making C-REAL.

You can already tell most of the commands by its name.
But if you are still confused with the command: go read manual.md.

Note: in discord, there are rate limitings. You will see a lot of rate limiting in the console while using some commands. (because the bot is too fast on creating or deleting.)

#### IMPORTANT: We will not take any responsibility over whatever you are going to do with this bot. This script is created with to test anti nuke/anti spam bots.

## Check list for setting up everything
1. Download the C-REAL file(or download the whole thing)
2. Get a discord profile(token) for the bot.
3. Make a configuration file with builder.HTML (Currently builder.html is not available. It still needs an update to match with V2.)
4. Drag the configured json file next to the executable file(The prebuilt verison)
5. Run the executable, and it should give you a bot invite link after the bot is ready. If the console closed by itself that means there's something wrong with the configuration file.
6. (Optional) If the bot is asking for a path-to-the configuration file, you enter a local path or full path for the config file.

## What is a token/how to setup a token
 1. The token for a bot is the profile for the bot. You'll need a profile for the bot to join servers.
 2. Go to [Discord developers site](https://discord.com/developers/applications), login or sign up.
 3. Create a new application or use your created application
 4. Go to the bot tab in the application.
 5. Click on add bot.
 6. And then click on "Click to Reveal Token" or "Copy" to get your token.
```
aCat a category that is going to be added during .nuke
aChannel a-channel-that-is-going-to-be-added-during-nuke-to-the-category
sn this changes the server name to this during nuke
si https://www.this.changes/the/server/icon/to/this/url.jpg
kaboom 1000000000 random
```

### Configuration file
C-REAL will always try to look for the file "default.json" that is next to it, after finding the file it'll use that file. If you don't have a config file, the bot will ask you to enter a path for the config file. This feature is made for multiple nukes.
Here's what the config file should look like if it's expanded (not in a single line):
```json
{
    "token": "<bot tokens or selfbot tokens> here",
    "permissions": [
        "TKperson#2348",
        "cyxl#9986",
        "739547265059913759",
        "349338062485979136"
    ],
    "bomb_messages": {
        "random": 10,
        "fixed": [
            "fixed 1",
            "fixed 2",
            "fixed 3",
            "ezzzzz",
            "TKperson",
            "fixed 4",
            "fixed 5",
            "fixed 6",
            "fixed 7"
        ]
    },
    "webhook_spam": {
        "pfp_urls": [
            null,
            "link to image",
            "link to image2",
        ],
        "usernames": [
            "\u200b",
            "more names",
            "more names2"
        ],
        "contents": [
            "@TKperson Hello C-real was here",
            "C-REAL on top",
            "Keep this under 2000 characters",
            ":The_bot_can_use_any_emojis_in_all_the_servers_that_the_bot_is_in: <- that is not 1 character keep that in mind"
        ]
    },
    "bot_permission": "2146958847",
    "command_prefix": ".",
    "bot_status": "offline",
    "verbose": 15,
    "after": [
        "aCat something",
        "aChannel some-channel-to something",
        "sn nuked",
        "si https://ih1.redbubble.net/image.788111706.5520/st,small,507x507-pad,600x600,f8f8f8.u2.jpg"
    ]
}
```
* token: Your bot's token or an user account token.
* permissions: This is for allowing the people/bot that is in it to use __any__ C-REAL commands.
* bomb_messages: `an`, `b64`, and `fixed` are the only bomb types that are supported currently.
 * random: The positive integer that is in this will tell the bot how long the length of random bomb should be for base64 and alphanumeric characters. usage example: `.kaboom 10 an` or `.kaboom 10 b64`
 * fixed: The texts that are in it will be randomly choosed when running a fixed bomb commands. EX. `.kaboom 10 fixed` (this will create 10 channels, categories, and roles [only if it has permissions] with names that is randomly chosen from `fixed` texts.)
* webhook_spam: None of the webhook things below can leave be empty
 * pfp_urls: Put `null` if you don't want the spammers to have a pfp. Put a link to an image if you want that image to be on one of your spammer.
 * usernames: Put `\u200b`(ZERO WIDTH SPACE) if you don't want the spammers to have a name.
 * contents: Put messages that you want the spammer to say. Note: keep the messages under 2000 unicode characters because that's the limit to how much you characters you can send in 1 message.
* bot permission: permissions that will be asked when the bot is getting invited to a server.
* command_prefix: Put a command prefix that you like in there.
* bot_status: When the script is connected to a profile, it will change the status of the current profile to whatever you put in there. Note: things you can put in there are `offline`, `invisible`, `dnd` (or `do_not_disturb`), `online`, or `idle`.
* verbose: Things that will be logged to you when you are running the bot. `0` is nothing will be logged to you. `15` is everything. Use builder.html to change verbose levels.
* after: commands that are in the "after" will be run after `.nuke` command. You can put the commands that you normally use in discord on there with the format showed in this example. And it's case insensitive.

* Although, if you don't what to configurate or use the one that I provided you can change it or make a new one with builder.html.

## Guids
[![cofig](http://img.youtube.com/vi/iM8TEYHwN9k/0.jpg)](http://www.youtube.com/watch?v=iM8TEYHwN9k "config")

[![nuke/kabbom](http://img.youtube.com/vi/iM8TEYHwN9k/0.jpg)](http://www.youtube.com/watch?v=iM8TEYHwN9k "nuke/kabbom")

[![webhook](http://img.youtube.com/vi/iM8TEYHwN9k/0.jpg)](http://www.youtube.com/watch?v=iM8TEYHwN9k "webhook")

[![other](http://img.youtube.com/vi/iM8TEYHwN9k/0.jpg)](http://www.youtube.com/watch?v=iM8TEYHwN9k "other")

## How to use the C-REAL
``` This image is from a BETA version of v1```
* After you are done with setting up the config file, all you have to do is to open the executable.
* You can choose to put the default.json next to the executable(so the bot will use the default.json everyone time you open, that way you don't have to write a path for the configuration file again.), or you can type the path-to-the configuration file when the bot asked.
* After finishing everything, you'll see the all the information displayed in the console.
* The invite link for the bot will always be generated in the console when the bot is ready to run commands.
![Image of a screenshot](https://snipboard.io/p4EjKZ.jpg)

## Problems/issues
* If you are experiencing crushing, please report it to "issues" on the [github page](https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot).
* If the bot doesn't respond to any of the commands, check if the console is in highlighting/mark mode. If it's highlighting/mark mode, click the console then press any key on your keyboard, and it'll resolve.
* If you see a bunch of white worded errors displaying in the console, that means you are using debugging mode. (the current windows prebuilt version is in debugging mode)
