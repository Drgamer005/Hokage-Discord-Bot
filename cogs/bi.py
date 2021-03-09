import discord
from discord.ext import commands
from datetime import datetime
import asyncio
from aiohttp import ClientSession

class Dm(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.command()
	async def mhs(self, ctx, member : discord.Member, *, message : str):
			url = None
			webhooks = await ctx.channel.webhooks()
			for webhook in webhooks:
					if webhook.name == 'Hokage':
							url = webhook.url
			if url is None:
					webhook = await ctx.channel.create_webhook(name = 'Hokage')
					url = webhook.url
			async with ClientSession() as session:
					webhook = discord.Webhook.from_url(url, adapter = discord.AsyncWebhookAdapter(session))

					await ctx.channel.purge(limit=1)
					await webhook.send(content = message, username = member.name, avatar_url = member.avatar_url)
					await ctx.send('LOL')
					await asyncio.sleep(1)
					await ctx.channel.purge(limit=1)

	@commands.command(aliases=['BI','bi','Bi','BOTINFO','BotInfo'])
	async def botinfo(self,ctx):

		embed=discord.Embed(title='Bot Information',colour=discord.Colour.blue(),timestamp=datetime.utcnow())

		embed.set_thumbnail(url=self.client.user.avatar_url)

		mh = 0
		for i in self.client.guilds:
			
			mh += len([m for m in i.members if not m.bot])
			
		mh = mh - len(self.client.guilds)

		fields = [("🆔ID", 797519687147585546, True),
							(":trophy: Owner",'<@!569105874912804874>', True),
							("🤖Name", "Hokage",True),
							(":sunglasses: No. of servers", int(len(list(self.client.guilds))),True),
							('🦮Helping',f'{mh} members',True),
							("📝Invite me","[Click Here to Add Me](https://discord.com/api/oauth2/authorize?client_id=800219427928801290&permissions=8&scope=bot)",True)]
							

		for name,value,inline in fields:
			embed.add_field(name=name,value=value,inline=inline)

		embed.set_footer(text=f'FBI agent:{ctx.author.name}',icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Dm(client))