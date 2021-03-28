import discord
import asyncio
import re
import os

source_token = os.environ['SOURCE_DISCORD_BOT_TOKEN']
target_token = os.environ['TARGET_DISCORD_BOT_TOKEN']
source_channel_id = int(os.environ['SOURCE_CHANNEL_ID'])
target_channel_id = int(os.environ['TARGET_CHANNEL_ID'])

source_client = discord.Client()
target_client = discord.Client()


def find_url(string):
    url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", string) # noqa
    return url


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


@source_client.event
async def on_message(message):
    if message.channel.id == source_channel_id:
        author_name = message.author.name + "#" + message.author.discriminator
        if len(message.attachments) > 0:
            image_url = message.attachments[0].url
        else:
            image_url = ""
        await send_message(build_embed(author_name, message.author.avatar_url_as(format=None, static_format='png', size=1024), message.clean_content, message.author.color, image_url))


@target_client.event
async def send_message(message_embed):
    channel = target_client.get_channel(target_channel_id)
    await channel.send(embed=message_embed)


loop = asyncio.get_event_loop()
task1 = loop.create_task(source_client.start(source_token))
task2 = loop.create_task(target_client.start(target_token))
gathered = asyncio.gather(task1, task2, loop=loop)
loop.run_until_complete(gathered)
