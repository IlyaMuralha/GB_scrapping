from telethon import TelegramClient
import time

api_id = 9196989
api_hash = '7ae6ac0a32ed20fcc4be20248c0a9a18'

client = TelegramClient('test_tg', api_id, api_hash)


async def main():
    # me = await client.get_me()
    dialogs = await client.get_dialogs()
    for dlg in dialogs:
        if dlg.title == '#ЯвДвижении':
            # # await dlg.send_message('Hello')
            # async for msg in client.iter_messages(dlg):
            #     if msg.media:
            #         await msg.download_media()
            #         print(msg.date, msg.text)
            #         time.sleep(1)
            members = await client.get_participants(dlg)
    for member in members:
     print(member.username)
    pass


with client:
    client.loop.run_until_complete(main())
