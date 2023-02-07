
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
import pynacl
from replit import db
import youtube_dl
import music
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}



@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")



@client.event
async def on_message(msg):
    if msg.content.startswith("?play"):

        try:
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        try:
            url = msg.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

            voice_clients[msg.guild.id].play(player)

        except Exception as err:
            print(err)


    if msg.content.startswith("?pause"):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)

    
    if msg.content.startswith("?resume"):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)

    
    if msg.content.startswith("?stop"):
        try:
            voice_clients[msg.guild.id].stop()
            await voice_clients[msg.guild.id].disconnect()
        except Exception as err:
            print(err)



# cogs = [music]

# client = commands.Bot(command_prefix="?",intents = discord.Intents.all())

# for i in range(len(cogs)):
#   cogs[i].setup(client)


# client.run("MTA2OTcxODQ3NzA1NDY4OTMzMA.GN44NM.w6tk6RbtNuUToAU8wsvVNX8F_ZfLco7_zK5PjY")


allowed_categories = ["business","world","technology","sports","science","politics","environment","top"]





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
    


  if message.content.startswith('$commands'):
    embed = discord.Embed(
    title = f"Here you Go ...!",)
    embed.set_thumbnail(url=message.author.avatar)
    embed.add_field(name = "Commands to Call me :",
                   value="1. $apod command gives you the Astronomy picture of the day released by NASA everyday \n 2.$launches gives you the list of upcoming rocket launches and the site to watch them! \n 3.$news- gives you with the Astronomy News but I dont stop there you can also get business, world, sports , science , top, entertainment news by typing $news-[topic you want]#1 this will give you the first page conatining ten articles for more just replace #1)\n 4.$chat- <your query> to chat with me. \n 5.$dob-<your dob in ddmmyy> to store the dob and wish you on your bday...!",inline = False)
    embed.add_field(name = "Rules to follow in the server :",
                   value="1. No Offensive messages \n 2.This is a server for Space Geeks so try to keep it that way \n 3.Only Healthy conversations \n 4.May the force be with you..!")

   
   
    await message.channel.send(embed=embed)

    
#   if message.content.startswith('!play'):
#         # Extract the song name
#         song_name = message.content[6:]
#         if not song_name:
#             await message.channel.send('Please specify a song name!')
#             return
#         if not song_name:
#             await message.channel.send('Please specify a song name!')
#             return

#         # Search for the song on YouTube
#         ydl_opts = {
#             'default_search': 'ytsearch',
#             # 'format': 'bestaudio/best',
#             # 'postprocessors': [{
#             #     'key': 'FFmpegExtractAudio',
#             #     'preferredcodec': 'mp3',
#             #     'preferredquality': '192',
#             # }],
#         }
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(song_name, download=False)
#             if 'formats' in info:
#                 stream_url = info['formats'][0]['url']
#             else:
#               await message.channel.send("Couldn't find an audio-only format for the song. Try searching for a different version.")
#             return

#         # Check if the user is in a voice channel
#         if message.author.voice is None:
#             await message.channel.send('Please join a voice channel first!')
#             return

#         # Join the user's voice channel
#         voice_channel = message.author.voice.channel
#         vc = await voice_channel.connect()

#         # Play the audio stream
#         vc.play(discord.FFmpegPCMAudio(stream_url), after=lambda e: print('done', e))
#         await message.channel.send(f'Playing: {info["title"]}')
@client.event
async def on_member_join(member):
    embed = discord.Embed(
    title = f"Welcome to the server {member.name}. Please type in your Date Of Birth in DDMMYY format",
    
    
)
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name = "Commands to Call me ...!",
                   value="1. $apod command gives you the Astronomy picture of the day released by NASA everyday \n 2.$launches gives you the list of upcoming rocket launches and the site to watch them! \n 3.$news- gives you with the Astronomy News but I dont stop there you can also get business, world, sports , science , top, entertainment news by typing $news-[topic you want]#1 this will give you the first page conatining ten articles for more just replace #1)\n 4.$chat- <your query> to chat with me. \n 5.$dob-<your dob in ddmmyy> to store the dob and wish you on your bday...!",inline = False)
    embed.add_field(name = "Rules to follow in the server",
                   value="1. No Offensive messages \n 2.This is a server for Space Geeks so try to keep it that way \n 3.Only Healthy conversations \n 4.May the force be with you..!")
    embed.set_image(url="https://media.tenor.com/ScSWQApVJyAAAAAC/space-dance-nasa.gif")                

   
   
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
