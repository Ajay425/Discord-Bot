import discord 
import requests
import json
import random
from replit import db

intents=discord.Intents.default()
intents.members=True
client=discord.Client(intents=intents)

sad_words=["sad","depressed","angry","irritating","unhappy"]

cheer=["You're Doing well", "Please dont be harsh on your're self"," You'll be fine"]


def update_bot(cheering):
  if "cheer" in db.keys():
    cheer=db["cheer"] #gets key from database
    cheer.append(cheering) # adds a cheer quote
    db["cheer"]=cheer
  else:
    db["cheer"] = [cheer]


def delete_msg(index):
  cheer=db["cheer"]
  if len(cheer) > index:
    del cheer[index] #deletes a cheer quote
    db["cheer"]=cheer 

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q'] +" -" + json_data[0]['a']
  return (quote)

@client.event
async def on_ready():
  print("Bot is ready to go {0.user}".format(client))
  channel=client.get_channel(863616382146838568)
  await channel.send("Hello There, I`ve Just connected here")


# when bot recives message

@client.event
async def on_message(message):
  #check if message from self
  if(message.author==client.user):
    return

  if message.content.startswith("$hello"):
    await message.channel.send("Welcome User") #sends message to when command triggered 
  if message.content=="$private":
    await message.author.send("Hello in private User")

  if message.content.startswith("$Ping"):
    await message.channel.send("<@794103895773282344>, How are you")

  if message.content.startswith("Haig"):
    await message.channel.send("<@338016845951008778> Hi User how are you")
  
  
  if message.content.startswith("$inspire"):
    quote=get_quote()
    await message.channel.send(quote)

  options=cheer
  if "cheers" in db.keys():#checks if starting cheer is in the database
    options=options+db.keys["cheer"]
  
  if any(word in message.content for word in sad_words):
    await message.channel.send(random.choice(options))
    
  if message.content.startswith("$new"):
    cheer=message.content.split("$new",1)[1] 
    update_bot(cheer)
    await message.channel.send("New message added")



  if message.content.startswith("$delete"):
    cheers={} # 
    if "cheer" in db.keys():
      index = int(message.content.split("$delete",1)[1])
      delete_msg(index)
      cheer=db["cheer"]
    await message.channel.send(cheer)

@client.event
async def on_member_join(member):
  guild=client.get_guild(947560890847330376)
  channel=guild.get_channel(970103516779667466)
  await channel.send(f"Welcome to the server {member.mention}. Hope you have a fun time around") #welcome a member
  await member.send(f"Welcome to the {guild.name} server. Hope you have a fun time around {member.name}")
  
# to run the bot

client.run('Your token')
