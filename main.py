import discord
from discord.ext import commands
import os
import json
import random
import aiohttp
import getenv
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
from run_forever import run_forever

def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes.get(str(message.guild.id), "--")


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=get_prefix,
intents=intents, owner_ids={569105874912804874,793433316258480128})
client.load_extension('jishaku')
client.sniped_messages = {}
client.sniped_messages1 = {}
client.remove_command("help")

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.online, activity=discord.Game('Naruto | Ping to know more'))
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------------')


@client.event
async def on_message(message):
	
	if message.content == f'<@!{client.user.id}>':

			try:
			
				with open('prefixes.json','r') as f:
					prefixes = json.load(f)

				pre = prefixes[str(message.guild.id)]

			except:
				pre ='--'	

			embed=discord.Embed(colour=discord.Colour.blue())
			embed.set_author(name=f'My command prefix for this server is `{pre}`,type `{pre}help` for more info',icon_url=message.author.avatar_url)
			await message.channel.send(embed=embed)
	
	await client.process_commands(message)

@client.command()
@commands.has_permissions(administrator = True)
async def setprefix(ctx,prefix):


    with open('prefixes.json','r') as f:
      prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json','w') as f:
      json.dump(prefixes,f)

    await ctx.send(f'The prefix was changed to {prefix}')

# @client.command()
# @commands.has_permissions(administrator = True)
# async def resetprefix(ctx,prefix):
	
# 	with open('prefixes.json','r') as f:
# 		prefixes = json.load(f)

# 	prefixes[str(ctx.guild.id)] = '--'

# 	with open ('prefixes.json','w') as f:
# 		json.dump(prefixes,f)

# 	await ctx.send (f'The prefix was reset to {pre}')

mainshop = [{
    "name": "Watch",
    "price": 200,
    "description": ""
}, {
    "name": "Laptop",
    "price": 5000,
    "description": ""
}, {
    "name": "Phone",
    "price": 6900,
    "description": ""
}, {
    "name": "Fishing pole",
    "price": 4000,
    "description": ""
}, {
    "name": "Hunting Rifle",
    "price": 3499,
    "description": ""
}]

@client.event
async def on_message_delete(message):
  client.sniped_messages[message.guild.id] = {message.author.id:(message.content,message.author,message.channel.name,message.created_at)}
  client.sniped_messages1[message.guild.id] = (message.content,message.author,message.channel.name,message.created_at)

@client.command()
async def snipe(ctx,member:discord.Member=None):
  
	if member == None:
		try:
			contents, author, channel_name, time = client.sniped_messages1[ctx.guild.id]

			embed=discord.Embed(description = contents, colour=discord.Colour.blue(),timestamp=time)
			embed.set_author(name=f'{author.name}#{author.discriminator}',icon_url=author.avatar_url)
			embed.set_footer(text=f'Deleted in : #{channel_name}')
			await ctx.send(embed=embed)
			
			await ctx.send(f'{author.name} just got sniped :archery:')
		except KeyError:
			await ctx.send('Nothing to snipe dumb!')

	else:
		try:

			contents, author, channel_name, time = client.sniped_messages[ctx.guild.id][member.id]

			embed=discord.Embed(description = contents, colour=discord.Colour.blue(),timestamp=time)
			embed.set_author(name=f'{member.name}#{member.discriminator}',icon_url=member.avatar_url)
			embed.set_footer(text=f'Deleted in : #{channel_name}')
			await ctx.send(embed=embed)
			
			await ctx.send(f'{member.name} just got sniped :archery:')
		except KeyError:
				await ctx.send('Nothing to snipe dumb!')


@client.event #facepalms #oops
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		embed = discord.Embed(
				title='Cooldown!', description=f'woah! slow it down buddy, this command is in a cooldown you can try after {round(error.retry_after)} seconds', colour=discord.Colour.blue())
		await ctx.send(embed=embed)
	elif isinstance(error, commands.MissingPermissions):

		embed=discord.Embed(title='Missing Permissions',description='You are missing permissions to run this command buddy',colour=discord.Colour.blue())
		await ctx.send(embed=embed)
	elif isinstance(error, commands.MissingPermissions):

		embed=discord.Embed(title='Missing Permissions',description='You are missing permissions to run this command buddy',colour=discord.Colour.blue())
		await ctx.send(embed=embed)
		
	elif isinstance(error, commands.CommandNotFound):


			embed=discord.Embed(title='Unknown Command',description='Thats not a Valid Command :thinking:',colour=discord.Colour.blue())
			await ctx.send(embed=embed)


	else:
		raise error

