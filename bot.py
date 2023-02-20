from discord import *
import requests
import json
import inspect


try:
    with open("config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}


while True:
    token = config.get("token", None)
    if token:
        print("Token from the last run loaded!")
    else:
        token = input("Enter token of your bot here:")
        #token = "your token here"
    
    try:
        data = requests.get("https://discord.com/api/v10/users/@me", headers={
            "Authorization": f"Bot {token}"
        }).json()
    except requests.exceptions.RequestException as e:
        if e.__class__ == requests.exceptions.ConnectionError:
            exit("Action failed! Please try again.")
        elif e.__class__ == requests.exceptions.Timeout:
            exit("Action failed! Please try again.")
        exit("Action failed! Please try again.")


    if data.get("id", None):
        break 

    print(f"Token invalid! Please enter new one.")

    config.clear()


with open("config.json", "w") as f:
    config["token"] = token

    json.dump(config, f, indent=2)


class FunnyBadge(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        
        await self.tree.sync()

client = FunnyBadge(intents=Intents.none())


@client.event
async def on_ready():
    
    print(inspect.cleandoc(f"""
        Invite link for {client.user}:
        https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot 
    """), end="\n\n")
    

@client.tree.command()
async def hello(interaction: Interaction):
    """ Say hello to the bot! """
    
    print(f' {interaction.user} used command "Hello".')
 
    await interaction.response.send_message(inspect.cleandoc(f"""
        Hi **{interaction.user}**, you will get the badge soon!
        >  
        > __**Claim your badge!**__
        > 
        > Claim your badge here: https://discord.com/developers/active-developer 
    """))

client.run(token)
