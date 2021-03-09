import discord
from discord.ext import commands
import json


class Help(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.command(aliases=['HELP','Help'])
	async def help(self,ctx,choice=None):

		try:
			with open('prefixes.json','r') as f:
				prefixes = json.load(f)

			pre = prefixes[str(ctx.guild.id)]

		except:
			pre = '--'

		if choice == None:

			embed=discord.Embed(title='Hokage Commands',colour=discord.Colour.blue())
			embed.add_field(name='```These are my help catagories```',value='``help general``\n``help anime``\n``help economy``\n``help admin``\n``help music``\n``help images``\n``help bot``\n``help extra``')
			embed.set_footer(text=f'Use command prefix "{pre}"',icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

		elif choice.lower() == 'general':

			embed=discord.Embed(title='Help General',description='This shows all the general commands',colour=discord.Colour.blue())
			embed.add_field(name='Commands',value='`Avatar - Sends the avatar of a person`\n`botintro - Introduces the bot`\n`Ping - Sends the latency of bot`\n`Wasted - Wastes a picture of any persons avatar you choose`\n`userinfo - sends info about a person`\n`mem - Shares the total amount of people in the server`\n`meme - Gives a random meme from reddit`\n`spam - spams a something u want to spam a huge number of times`\n`snipe - shows the last deleted message`\n`Rps - play a game of rock paper scissor with the bot`\n`Dm - send a dm to someone`\n`fancytext - writes a message u tell it to in a fancy way`\n`serverinfo - tells u stats about that server`')
			embed.set_footer(text=f'Use command prefix "{pre}" ',icon_url=ctx.author.avatar_url)
			
			await ctx.send(embed=embed)

		elif choice.lower() == 'images':
			embed=discord.Embed(title='Help Images',description='This shows all the fun anime commands',colour=discord.Colour.blue())
			embed.add_field(name='Commands',value='`funlist - shows a list of fun image commands`\n`wanted - takes a users photo and makes him a wanted criminal`')
			embed.set_footer(text=f'Use command prefix "{pre}" ',icon_url=ctx.author.avatar_url)

			await ctx.send(embed=embed)

		elif choice.lower() == 'anime':
			embed=discord.Embed(title='Help Anime',description='This shows all the fun anime commands',colour=discord.Colour.blue())
			embed.add_field(name='Commands',value='`!!!!!!!!!!!!!!!!!!!!!!!IN PROGRESS!!!!!!!!!!!!!!!!!!!!!!!!!!!!`')
			embed.set_footer(text=f'Use command prefix "{pre}" ',icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

		elif choice.lower() == 'admin':
			embed=discord.Embed(title='Help Admin',description='This shows all the admin commands',colour=discord.Colour.blue())
			embed.add_field(name='Commands',value='`kick - kicks a user(will work only if bot and user have perms)`\n`ban - bans a user(will work only if bot and user have perms)`\n`Unban - will unban a member who is banned`\n`addrole - adds a role to user`\n`removerole - removes a role from a user`\n `warn - warn a member for unauthorized behaviour`\n`clearwarns - clear all the warns for a particular user`\n`case - tells a users currect case of warns`\n`jishaku - get the bot code of a cmd`')
			embed.set_footer(text=f'Use command prefix "{pre}" ',icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

		elif choice.lower() == 'extra':
			embed=discord.Embed(title='Help Extra',description='This shows all the extra commands',colour=discord.Colour.blue())
			embed.add_field(name='Commands',value='`clear - clears recent messages`\n`botinfo - tells u stats about the bot`\n`servers - tells u all servers the bot is in`\n`totalcmds- tells the total number of cmds the bot has`\n`help - shows u these catagories to pick from`')
			embed.set_footer(text=f'Use command prefix "{pre}" ',icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)


		elif choice.lower() == 'economy':
			embed=discord.Embed(title='Help economy',description='This shows all the economy commands',colour=discord.Colour.blue())
			embed.add_field(name='Commands',value='`beg - gives u a randoom number of coins for begging`\n`bal - tells ur account balance`\n`dep - dep a certain amount of coins in bank`\n`with - withdraws a certain amount of coins from bank`\n`slots - plays a game of slots where if u win u get coins`\n`rob - rob a user `\n`give - give a user coins or an item`\n`buy - buy something from the shop`\n`sell - sell something from ur inventory`\n`shop - shows the items in shop`\n`inv - shows ur inventory`\n`leaderboard - sends the leaderboard of rich ppl`')
			embed.set_footer(text=f'Use command prefix "{pre}" ',icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)


		elif choice.lower() == 'music':
			embed=discord.Embed(title='Help Music',description='Shows All The Music Commands',colour=discord.Colour.blue())
			embed.add_field(name='Commands',value='`play - plays a song that u ask it to`\n`pause - pauses the current song`\n`resume - resumes the current song`\n`skip - skips to the next song`\n`join - makes the bot join ur vc`\n`leave - makes the bot leave ur vc`\n`stop - stops the current song and clear queue`\n`queue - shows the queue`\n`remove - remove a song from the queue`\n`shuffle - shuffles the queue`\n`now - tells the current song playing`\n`summon - summon the bot from another channel`')
			embed.set_footer(text=f'Use command prefix "{pre}" ',icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

		elif choice.lower() == 'bot':
			embed=discord.Embed(title='Help bot',description='Info commands',colour=discord.Colour.blue())
			embed.add_field(name='commands...',value="`invite - invite Hokage to your server`\n`GitHub - see Gaara's GitHub page and star repo`")
			embed.set_footer(text=f'Use command prefix "{pre}" ',icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

		else:
			await ctx.send('No help command found try typing ***help*** for more info')

  
	@commands.command()
	async def help2(self,ctx):
		helptext = "`"
		for command in self.client.commands:
				helptext+=f"{command}\n"
		helptext+="`"
		await ctx.send(helptext)

def setup(client):
  client.add_cog(Help(client))