# @client.event
# async def on_member_join(member):
#     guild = client.get_guild(731502989596164146) 
#     welcome_channel = guild.get_channel(731502989596164149) 
#     await welcome_channel.send(f'Welcome to the our Server, {member.mention} !  :partying_face:')
#     await member.send(f'We are glad to have you in our group, {member.name} !  :partying_face:')

@client.command(aliases=['ft','ascii'])
async def fancytext(ctx,*,word):
	# async def char(ctx,word):
	# 	a  = [i for i in word]
	# 	await ctx.send(len(a))
	# if	len(a) > 15:
	# 	await ctx.send('So Big will look messed up')
	# else:
		async with aiohttp.ClientSession() as session:
									
				async with session.get(
						f"https://artii.herokuapp.com/make?text={word}"
				) as response:
						fancy = await response.text()
						await ctx.send(f"```{fancy}```")
						await ctx.send('May Look Disoriented on Phone :disappointed_relieved:')

#ECONOMY CMD STARTS HERE///////////////////////////////////////////////////////////////////////////// 



@client.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f'{ctx.author.name} Balance',
                       color=discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance', value=bank_amt)
    await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 15, commands.BucketType.member)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(20, 101)

    await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", 'w') as f:
        json.dump(users, f)


@client.command(aliases=['with'])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, 'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')


@client.command(aliases=['dep'])
async def deposit(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, -1 * amount)
    await update_bank(ctx.author, amount, 'bank')
    await ctx.send(f'{ctx.author.mention} You deposited {amount} coins')


@client.command()
async def give(ctx, member: discord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, -1 * amount, 'bank')
    await update_bank(member, amount, 'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')

# @client.command(aliases=['scout'])
# async def

@client.command(aliases=['steal'])
@commands.cooldown(1, 20, commands.BucketType.member)
async def rob(ctx, member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)

    if bal[0] < 100:
        await ctx.send('he broke')
        return

    earning = random.randrange(0, bal[0])

    await update_bank(ctx.author, earning)
    await update_bank(member, -1 * earning)
    await ctx.send(
        f'{ctx.author.mention} You robbed {member.mention} and got {earning} coins'
    )


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def slots(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice([':green_circle:', ':blue_circle:', ':red_circle:',':orange_circle:',':purple_circle:',':brown_circle:'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author, 2 * amount)
        await ctx.send(f'You won :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author, -1 * amount)
        await ctx.send(f'You lose :( {ctx.author.mention}')


@client.command()
async def shop(ctx):
    em = discord.Embed(title="Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f"₹{price} | {desc}")

    await ctx.send(embed=em)


@client.command()
async def buy(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send(
                f"You don't have enough money in your wallet to buy {amount} {item}"
            )
            return

    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def inv(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        inventory = users[str(user.id)]["inventory"]
    except:
        inventory = []

    em = discord.Embed(title="Inventory")
    for item in inventory:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["inventory"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["inventory"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["inventory"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["inventory"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]


@client.command()
async def sell(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send(f"You don't have {amount} {item} in your inventory.")
            return
        if res[1] == 3:
            await ctx.send(f"You don't have {item} in your inventory.")
            return

    await ctx.send(f"You just sold {amount} {item}.")


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.7 * item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["inventory"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["inventory"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "wallet")

    return [True, "Worked"]



@client.command(aliases=["lb"])
async def leaderboard(ctx, x=1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(
        title=f"Top {x} Richest People",
        description=
        "This is decided on the basis of raw money in the bank and wallet",
        color=discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = commands.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json', 'w') as f:
        json.dump(users, f)

    return True


async def get_bank_data():
    with open('mainbank.json', 'r') as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode='wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json', 'w') as f:
        json.dump(users, f)
    bal = users[str(user.id)]['wallet'], users[str(user.id)]['bank']
    return bal

#ECONOMY CODE ENDS HERE
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////PHOTO CODE STARTS HERE

@client.command()
async def wanted(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	wanted = Image.open ("wanted.jpg")

	asset = user.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)

	pfp = pfp.resize((265,267))

	wanted.paste(pfp, (92,192))
	wanted.save("Wantedoutput.jpg")

	await ctx.send(file = discord.File("Wantedoutput.jpg"))

@client.command()
async def note(ctx, *,text = "No text entered"):

	note = Image.open ("note.png")

	draw = ImageDraw.Draw(note)
	font = ImageFont.truetype("Roboto.ttf", 25)

	draw.text((426,440), text, (0,0,0),font = font)

	note.save("noteoutput.png")

	await ctx.send(file = discord.File("noteoutput.png"))


@client.command(pass_context=True)
async def giphy(ctx, *, search):
    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get(f'https://api.giphy.com/v1/gifs/random?api_key={getenv("")}')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + f'&api_key={getenv("gify")}')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    await session.close()

    await ctx.send(embed=embed)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

run_forever()
client.run(os.getenv('TOKEN'))