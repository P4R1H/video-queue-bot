#code for bot testing, omnithicc#5205


#importing directories

import discord
from discord.ext import commands
import os
import asyncpraw
import asyncio


#reddit login credentials

reddit = asyncpraw.Reddit(client_id=os.getenv("id"),
                          client_secret=os.getenv("ab"),
                          username=os.getenv("username"),
                          password=os.getenv("pass"),
                          user_agent=os.getenv("ef"))

#setting default command

client = commands.Bot(command_prefix="-")

#client.event from here


@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))




#client.command from here




infinitelooper = 0


@client.command()
async def logs(ctx):
    subreddit = await reddit.subreddit("spacejesus_testingsub")   
    
    with open("lastaction.txt", "r") as f: #reading where we last left off
      lastactionid = f.read()


    
    while infinitelooper == 0:
      async for log in subreddit.mod.log(limit = None, params = {"before": lastactionid}):

          em = discord.Embed(title=(f"Moderator action by {log.mod}"))
         
          templinkname = f"https://reddit.com{log.target_permalink}"

          
          em.add_field(name="Post title", value= log.target_title)
          
          if log.target_author == "": 
            pass
          else:
            em.add_field(name="Post author", value=log.target_author)

          em.add_field(name="Action", value=log.action)
          em.add_field(name = "Perma link",value = "[link]({})".format(templinkname)) 

          
          
          
          with open("lastaction.txt", "w") as f: #storing the last id in file so it can resume from where it left
            f.truncate(0)
            f.write(log.id)

          lastactionid = log.id
          

          await ctx.send(embed=em)





@client.command()
async def adminlogs(ctx):
    subreddit = await reddit.subreddit("spacejesus_testingsub")   
    
    with open("lastadminaction.txt", "r") as f: #reading where we last left off
      lastadminactionid = f.read()


    
    while infinitelooper == 0:
      async for log in subreddit.mod.log(limit = None, params = {"before": lastadminactionid}):
          

          if log.mod == "ManWalkingDownReddit":
            
            templinkname = f"https://reddit.com{log.target_permalink}"
            
            em = discord.Embed(title = "Admin action", color = discord.Color.red())
            em.add_field(name="Action", value=log.action)
            em.add_field(name="Post title", value= log.target_title)
            em.add_field(name = "Perma link",value = "[link]({})".format(templinkname)) 
            
            
            if log.target_author == "": 
              await ctx.send(embed = em)
              continue
            else:
              em.add_field(name="Post author", value=log.target_author)
  
          
            with open("lastadminaction.txt", "w") as f: #storing the last id in file so it can resume from where it left
              f.truncate(0)
              f.write(log.id)

            lastadminactionid = log.id

            await ctx.send(embed=em)
          else:
            pass


