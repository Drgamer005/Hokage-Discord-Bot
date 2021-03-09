from os import getenv
import discord
from discord.ext import commands
from pymongo import MongoClient
import asyncio


cluster = MongoClient(getenv("MONGO")) # Don't include "<" and ">" fill in those with your credentials
collection = cluster.dr.dr

class Warn(commands.Cog):
	def __init__(self,client):
		self.client = client


	@commands.command(aliases=['WARN','Warn'])
	@commands.has_permissions(ban_members=True)
	async def warn(self,ctx,member:discord.Member=None):
		

		if member == None:
			await ctx.send('How should i warn if thers no one to warn dumb')
			return

		warnstats = collection.find_one({"guild":ctx.guild.id,"member": member.id})

		if member.top_role > ctx.author.top_role:
			await ctx.send('Respect ur seniors dont try to ban them!!')

		elif member.id == ctx.author.id:
			await ctx.send('Why u tryng to ban urself hmm')

		elif member.bot:
			await ctx.send('Cannot warn Bot! No use!')

		elif not warnstats:
			collection.insert_one({"guild":ctx.guild.id,"member":member.id,"warns":1})

			async with ctx.typing():
				await ctx.send(f'Warned {member.mention}, now has 1 warn')

		else:
			if warnstats['warns'] >= 4:
				await member.ban(reason='Given warning but did not listen')
				await ctx.send(f'{member.mention} got banned for ignoring warns')
				collection.remove({"guild":warnstats['guild'],"member":warnstats['member']})

			else:
				warnstats['warns'] += 1

				async with ctx.typing():
					await ctx.send(f'Warned {member.mention}, has {warnstats["warns"]} warns ')



				collection.replace_one({"guild":warnstats['guild'],"member":warnstats['member']},{"guild":warnstats['guild'],"member":warnstats['member'],"warns":warnstats['warns']})

	@commands.command(aliases=['CASE','Case'])
	async def case(self,ctx,member:discord.Member=None):
		if member == None:
			member = ctx.author

		warnstats = collection.find_one({"guild":ctx.guild.id,"member": member.id})

		if not warnstats:
				await ctx.send('No Data Found')

		else:
			
				embed=discord.Embed(title='Warns',description=f'{member.mention} has {warnstats["warns"]} warns',colour=discord.Colour.blue())
				await ctx.send(embed=embed)

	@commands.command(aliases=['cw'])
	@commands.has_permissions(ban_members=True)
	async def clearwarns(sself,ctx,member:discord.Member):
		warnstats = collection.find_one({"guild":ctx.guild.id,"member": member.id})
		if not warnstats:
			
				embed=discord.Embed(title='Error',description='Nothing To clear',colour=discord.Colour.blue())
				await ctx.send(embed=embed)

		elif member.id == ctx.author.id:
			await ctx.send('U cant clear ur own warns')

		else:
			#bankinfo['warns'] = 0
			collection.remove({"guild":warnstats['guild'],"member":warnstats['member']})#bruh let me fork this and run

			embed=discord.Embed(title='Cleared!',description=f'Data Cleared for {member.mention}',colour=discord.Colour.blue())
			await ctx.send(embed=embed)


def setup(client):
  client.add_cog(Warn(client))
	