
import json
import random
from keep_alive import keep_alive
import os
import openai
import logging
import discord
import requests
import asyncio
import datetime
from replit import db

openai.api_key = " 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"

allowed_categories = ["business","world","technology","sports","science","politics","environment","top"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
  if message.author == client.user:
        return
  member_id = message.author.id
  member_name = message.author.name
  channel_id = message.channel.id

  if message.content.startswith('$apod'):
    response = requests.get(
      "https://api.nasa.gov/planetary/apod?api_key=JuwvfjFyYOzdMNqydhcXyIHr4gwGp5IVc4qsJhSE"
    ).json()

    embed = discord.Embed(title=response["title"],
                          description=response['explanation'],
                          color=0x008080)
    embed.set_image(url=response['url'])
    sent_message = await message.channel.send(embed=embed)
    await sent_message.add_reaction("\U0001F929")

  if message.content.startswith('$launches'):
    response = requests.get(
      "https://fdo.rocketlaunch.live/json/launches/next/5").json()
    launches = response["result"]
    color = random.randint(0, 0xffffff)
    embed = discord.Embed(title="Upcoming Rocket Launches", color=color)

    for launch in launches:
      name = launch["launch_description"]
      pad = launch["pad"]
      description = pad["location"]
      mission = launch["missions"]
      mission_name = mission[0]["name"]
      provider2 = launch["provider"]["name"]

      if description["country"] == "United States":

        if provider2 == "ULA":
          link = "https://www.youtube.com/user/UnitedLaunchAlliance/videos"
          country = "🇺🇸️"
        elif provider2 == "SpaceX":
          link = "https://www.youtube.com/@SpaceX"
          country = "🇺🇸️"
        elif provider2 == "RocketLab":
          link = "https://www.youtube.com/@RocketLabNZ"
          country = "🇺🇸️🇳🇿️"
        elif provider2 == 'NASA':
          link = "https://www.youtube.com/@NASA"
          country = "🇺🇸️"
        else:
          link = "https://www.youtube.com/@NASA"
          country = "🇺🇸️"

      elif description["country"] == "India":
        country = "🇮🇳️"
        link = "https://www.youtube.com/@isroofficial5866"

      elif description["country"] == "China":
        country = "🇨🇳️"
        link = f"https://www.google.com/search?q={mission_name + ' launch'}"

      elif description["country"] == "Japan":
        country = "🇯🇵️"
        link = "https://www.youtube.com/@JAXA-PR/streams"

      elif description["country"] == "Russia" or "Kazakhstan":
        country = "🇷🇺️"
        link = "https://www.youtube.com/@tvroscosmos/featured"
      elif description["country"] == "Europe":
        country = "🇪🇺️"
        link = "https://www.youtube.com/@EuropeanSpaceAgency/featured"
      else:
        country = "🌏️"
        link = f"https://www.google.com/search?q={mission_name + ' launch'}"

      embed.add_field(name=name,
                      value=f"{description['name']}  {country}    {link}",
                      inline=False)

    sent_message = await message.channel.send(embed=embed)
    for i in range(len(launches)):
      await sent_message.add_reaction(f"{i + 1}\u20e3")

  
  if message.content.startswith('$news'):
    
    result = [i for sub in message.content.split("-") for i in sub.split("#")]

    keyword = result[1]
    if keyword == "":
      response = requests.get(
      "https://newsdata.io/api/1/news?apikey=pub_16464c67300e3900fe3c92a05fdf67ddf525a&language=en&qInTitle=astronomy%20OR%20nasa%20OR%20spacex"
    ).json()
      news_defaults = response["results"]
      color = random.randint(0, 0xffffff)
      embed = discord.Embed(title="Astronomy News", color=color)
      for news_default in news_defaults:
        name = news_default["title"]
        link = news_default["link"]
        description = news_default["description"]
        description = str(description) if description else ""
        truncated_description = description[:300]
        embed.add_field(name=name,
                      value=f"{truncated_description}...\n{link}",
                      inline=False)

      sent_message = await message.channel.send(embed=embed)
      
    

    

    if keyword == "india":
      number_of_pages = result[2]
      logging.critical(number_of_pages)
      api_link="https://newsdata.io/api/1/news?apikey=pub_16464c67300e3900fe3c92a05fdf67ddf525a&language=en&country=in&page="
      if number_of_pages == "1":
        logging.critical('This is an info message 1')
        response = requests.get(api_link).json()
        news_defaults = response["results"]
        color = random.randint(0, 0xffffff)
        embed = discord.Embed(title="India News", color=color)
        next_page = response["nextPage"]
        
        for news_default in news_defaults:
          name = news_default["title"]
          link = news_default["link"]
          description = news_default["description"]
          description = str(description) if description else ""
          truncated_description = description[:300]
          embed.add_field(name=name,
                      value=f"{truncated_description}...\n{link}",
                      inline=False)

          

        sent_message = await message.channel.send(embed=embed)
      
      if number_of_pages != "1":
        logging.critical('This is an info message 2')
        response = requests.get(api_link).json()
        next_page = response["nextPage"]
        for x in range(2,int(number_of_pages)+1):
          api_link=f"https://newsdata.io/api/1/news?apikey=pub_16464c67300e3900fe3c92a05fdf67ddf525a&language=en&country=in&page={next_page}"
          response = requests.get(api_link).json()
          next_page = response["nextPage"]
        
        
        news_defaults = response["results"]
        color = random.randint(0, 0xffffff)
        embed = discord.Embed(title="India News", color=color)
        next_page = response["nextPage"]
        
        for news_default in news_defaults:
          name = news_default["title"]
          link = news_default["link"]
          description = news_default["description"]
          description = str(description) if description else ""
          truncated_description = description[:300]
          embed.add_field(name=name,
                      value=f"{truncated_description}...\n{link}",
                      inline=False)

        sent_message = await message.channel.send(embed=embed)
        
    if keyword in allowed_categories:
      number_of_pages = result[2]
      logging.critical(number_of_pages)
      api_link=f"https://newsdata.io/api/1/news?apikey=pub_16464c67300e3900fe3c92a05fdf67ddf525a&language=en&category={keyword}"+"&page="
      if number_of_pages == "1":
        logging.critical('This is an info message 1')
        response = requests.get(api_link).json()
        news_defaults = response["results"]
        color = random.randint(0, 0xffffff)
        embed = discord.Embed(title= keyword.title() + " News", color=color)
        next_page = response["nextPage"]
        
        for news_default in news_defaults:
          name = news_default["title"]
          link = news_default["link"]
          description = news_default["description"]
          description = str(description) if description else ""
          truncated_description = description[:300]
          embed.add_field(name=name,
                      value=f"{truncated_description}...\n{link}",
                      inline=False)

          

        sent_message = await message.channel.send(embed=embed)
      
      if number_of_pages != "1":
        logging.critical('This is an info message 2')
        response = requests.get(api_link).json()
        next_page = response["nextPage"]
        for x in range(2,int(number_of_pages)+1):
          api_link=f"https://newsdata.io/api/1/news?apikey=pub_16464c67300e3900fe3c92a05fdf67ddf525a&language=en&category={keyword}&page={next_page}"
          response = requests.get(api_link).json()
          next_page = response["nextPage"]
        
        
        news_defaults = response["results"]
        color = random.randint(0, 0xffffff)
        embed = discord.Embed(title= keyword.title() + " News", color=color)
        next_page = response["nextPage"]
        
        for news_default in news_defaults:
          name = news_default["title"]
          link = news_default["link"]
          description = news_default["description"]
          description = str(description) if description else ""
          truncated_description = description[:300]
          embed.add_field(name=name,
                      value=f"{truncated_description}...\n{link}",
                      inline=False)

        sent_message = await message.channel.send(embed=embed)
# @client.event
# async def on_member_join(member):
#     channel = discord.utils.get(member.guild.text_channels, name="general")
#     if channel is not None:
#         embed = discord.Embed(title="Welcome!", description=f"{member.mention} has joined the server!", color=0x00ff00)
#         await channel.send(embed=embed)

  if message.content.startswith('$chat'):
    member_message = message.content.split("-")[1]
    openai.api_key = "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"
    
    model_engine = "text-davinci-003"
    
    
    prompt = f"  I'm using the chatGPT api in my discord bot named R2D2 so whatever response you generate for the particular member of the discord server act like you are R2D2 and address them with their member name here i will provide you the member_name and member_message;{member_name} : {member_message}; reminder whenever you use the member_name do not forget to add @ before the member name"


    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    embed = discord.Embed(
      
    description=response,
    
)

    embed.set_author(name=f"To {member_name}", icon_url=message.author.display_avatar)
    # embed.timestamp = datetime.datetime.utcnow()
    await message.channel.send(embed=embed)


# @client.event
# async def on_ready():
#     client.loop.create_task(check_birthday())


  


  if message.content.startswith('$dob'):
    member_dob = message.content.split("-")[1]
    print(member_dob)
    if len(member_dob) != 6:
        await message.channel.send("Error: Please enter a valid DOB in the format of `ddmmyy` with 6 digits")
        return

    day = int(member_dob[:2])
    month = int(member_dob[2:4])
    year = int(member_dob[4:])

    try:
        date = datetime.datetime(year + 2000, month, day)
    except ValueError:
        await message.channel.send("Error: Please enter a valid date")
        return
    birthday = member_dob
    member_id = message.author.id
    db[member_id] = birthday 
    logging.critical("done")
    await message.channel.send("Value Updated / Stored")
    


@client.event
async def on_member_join(member):
    embed = discord.Embed(
    title = f"Welcome to the server {member.name}. Please type in your Date Of Birth in DDMMYY format"
    
)
    embed.set_thumbnail(url=member.avatar)

   
   
    await member.send(embed=embed)
    def check(m):
        if len(m.content) != 6:
            return False
        if not m.content.isdigit():
            return False
        day = int(m.content[:2])
        month = int(m.content[2:4])
        if day < 1 or day > 31 or month < 1 or month > 12:
            return False
        return m.author == member
    message = await client.wait_for('message', check=check)
    logging.critical(message.content)
    birthday = message.content
    member_id = member.id
    db[member_id] = birthday 
    logging.critical("done")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    for guild in client.guilds:
        text_channel = guild.text_channels[0]
        channel_id = text_channel.id
        break
    while True:
        now = datetime.datetime.now()
        for member_id in db:
            birthday = db[member_id]
            day = int(birthday[:2])
            month = int(birthday[2:4])
            if now.day == day and now.month == month:
              for guild in client.guilds:
                member = guild.get_member(int(member_id))
                print(member)
                print(f'Found the member: {member.name} with ID: {member.id}')
                
                embed = discord.Embed(
                    title = "Many more Happy returns of the day ,"+ member.name,
                    description = "Beep boop beep,May the force of the universe be with you on your special day! May you have an intergalactic celebration filled with starry adventures, far-off explorations, and an infinite supply of happiness. Happy Birthday, space adventurer! Beep boop beeeeeeep ",color=0xff0000
                )
                embed.set_image(url="https://i.pinimg.com/originals/06/51/b5/0651b524d630d440ff7f87fab79d00b3.gif")
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="May the Force be with You ...!",
                                value="enjoy",
                      
                      inline=False)
                
                channel = client.get_channel(channel_id)
                await channel.send(embed=embed)
            else:
              print("nobody")
        await asyncio.sleep(86000)


# async def check_birthday():
#     while True:
#         now = datetime.datetime.now()
#         for member_id, birthday in db.items():
#             if now.strftime("%d%m") == birthday[:4]:
                
#                 member = client.get_user(member_id)
#                 await member.send("Happy Birthday!")
#         await asyncio.sleep(60) # sleep for 1 hour  







keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)
