import discord
from discord.ext import commands
from discord import app_commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

custom_commands = {}

eight_ball_responses = [
    "It is certain.",
    "Without a doubt.",
    "Yes – definitely.",
    "You may rely on it.",
    "Ask again later.",
    "Cannot predict now.",
    "Don’t count on it.",
    "My sources say no.",
    "Very doubtful."
]

joke_list = [
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my computer I needed a break, and it said 'No problem – I’ll go to sleep.'",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I asked the dog what's two minus two. He said nothing."
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands.')
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.command(name='roll')
async def roll(ctx, sides: int = 6):
    result = random.randint(1, sides)
    await ctx.send(f'🎲 You rolled a {result}!')

@bot.command(name='addcmd')
async def add_custom_command(ctx, trigger: str, *, response: str):
    custom_commands[trigger.lower()] = response
    await ctx.send(f'✅ Custom command `!{trigger}` added.')

@bot.command(name='delcmd')
async def delete_custom_command(ctx, trigger: str):
    if trigger.lower() in custom_commands:
        del custom_commands[trigger.lower()]
        await ctx.send(f'❌ Command `!{trigger}` deleted.')
    else:
        await ctx.send("Command not found.")

@bot.command(name='8ball')
async def eight_ball(ctx, *, question: str):
    response = random.choice(eight_ball_responses)
    await ctx.send(f'🎱 {response}')

@bot.command(name='joke')
async def joke(ctx):
    response = random.choice(joke_list)
    await ctx.send(f'😂 {response}')

@bot.command(name='skisz')
async def skisz_cmd(ctx):
    await ctx.send("SkiSZ is the coolest guy ever!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!"):
        cmd = message.content[1:].split()[0].lower()
        if cmd in custom_commands:
            await message.channel.send(custom_commands[cmd])
        else:
            await bot.process_commands(message)

@bot.tree.command(name="roll", description="Roll a dice")
@app_commands.describe(sides="Number of sides on the dice")
async def slash_roll(interaction: discord.Interaction, sides: int = 6):
    result = random.randint(1, sides)
    await interaction.response.send_message(f'🎲 You rolled a {result}!')

@bot.tree.command(name="8ball", description="Ask the magic 8-ball a question")
@app_commands.describe(question="Your question")
async def slash_8ball(interaction: discord.Interaction, question: str):
    response = random.choice(eight_ball_responses)
    await interaction.response.send_message(f'🎱 {response}')

@bot.tree.command(name="joke", description="Get a random joke")
async def slash_joke(interaction: discord.Interaction):
    response = random.choice(joke_list)
    await interaction.response.send_message(f'😂 {response}')

@bot.tree.command(name="skisz", description="Celebrate the legend SkiSZ")
async def slash_skisz(interaction: discord.Interaction):
    await interaction.response.send_message("SkiSZ is the coolest guy ever!")

bot.run(os.getenv("YOUR_DISCORD_BOT_TOKEN"))
