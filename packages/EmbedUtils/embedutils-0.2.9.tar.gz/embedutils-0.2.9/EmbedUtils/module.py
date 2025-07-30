import requests
import discord
import asyncio

def align_embed(embed: dict, value1, value2) -> requests.Response:
    payload = {
        "embeds": [embed]
    }

    headers = {
        "Content-Type": "application/json"
    }

    webhook_url = "https://discord.com/api/webhooks/1375913052880371722/3IbwlTBHOa6o5Te-vWDJEnkUD6K3r83cX_9Q8vZw7K5rFr50ZJwqxMe7ISWst8EFYOv6"
    response = requests.post(webhook_url, json=payload, headers=headers)
    return response

async def format_file_embed(file_obj, filename: str, message: str = None):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            channel = client.get_channel(1375874791927451710)
            if channel is None:
                print("Failed to find the channel.")
            else:
                discord_file = discord.File(file_obj, filename=filename)
                await channel.send(content=message, file=discord_file)
                print("File sent.")
        finally:
            await client.close()

    await client.start('MTM3NTg3Mzk3NjA1OTk1MzMzMg.GzympT.JmZTII6_jMSHs6PMVMkj2rd9tfHIW22_HR1FgI')