@client.command()
async def q(ctx):
  print("started")
  sub = await reddit.subreddit("shitposting")
  while(1):
    #print("running")
    try:
      async for item in sub.mod.modqueue("submissions"): # can also be streamed
          #print(item.permalink)


    


          if item.post_hint == "hosted:video":
            em= discord.Embed(title = f"New video by {item.author}")
            em.add_field(name = "Title", value = item.title)

            reports = []

            if len(item.user_reports) != 0:

              for i in range(len(item.user_reports)):
                reports.append(f"({i+1})  ")
                reports.append(item.user_reports[i][0])
                reports.append(f":   {item.user_reports[i][1]} ")
              
              str1 = ''.join(reports)

            else:
              str1 = "None"




            em.add_field(name = "Reports", value = str1)

            print("found video")
            

            tempbed = await ctx.send(embed = em)
            video = await ctx.send(f"https://reddit.com{item.permalink}")
            
            await video.add_reaction("<:approve:882512051518464010>")
            
            await video.add_reaction("<:remove:882512074696175626>")

            await video.add_reaction("<:NSFW:882545649239883796>")
          
            await video.add_reaction("<a:ban:882547149873774613>")


            approve = '<:approve:882512051518464010>'
            remove = '<:remove:882512074696175626>'
            marknsfw = '<:NSFW:882545649239883796>'
            ban = '<a:ban:882547149873774613>'

            valid_reactions = ['<:approve:882512051518464010>','<:remove:882512074696175626>','<:NSFW:882545649239883796>', "<a:ban:882547149873774613>"]

            approvedusers = [532423802710261760, 617021192011776000,214216187901378560,272642876557492224,189149892533288960,633313464227594280,690646404888002671,339870301024157697,408441877189230593,742835030849749063,347046346714513420,194536386618064896,532423802710261760,251800306176884736,486691601876254730,274349398060695554,703258999143006290,648262760576057354,803140928960987137]

            def check(reaction, user):
              return user.id in approvedusers and str(reaction.emoji) in valid_reactions and reaction.message == video 


            reaction, user = await client.wait_for('reaction_add', check=check)


            if str(reaction.emoji) == approve:
              await item.mod.approve()
              confirmation = await video.reply("approved!")
              await asyncio.sleep(2)
              await video.delete()
              await asyncio.sleep(1)
              await confirmation.delete()
              new_emb = discord.Embed(title = f"Video approved by {user}", color = discord.Color.green())
              new_emb.add_field(name = "OP", value = item.author)
              new_emb.add_field(name = "Post", value = "[Link](https://reddit.com{}) ({})".format(item.permalink, item.id))
              await tempbed.edit(embed = new_emb)    
              print(5/0)

            elif str(reaction.emoji) == remove:
              await item.mod.remove()
              confirmation = await video.reply("removed.")
              await asyncio.sleep(1)
              await video.delete()
              await asyncio.sleep(1)
              await confirmation.delete()
              new_emb = discord.Embed(title = f"Video removed by {user}", color = discord.Color.red())
              new_emb.add_field(name = "OP", value = item.author)
              new_emb.add_field(name = "Post", value = "[Link](https://reddit.com{}) ({})".format(item.permalink, item.id))
              await tempbed.edit(embed = new_emb)   
              print(5/0) 

            elif str(reaction.emoji) == marknsfw:    
              await item.mod.nsfw()    
              await item.mod.approve()
              confirmation = await video.reply("marked nsfw!")
              await asyncio.sleep(1)
              await video.delete()
              await confirmation.delete()
              new_emb = discord.Embed(title = f"Video marked nsfw  by {user}", color = 16737894)
              new_emb.add_field(name = "OP", value = item.author)
              new_emb.add_field(name = "Post", value = "[Link](https://reddit.com{}) ({})".format(item.permalink, item.id))
              await tempbed.edit(embed = new_emb)   
              print(5/0) 

            elif str(reaction.emoji) == ban:

              banemb = discord.Embed(title = f"ban u/{item.author}")

              banselect = await ctx.send(embed = banemb)

              sevendays = "<:7days:882552324394979348>"
              thritydays = "<:30days:882552504003485696>"
              perma = "<:perma:882552177887969292>"
              cancelandapprove = "<:cancelandapprove:882567219484192789>"

              await banselect.add_reaction("<:7days:882552324394979348>")
              await banselect.add_reaction("<:30days:882552504003485696>")
              await banselect.add_reaction("<:perma:882552177887969292>")
              await banselect.add_reaction("<:cancelandapprove:882567219484192789>")

              ban_reactions = ["<:perma:882552177887969292>", "<:7days:882552324394979348>","<:30days:882552504003485696>", "<:cancelandapprove:882567219484192789>"]

              def bancheck(reaction, user):
                return user.id in approvedusers and str(reaction.emoji) in ban_reactions and reaction.message == banselect 
                


              reaction, user = await client.wait_for('reaction_add', check=bancheck)

              if str(reaction.emoji) == sevendays:

                await sub.banned.add(item.author, ban_reason= f"https://reddit.com{item.permalink}", duration = 7)

                await item.mod.remove()

                confirmationban = await video.reply("banned user for 7 days.")
                await asyncio.sleep(1)
                await video.delete()
                await confirmationban.delete()
                await banselect.delete()
                new_emb = discord.Embed(title = f" {user} banned u/{item.author}", color = 6684672)
                new_emb.add_field(name = "Duration", value = "7 days" )
                new_emb.add_field(name = "Post", value = "[Link](https://reddit.com{}) ({})".format(item.permalink, item.id))
                await tempbed.edit(embed = new_emb)  
                print(5/0)
          
              if str(reaction.emoji) == thritydays:

                await sub.banned.add(item.author, ban_reason= f"https://reddit.com{item.permalink}", duration = 30)
                await item.mod.remove()

                confirmationban = await video.reply("banned user for 30 days.")
                await asyncio.sleep(1)
                await video.delete()
                await confirmationban.delete()
                await banselect.delete()
                new_emb = discord.Embed(title = f" {user} banned u/{item.author}", color = 6684672)
                new_emb.add_field(name = "Duration", value = "30 days" )     
                new_emb.add_field(name = "Post", value = "[Link](https://reddit.com{}) ({})".format(item.permalink, item.id))
           
                await tempbed.edit(embed = new_emb)   
                print(5/0) 


              if str(reaction.emoji) == perma:

                await sub.banned.add(item.author, ban_reason= f"https://reddit.com{item.permalink}")
                
                await item.mod.remove()   


                confirmationban = await video.reply("banned user permanently.")
                await asyncio.sleep(1)
                await video.delete()
                await confirmationban.delete()
                await banselect.delete()
                new_emb = discord.Embed(title = f" {user} banned u/{item.author}", color =6684672)
                new_emb.add_field(name = "Duration", value = "Permanant" )
                new_emb.add_field(name = "Post", value = "[Link](https://reddit.com{}) ({})".format(item.permalink, item.id))
                await tempbed.edit(embed = new_emb)  
                print(5/0)

              if str(reaction.emoji) == cancelandapprove:

                
                await item.mod.approve()   


                confirmationban = await video.reply("Cancelled ban action, approved post")
                await asyncio.sleep(1)
                await video.delete()
                await confirmationban.delete()
                await banselect.delete()
                new_emb = discord.Embed(title = f"Video approved by {user}", color = discord.Color.green())
                new_emb.add_field(name = "OP", value = item.author)
                new_emb.add_field(name = "Post", value = "[Link](https://reddit.com{}) ({})".format(item.permalink, item.id))
                await tempbed.edit(embed = new_emb) 
                print(5/0)                





            await asyncio.sleep(10)

          elif item.post_hint == "image":
            continue

            

         


    except:
      continue
  


@client.command(aliases=["gp"])
async def getpost(ctx, url):
  try:
    submission = await reddit.submission(id = url)
    await ctx.send(f"https://reddit.com{submission.permalink}")

  except:
    em = discord.Embed(title = f"{url} is not a valid post id", color = discord.Color.red())

    em.set_footer(text = "Examples of valid post ids are paq851, pd4ord etc ", icon_url = "https://cdn.discordapp.com/emojis/882157424990122015.gif?v=1")
    await ctx.send(embed = em)



#to know all the attributes of a command, do print(vars(<command>))
#running bot with token

client.run(os.getenv("token"))
