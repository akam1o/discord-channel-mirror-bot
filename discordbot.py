import discord
import asyncio
import re
import os

source_token = os.environ["SOURCE_DISCORD_BOT_TOKEN"]
target_token = os.environ["TARGET_DISCORD_BOT_TOKEN"]
source_channel_id = int(os.environ["SOURCE_CHANNEL_ID"])
target_channel_id = int(os.environ["TARGET_CHANNEL_ID"])

source_intents = discord.Intents.default()
source_intents.guilds = True
source_intents.messages = True
source_intents.message_content = True
source_client = discord.Client(intents=source_intents)

target_intents = discord.Intents.default()
target_intents.guilds = True
target_client = discord.Client(intents=target_intents)


def find_url(string):
    urls = re.findall(r"https?://\S+", string)
    return [u.rstrip(").,]") for u in urls]


def build_embed(author_name, author_picture, embed_desc, embed_color, embed_image):
    emb = discord.Embed()
    emb.set_author(name=author_name, url="", icon_url=author_picture)
    emb.description = embed_desc
    emb.color = embed_color
    message_urls = find_url(embed_desc)
    if embed_image != "":
        emb.set_image(url=embed_image)
        print(author_name + " uploaded an image")
    elif len(message_urls) > 0:
        emb.set_image(url=message_urls[0])
        print(author_name + " linked an image")
    else:
        print(author_name + ": " + embed_desc)
    return emb


async def send_message(message_embed):
    channel = target_client.get_channel(target_channel_id)
    if channel is None:
        channel = await target_client.fetch_channel(target_channel_id)
    await channel.send(embed=message_embed)


@source_client.event
async def on_message(message):
    if message.channel.id == source_channel_id:
        author_name = message.author.name + "#" + message.author.discriminator
        image_url = ""
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image/"):
                image_url = attachment.url
                break
        author_picture = message.author.display_avatar.replace(size=1024).url
        author_color = getattr(message.author, "color", discord.Color.default())
        await send_message(
            build_embed(
                author_name,
                author_picture,
                message.clean_content,
                author_color,
                image_url,
            )
        )


async def main():
    async with source_client, target_client:
        await asyncio.gather(
            source_client.start(source_token),
            target_client.start(target_token),
        )


asyncio.run(main())
