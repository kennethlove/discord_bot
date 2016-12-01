from urllib.parse import urlencode

from discord.ext.commands import Bot
import pyrebase

import secrets


treehouse_bot = Bot(command_prefix="!")
firebase = pyrebase.initialize_app(secrets.FIREBASE_CONFIG)
db = firebase.database()


@treehouse_bot.event
async def on_read():
    print("Client logged in")


@treehouse_bot.command()
async def hello(*args):
    return await treehouse_bot.say("Hello world!")


@treehouse_bot.command(aliases=['py_help', 'pyh'])
async def python_help(*args):
    url = ("https://docs.python.org/3/search.html?{}"
           "&check_keywords=yes&area=default".format(
               urlencode({'q': ' '.join(args)})
           ))
    return await treehouse_bot.say(url)


@treehouse_bot.command(aliases=['locations'])
async def show_location_names():
    all_locations = db.child("minecraft").child("locations").shallow().get()
    response = "I know about:\n{}".format("\n".join(all_locations.val()))
    return await treehouse_bot.say(response)


@treehouse_bot.command()
async def add_location(x, y, z, *, name):
    db.child("minecraft").child("locations").update(
        {name: "{} {} {}".format(x, y, z)}
    )
    return await treehouse_bot.say("I've added {}".format(name))


@treehouse_bot.command()
async def show_location(name):
    location = db.child("minecraft").child("locations").child(name).get()
    x, y, z = location.val().split()
    response = "{} is at X {}, Y {}, Z {}".format(name, x, y, z)
    return await treehouse_bot.say(response)


@treehouse_bot.command()
async def delete_location(name):
    db.child("minecraft").child("locations").child(name).remove()
    return await treehouse_bot.say("Done!")

treehouse_bot.run(secrets.BOT_TOKEN)
