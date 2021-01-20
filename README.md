# Nuking Discord Server Bot/Nuke Bot
* C-REAL is currently the **FASTEST** and **FREE** open source nuke bot out here. All commands will be focused on nuking-related.

* We have combined threading, queue, requests, and discord.py API to make the commands run as fast as possible. If you are seeing rate limiting logged in your consol while using this script, then that is simply because <ins>it runs too fast</ins>.

* If you want the updates that have been happening click [here](news.md)

* All 48 commands can be found [here](manual.md)


# IMPORTANT: 
* We will not take any responsibility over whatever you are going to do with this bot.
* The bot will still have to obey the [server limitings](https://discordia.me/en/server-limits) here.
* Note: in discord, there are rate limitings. You will see a lot of rate limiting in the console while using some commands. (because the bot is too fast on creating or deleting.)
* Also, since we are using HTTP requests, unlike other nuke bot out there, C-REAL spam creating channel, role, and category(CRC) can create beyond the 250 limit for CRC that the old nuking bots have.

## Check list for setting up everything
1. [Download](https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot/releases/latest/download/c-realV2.zip) the C-REAL file(or download the [whole thing](https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot/archive/master.zip))
2. Get a discord profile(token) for the bot.
3. Make a configuration file with `builder.html`.
4. Drag the configured json file next to the executable file(The prebuilt verison)
5. Run the executable, and it should give you a bot invite link after the bot is ready. If the console closed by itself that means there's something wrong with the code and please report the issue to this github page.
6. (Optional) If the bot is asking for a path-to-the configuration file, you enter a local path or full path for the config file.

## What is a token/how to setup a token
 1. The token for a bot is the profile for the bot. You'll need a profile for the bot to join servers.
 2. Go to [Discord developers site](https://discord.com/developers/applications), login or sign up.
 3. Create a new application or use your created application
 4. Go to the bot tab in the application.
 5. Click on add bot.
 6. And then click on "Click to Reveal Token" or "Copy" to get your token.

## Configuration file
C-REAL will always try to look for the file "default.json" that is next to it, after finding the file it'll use that file. If you don't have a config file, the bot will ask you to enter a path for the config file. This feature is made for multiple nukes.
Here's what the config file should look like if it's expanded (not in a single line):

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

* Although, if you don't what to configurate or use the one that I provided you can change it or make a new one with `builder.html`.

## Guides
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

## How to use the C-REAL
``` This image is from a BETA version of v1```
* After you are done with setting up the config file, all you have to do is to open the executable.
* You can choose to put the default.json next to the executable(so the bot will use the default.json everyone time you open, that way you don't have to write a path for the configuration file again.), or you can type the path-to-the configuration file when the bot asked.
* After finishing everything, you'll see the all the information displayed in the console.
* The invite link for the bot will always be generated in the console when the bot is ready to run commands.
![Image of a screenshot](https://snipboard.io/p4EjKZ.jpg)

## Problems/issues
* If you are experiencing crashing, please report it to "issues" on the [github page](https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot).
* If the bot doesn't respond to any of the commands, check if the console is in highlighting/mark mode. If it's highlighting/mark mode, click the console then press any key on your keyboard, and it'll resolve.
* If you see a bunch of white worded errors displaying in the console, and then crashed that means it's 90% a bug. So please make a new issue about it.
* If you need extra help dm cyxl#0001 on discord.

### Extra
* PS: woah, 150+ commits, never thought I would even have something passing 10 commits also 18 stars. You guys are amazing thanks for all the support.

* Message to those coding masters out there, if you see something we can improve in our code, feel free to make a pull request. This will really help us a lot. ╰(✿´⌣\`✿)╯♡
