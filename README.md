# Nuking Discord Server Bot/Nuke Bot

### note update on this bot: We might start to work on the during breaks (too much school in the last few months). I'm sorry if you are having problems while using this bot. Once again, the bot is depended on whether if you configured the bot right or wrong.
And remember to check if the bot has the permission to use the command you want it to perform. Good luck!

Update 12/22/2020: C-REAL V2 is here. More descriptions will be added soon. builder.html is also getting an update; it will be added to the github page soon. For now you have to configurate the .json files manually :). 

## C-REAL bot
* If you need extra help dm cyxl#9986 on discord.
* C-REAL bot has 45 commands:
```
[addEmoji] [addRole] [addChannel] [addVoiceChannel] 
[addCategory] [ban] [bans] [banAll] [connect] 
[channelBomb] [categoryBomb] [categories] 
[checkRolePermissions] [channels] [clear] [changeStatus] 
[deleteRole] [deleteChannel] [deleteVoiceChannel] 
[deleteCategory] [deleteCC] [deleteEmoji] [deleteAllRoles] 
[deleteAllChannels] [deleteAllEmojis] [deleteAllWebhooks] 
[emojis] [help] [joinNuke] [kaboom] [leave] [leaveAll] 
[link] [moveRole] [nuke] [off] [roles] [roleBomb] [roleTo] 
[si] [sn] [servers] [unban] [voiceChannels] [webhook] 
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
3. Make a configuration file with builder.HTML
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
 
<!-- ## How to use builder.html
 builder.html is a web page that can help you to make the configuration file for the bot.
### Enter your bot's token
 Enter the token you got from (how to setup a token)
### Bot permission calculator
 Bot permission calculator is used for permission that will give to the bot when inviting.
### User permissions
##### C-REAL currectly doesn't support tags with special characters.
 The bot will check if the tag of the person that used (".something" command) matches the tags you put in the user permissions. If it matches, the bot will execute the command. If not, the bot will print out a line saying who and where is the person using the command.
### Kaboom
#### Random
 Enter an positive integer that will tell the bot during any bomb commmands like ".kaboom 10 random" to spam with random base64 text with a give length.
#### Fixed
 Enter anything you want that will tell the bot during any bomb commands like ".kaboom 10 fixed" to spam with fixed text randomly.
### After
 After part, is executed during ".nuke" the channels, categories, and roles created in the after command will not get affected by ".nuke".
 You can enter any C-REAL bot command that you can use in the discord chat in the after part.
 If you are not experienced with all the commands, you can leave it blank.
examples: IMPORTANT: inside the after part, everything will be case sensitive. And you don't need the bot's prefix in the after part. -->
### How to turn on discord intents?
* Go to discord developer portal
* Login
* Navigate to your bot application > "bot" tab (the place you get your bot token from) > scroll down a little bit > and turn on the 2 buttons that is right under "Privileged Gateway Intents".
 ![Image of a screenshot](https://snipboard.io/U04VLE.jpg)

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
            "right now, there's only a 1/4 chance for one of the spammer to not have a pfp"
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
* permissions: This is for allowing the people/bot that is in it to use _any_ C-REAL commands.
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

## How to use the C-REAL
``` This image is from a BETA version of v1```
* After you are done with setting up the config file, all you have to do is to open the executable.
* You can choose to put the default.json next to the executable(so the bot will use the default.json everyone time you open, that way you don't have to write a path for the configuration file again.), or you can type the path-to-the configuration file when the bot asked.
* After finishing everything, you'll see the all the information displayed in the console.
* The invite link for the bot will always be generated in the console when the bot is ready to run commands.
![Image of a screenshot](https://snipboard.io/p4EjKZ.jpg)

## Problems/issues
* If you are experiencing crushing, please report it to "issues" to [github page](https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot).
* If the bot doesn't respond to any of the commands, check if the console is in highlighting/mark mode. If it's highlighting/mark mode, click the console then press any key on your keyboard, and it'll resolve.
* If you see a bunch of white worded errors displaying in the console, that means you are using debugging mode. (the current windows prebuilt version is in debugging mode)
