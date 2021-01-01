from telethon import events
from dsc import dsc

@dsc.on(events.NewMessage(pattern="^.ping", outgoing=True))
async def _(hehe):
    await hehe.edit("Pong")
