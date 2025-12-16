import discord
import requests
import os
from discord.ext import tasks

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

class RegionView(discord.ui.View):
    def __init__(self, regions):
        super().__init__(timeout=None)
        self.regions = regions

    @discord.ui.button(label="🌍 Voir les régions", style=discord.ButtonStyle.primary)
    async def show_regions(self, interaction: discord.Interaction, button: discord.ui.Button):
        text = "\n".join([f"• {r}" for r in self.regions])
        await interaction.response.send_message(
            f"🌍 **Régions disponibles :**\n{text}",
            ephemeral=True
        )

@tasks.loop(hours=24)
async def post_events():
    url = "https://fortnite-api.com/v1/events/list"
    response = requests.get(url)
    data = response.json()

    channel = client.get_channel(CHANNEL_ID)

    for event in data["data"]["events"][:3]:
        name = event["name"]
        date = event["beginTime"].replace("T", " ").replace("Z", "")
        regions = list(event["regions"].keys())

        embed = discord.Embed(
            title=f"🏆 {name}",
            description=f"📅 {date}\nClique sur le bouton pour voir les régions",
            color=0x3498db
        )

        await channel.send(embed=embed, view=RegionView(regions))

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")
    post_events.start()

client.run(DISCORD_TOKEN)