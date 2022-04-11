# discord_bot

Bot to return query keyword and update pics and download button

The purpose of this project is like following:

- discord_bot.py is the bot script. 

- It adds a slash command /colour to invoke [MovieInfo](https://github.com/crvideo/MovieInfo) to seach a keyword in two avideo websites. 

[/colour keyword](./img/1.png)

- The results will generate several lines of drop select options. 

[options](./img/2.png)

- After you choose an option, the pics for the video will embed in the discord message.

[embed](./img/3.png)

- A download button will appear below the select options.

- By pressing the download button, the bot will query the specific video using [raincoat_prowlarr](https://github.com/crvideo/raincoat). The json results including download link will be returned in background.

- The download link will be sent to approprate downloading client to download it.

[downloading](./img/4.png)

# requisites

## python packages for build

- disnake
- disnake.ext
- subprocess
- json
- pprint
- re
- pathlib
- argparse
- urllib.parse
- shutil
- os.path


## other packages
- MovieInfo
- raincoat-prowlarr
- loaded indexers in Jackett/Prowlarr




# usage

```{bash, label = "", linewidth = 85, eval=opt$eval}

python discord_bot.py 

```

# options

- --config (str)
  - config files not in default path
- --test_guilds (int)
  - your servers id
- --token
  - your bot's token


# Config file
Put the config file in $HOME/.config/discord_query_bot.json


{
    "test_guilds": a long number,
    "token": "a long str"
}


- test_guilds (int)
  - This is the server name. You can right click onthe server and copy id to find it. Specifying test_guilds to accelerate deployment of your bots, which facilitate of debuging.

- token (str)
  - This is the token of your bot. You create a bot, give it the right permissions and generate a token.
  
  

# discord bot related

[How to create a bot account](https://discordpy.readthedocs.io/en/stable/discord.html)

[How to find server id](https://www.alphr.com/discord-find-server-id/)

[How to use disnake to write a bot](https://github.com/DisnakeDev/disnake)

[Quick start of minimal bot](https://docs.disnake.dev/en/latest/quickstart.html)

[Examples of disnake](https://github.com/DisnakeDev/disnake/tree/master/examples)

[Button](https://github.com/DisnakeDev/disnake/blob/master/examples/views/button/confirm.py)

[Select](https://github.com/DisnakeDev/disnake/blob/master/examples/views/select/dropdown.py)

Pay attention to:

disnake.ui.View
disnake.ui.Button
disnake.ui.Select
disnake.MessageInteraction



# Acknowledgement

I am totally newhand to develop this project. It's workable but not fancy.
