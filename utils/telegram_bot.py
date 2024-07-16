import telegram
import asyncio

TOKEN = "7261947544:AAFTGs0bnyuBEBIWydw9oL5RCZP65YGHpg0"  # YOUR BOT TOKEN
CHAT_ID = '1587088624'

bot = telegram.Bot(token=TOKEN)


async def send_message(text):
    async with bot:
        await bot.send_message(text=text, chat_id=CHAT_ID)


async def send_document(document):
    async with bot:
        await bot.send_document(document=document, chat_id=CHAT_ID)


async def send_photo(photo):
    async with bot:
        await bot.send_photo(photo=photo, chat_id=CHAT_ID)


async def send_video(video):
    async with bot:
        await bot.send_video(video=video, chat_id=CHAT_ID)


async def main():
    # Sending a message
    await send_message(text='Hi World!, How are you?')

    # # Sending a document
    # await send_document(document=open('/path/to/document.pdf', 'rb'), chat_id=chat_id)
    #
    # # Sending a photo
    # await send_photo(photo=open('/path/to/photo.jpg', 'rb'), chat_id=chat_id)
    #
    # # Sending a video
    # await send_video(video=open('path/to/video.mp4', 'rb'), chat_id=chat_id)


if __name__ == '__main__':
    asyncio.run(main())
