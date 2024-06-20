import os
import discord
from google.cloud import secretmanager
from itertools import cycle

# Initialize Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure this is enabled if needed
client = discord.Client(intents=intents)

# Function to retrieve token from Secret Manager
def get_discord_token():
    # Initialize Secret Manager client
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "projects/963968816496/secrets/DISCORD_TOKEN"
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("UTF-8")

# Cycle for bot status
status_cycle = cycle([
    discord.Activity(type=discord.ActivityType.watching, name="your happiness!"),
    discord.Activity(type=discord.ActivityType.watching, name="you cheer up!")
])

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    change_status.start()  # Start changing statuses after the bot is ready

@tasks.loop(seconds=10)
async def change_status():
    # Get the next activity from the cycle
    next_status = next(status_cycle)
    # Update the bot's presence
    await client.change_presence(activity=next_status)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("$inspire"):
        # Implement your inspire command here
        pass

    if msg.startswith("$list"):
        await message.channel.send('Here are the sad words: sad, depressed, unhappy, angry, miserable, mad, unhappy.')

    if msg.startswith("$responding"):
        # Implement your responding command here
        pass

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$help'):
        await message.channel.send('My commands are: $inspire ...')  # Update with your help message

# Start the bot
discord_token = get_discord_token()
client.run(discord_token)
