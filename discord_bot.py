import disnake
from disnake.ext import commands
import subprocess
import json
import pprint
import re
from discord_bot_download import search
from pathlib import Path
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="config file for discord bot")
    parser.add_argument("--test_guilds", help="guilds to deploy")
    parser.add_argument("--token", help="token of this bot")
    args = parser.parse_args()
    return args

def load_config(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        print(f"Config file not found. ({path})")



def set_overrides(cfg,args):
    if args.test_guilds is not None:
        cfg['test_guilds'] = args.test_guilds

    if args.token is not None:
        cfg['token'] = args.token

    return cfg

args = parse_args()

cfg_path = f"{str(Path.home())}/.config/discord_query_bot.json"
if args.config is not None:
    cfg_path = args.config
cfg = load_config(cfg_path)

cfg = set_overrides(cfg, args)

bot = commands.Bot(command_prefix="$",
                   test_guilds=[cfg['test_guilds']]
                   )


# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(disnake.ui.Select):
    def __init__(self,options,):

        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="Choose your favourite colour...",
            min_values=1,
            max_values=1,
            options=options,
        )

    # async def callback(self, interaction: disnake.MessageInteraction):
    #     # Use the interaction object to send a response message containing
    #     # the user's favourite colour or choice. The self object refers to the
    #     # Select object, and the values attribute gets a list of the user's
    #     # selected options. We only want the first one.
    #     await interaction.response.edit_message(embed = json_dict[self.values[0]]["embed"])

class ConfirmButton(disnake.ui.Button):
    def __init__(self,custom_id):
        super().__init__(label=custom_id,custom_id=custom_id,style = disnake.ButtonStyle.green)

    # async def callback(self, interaction: disnake.MessageInteraction):
    #     print(interaction.component.type)
    #     await interaction.response.send_message("Confirming", ephemeral=True)
    #     self.value = True
        #self.disabled = True
    
    

class DropdownView(disnake.ui.View):
    def __init__(self, options_final,json_dict):
        super().__init__()
        self.options_final = options_final
        self.json_dict = json_dict

        # Adds the dropdown to our view object.
        for each_select in self.options_final:
            self.add_item(Dropdown(each_select))
    
    async def interaction_check(self, interaction: disnake.MessageInteraction):
        #print(str(interaction.component.type))
        if str(interaction.component.type) == "ComponentType.select":
            self.value = interaction.data.values[0]
            for item in self.children:
                #print(type(item).__name__)
                if type(item).__name__ == "ConfirmButton":
                    self.remove_item(item)
            self.add_item(self.json_dict[interaction.data.values[0]]["button"])
            await interaction.response.edit_message(embed = self.json_dict[interaction.data.values[0]]["embed"],view = self)
        if str(interaction.component.type) == "ComponentType.button":
            #await interaction.response.edit_message(content = "Confirming "+self.value)
            await interaction.response.defer()
            msg = search(self.value)
            await interaction.edit_original_message(content = msg + " " + self.value,view = self)
            
def formatSelectOption(json_data):
    options = []
    for video in json_data:
        options.append(disnake.SelectOption(label = video['number']))
    n = 25
    options_final = [options[i * n:(i + 1) * n] for i in range((len(options) + n - 1) // n )]
    return options_final
            
def addEmbed(json_dict):
    for number in json_dict.keys():
        json_dict[number]["embed"] = disnake.Embed(title =  number,
                                           description = json_dict[number].get("title"),
                                           type = "rich")
        json_dict[number]["embed"].set_image(url = json_dict[number].get("cover"))
    return json_dict

        
def runShellCmd(cmd):
    output = subprocess.run(cmd, stdout=subprocess.PIPE, shell = True)
    return output


class searchKeyword(object):
    def __init__(self,keyword):
        res = runShellCmd("MovieInfo --keyword \"" + keyword + "\"")
        #print(res.stdout)
        if res.stdout:
            self.json_data = json.loads(res.stdout.decode("utf8"))
            self.json_data = list({v['number']:v for v in self.json_data}.values())
            ## get options for select object
            self.options = formatSelectOption(self.json_data)

            ## get embed for each video
            self.json_dict = {}
            for video in self.json_data:
                self.json_dict[video['number']] = video
            self.json_dict = addEmbed(self.json_dict)

            ## create button for each video
            for number in self.json_dict.keys():
                self.json_dict[number]["button"] = ConfirmButton(custom_id = number)
        else:
            return ''


@bot.slash_command()
async def colour(inter,keyword):
    #await inter.response.send_message("confirming",view=Confirm())
    await inter.response.send_message("Searching " + keyword)
    search_result = searchKeyword(keyword)
    if search_result:
        await inter.send(view=DropdownView(search_result.options,search_result.json_dict))
    else:
        await inter.send(content="Can not found the keyword " + keyword)


bot.run(cfg['token'])
