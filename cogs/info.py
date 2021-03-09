import discord
from os import getenv 
from discord.ext import commands
from typing import Optional
from discord import Member
from pymongo import MongoClient
from datetime import datetime


cluster = MongoClient(getenv("WARN_PASS")) # Don't include "<" and ">" fill in those with your credentials
collection = cluster.drgamer.drgamer

predb = cluster["discord"]["prefix"]

class Info(commands.Cog):
	def __init__(self,client):
		self.client = client


	@commands.command()
	async def totalcmds(self,ctx):
		await ctx.send(f'There are {len(self.client.commands)} commands')

	@commands.command(aliases=['guilds', 'my_guilds', 'listguilds', 'servers', 'my_servers'], hidden=False)
	async def list_guilds(self, ctx, member:discord.Member=None,*,message = None):
		''' Returns a list of servers where Hokage is a member '''
		if ctx.author.id == 569105874912804874:
			temp_txt, index = '', 0
			async for guild in self.client.fetch_guilds(limit=150):
					index += 1
					temp_txt = temp_txt + \
							f'**{index})** {guild.name}\n'
			embed = discord.Embed(title=f"{self.client.user.display_name}\'s Servers", colour=discord.Colour(
					0xE5E242), description=temp_txt)

			embed.set_image(
					url="https://image.shutterstock.com/image-vector/yay-vector-handdrawn-lettering-banner-260nw-1323618563.jpg")

			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			await ctx.channel.purge(limit=1)
			await ctx.author.send(embed=embed)
		else:
			await ctx.send('You are not eligible for this command')

	@commands.command(aliases=['UI','ui','Ui','USERINFO','Userinfo','info','INFO','Info','UserInfo'])
	async def userinfo(self,ctx, target: Optional[Member]):
		target = target or ctx.author

		embed=discord.Embed(title='User Information',colour=target.colour,timestamp=datetime.utcnow())

		embed.set_thumbnail(url=target.avatar_url)

		fields = [("ID", target.id, False),
							("Name", str(target),True),
							("Bot?", target.bot, True),
							("Top role",target.top_role.mention, True),
							("Status", str(target.status).title(), True),
							("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
							("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True)]

		for name,value,inline in fields:
			embed.add_field(name=name,value=value,inline=inline)

		embed.set_footer(text=f'FBI agent:{ctx.author.name}',icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

	
	# @commands.command(aliases=['SI','si','Si','SERVERINFO','Serverinfo','ServerInfo'])
	# async def serverinfo(self,ctx):
	# 	embed=discord.Embed(title='Server Information',colour=ctx.guild.owner.colour,timestamp=datetime.utcnow())

	# 	embed.set_thumbnail(url=ctx.guild.icon_url)

	# 	fields = [("🆔ID",ctx.guild.id, True),
	# 						("👑Owner",ctx.guild.owner.mention, True),
	# 						(":earth_asia:Region",ctx.guild.region, True),
	# 						(":alarm_clock:Created at",str(ctx.guild.created_at)[0:11], True),
	# 						(":100:Members",len(ctx.guild.members), True),
	# 						(":man:Humans",len(list(filter(lambda m: not m.bot,ctx.guild.members))),True),
	# 						("🤖Bots",len(list(filter(lambda m:m.bot,ctx.guild.members))),True),
	# 						("❌Banned members",len(await ctx.guild.bans()),True),
	# 						("📜Text Channels",len(ctx.guild.text_channels),True),
	# 						("🎵Voice Channels",len(ctx.guild.voice_channels),True),
	# 						("🗃️Categories",len(ctx.guild.categories),True),
	# 						("🤴Roles",len(ctx.guild.roles),True),
	# 						("\u200b","\u200b",True),]

	# 	for name,value,inline in fields:
	# 		embed.add_field(name=name,value=value,inline=inline)

	# 	embed.set_footer(text=f'FBI agent:{ctx.author.name}',icon_url=ctx.author.avatar_url)
	# 	await ctx.send(embed=embed)

	
	@commands.command(aliases=["si", "serverinfo"])
	async def server(self, ctx):
			own = ctx.guild.owner
			reg = str(ctx.guild.region)
			tim = str(ctx.guild.created_at)
			txt = len(ctx.guild.text_channels)
			vc = len(ctx.guild.voice_channels)
			embed = discord.Embed(
					timestamp=ctx.message.created_at,
					title="Server Info",
					color=0xFF0000,
			)
			embed.add_field(name=":ballot_box: Name", value=f"{ctx.guild}")
			embed.add_field(name=":crown: Owner", value=f"{own.mention}")
			embed.add_field(
					name=":person_red_hair:Members",
					value=f"{ctx.guild.member_count}",
			)
			embed.add_field(
					name=":airplane:Region", value=f"{reg.capitalize()}"
			)
			embed.add_field(name=":alarm_clock:Created At", value=f"{tim[0:11]}")
			embed.add_field(
					name=":speech_balloon:Text Channels", value=f"{txt}"
			)
			embed.add_field(
					name=":loud_sound:Voice Channels", value=f"{vc}"
			)
			embed.set_footer(
					text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
			)

			embed.set_thumbnail(url=ctx.guild.icon_url)

			await ctx.send(embed=embed)

	@commands.command(aliases=['git'])
	async def github(self,ctx):
		embed=discord.Embed(title='Check my GitHub',description='[Click Here](https://github.com/Drgamer005/Hokage-Discord-Bot)',colour=discord.Colour.blue())  
		await ctx.send(embed=embed)


	@commands.command(aliases=['INVITE','Invite'])
	async def invite(self,ctx):
		embed=discord.Embed(title='Invite Me here',description='[Click Here](https://discord.com/api/oauth2/authorize?client_id=797519687147585546&permissions=0&scope=bot)',colour=discord.Colour.blue())  
		await ctx.send(embed=embed)


def setup(client):
  client.add_cog(Info(client))