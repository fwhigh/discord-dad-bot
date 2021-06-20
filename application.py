import os
import random

import discord
import giphy_client
from giphy_client.rest import ApiException
from dotenv import load_dotenv

HEY_DAD_GIMME_COMMAND_LIST = [
    'hey dad i want', 'hey daddy i want',
    'hey dad gimme', 'hey daddy gimme',
    'hey dad, gimme', 'hey daddy, gimme',
    'hey dad give me', 'hey daddy give me',
    'hey dad, give me', 'hey daddy, give me',
]


def is_hey_dad_gimme_command(s: str):
    for command in HEY_DAD_GIMME_COMMAND_LIST:
        if s.lower().startswith(command):
            return True
    return False


def get_hey_dad_gimme_query(s: str):
    result = str(s).lower()
    for command in HEY_DAD_GIMME_COMMAND_LIST:
        if result.startswith(command):
            return result.replace(command, '')
    return None


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
giphy_api_instance = giphy_client.DefaultApi()
giphy_api_key = os.getenv('GIPHY_API_KEY')
giphy_kwargs = dict(
    limit=25,  # int | The maximum number of records to return. (optional) (default to 25)
    offset=0,  # int | An optional results offset. Defaults to 0. (optional) (default to 0)
    rating='g',  # str | Filters results by specified rating. (optional)
    lang='en', # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
    fmt='json',  # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)
)


async def search_gifs(query, **kwargs):
    try:
        response = giphy_api_instance.gifs_search_get(
            giphy_api_key,
            query, **kwargs)
        lst = list(response.data)
        gif = random.choices(lst)

        index = 0  # TODO Randomize index
        return gif[index].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Heller High Discord server!'
    )


@client.event
async def on_message(message):
    # Don't let the bot call the bot
    if message.author == client.user:
        return

    anthony_bourdain_quotes = [
        "Your body is not a temple, it's an amusement park. Enjoy the ride.",
        "I always entertain the notion that I'm wrong, or that I'll have to revise my opinion. Most of the time that feels good; sometimes it really hurts and is embarrassing.",
        "Luck is not a business model.",
        "If I'm an advocate for anything, it's to move. As far as you can, as much as you can. Across the ocean, or simply across the river. Walk in someone else's shoes or at least eat their food. It's a plus for everybody.",
        "Travel is about the gorgeous feeling of teetering in the unknown.",
        "Skills can be taught. Character you either have or you don't have.",
        "I don't have to agree with you to like you or respect you.",
        "As you move through this life and this world, you change things slightly; you leave marks behind, however small. And in return, life--and travel--leaves marks on you. Most of the time, those marks--on your body or on your heart--are beautiful. Often, though, they hurt.",
        "I'm not afraid to look like an idiot.",
        "Without experimentation, a willingness to ask questions and try new things, we shall surely become static, repetitive, and moribund.",
        "Maybe that's enlightenment enough: to know that there is no final resting place of the mind, no moment of smug clarity. Perhaps wisdom ... is realizing how small I am, and unwise, and how far I have yet to go.",
        "You learn a lot about someone when you share a meal together.",
        "The journey is part of the experience -- an expression of the seriousness of one's intent. One doesn't take the A train to Mecca.",
        "I'm a big believer in winging it. I'm a big believer that you're never going to find a perfect city travel experience or the perfect meal without a constant willingness to experience a bad one. Letting the happy accident happen is what a lot of vacation itineraries miss, I think, and I'm always trying to push people to allow those things to happen rather than stick to some rigid itinerary.",
        "Cooking is a craft, I like to think, and a good cook is a craftsman -- not an artist. There's nothing wrong with that: The great cathedrals of Europe were built by craftsmen -- though not designed by them. Practicing your craft in expert fashion is noble, honorable, and satisfying.",
        "To me, life without veal stock, pork fat, sausage, organ meat, demi-glace, or even stinky cheese is a life not worth living.",
        "Don't lie about it. You made a mistake. Admit it and move on. Just don't do it again. Ever.",
        "Travel isn't always pretty. It isn't always comfortable. Sometimes it hurts, it even breaks your heart. But that's OK. The journey changes you; it should change you. It leaves marks on your memory, on your consciousness, on your heart, and on your body. You take something with you. Hopefully, you leave something good behind.",
        "The way you make an omelet reveals your character.",
        "Assume the worst. About everybody. But don't let this poisoned outlook affect your job performance. Let it all roll off your back. Ignore it. Be amused by what you see and suspect. Just because someone you work with is a miserable, treacherous, self-serving, capricious, and corrupt asshole shouldn't prevent you from enjoying their company, working with them, or finding them entertaining.",
        "I'm not going anywhere. I hope. It's been an adventure. We took some casualties over the years. Things got broken. Things got lost. But I wouldn't have missed it for the world.",
        "[When I die], I will decidedly not be regretting missed opportunities for a good time. My regrets will be more along the lines of a sad list of people hurt, people let down, assets wasted, and advantages squandered.",
        "Without new ideas, success can become stale.",
        "I wanted kicks -- the kind of melodramatic thrills and chills I'd yearned for since childhood, the kind of adventure I'd found as a little boy in the pages of my Tintin comic books.",
        "Cream rises. Excellence does have its rewards.",
        "What are our expectations? Which of the things we desire are within reach? If not now, when? And will there be some left for me?",
        "I'm very type-A, and many things in my life are about control and domination, but eating should be a submissive experience, where you let down your guard and enjoy the ride.",
        "I learned a long time ago that trying to micromanage the perfect vacation is always a disaster. That leads to terrible times.",
        "I can unload my opinion on anybody at any time.",
    ]

    if message.content == 'abq!':
        response = random.choice(anthony_bourdain_quotes)
        await message.channel.send(response)
    elif is_hey_dad_gimme_command(message.content):
        query = get_hey_dad_gimme_query(message.content)
        gif = await search_gifs(query)
        await message.channel.send(gif)


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)
