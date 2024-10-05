import re
import os, random, time, sys
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB, Message
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import string

# Bot Token, API ID, and API Hash
BOT_TOKEN = "7205900462:AAE3drpVj8teYXRHMcrbnc4lLHnTn7GSbLg"
API_ID = 26487396
API_HASH = '778b12cba913e98ee54b5ee441b908c9'

# Updated Channel IDs and their links
Fsub1 = -1002481055755
Fsub_Link1 = "https://t.me/+OFTzixeLCmUyN2U1"

Fsub2 = -1002451309277
Fsub_Link2 = "https://t.me/+2ne7CdxMFR5kODA1"

Fsub3 = -1002293100873
Fsub_Link3 = "https://t.me/+4mHyvBsbhWtkNDE9"

Fsub4 = -1002402830740
Fsub_Link4 = "https://t.me/+Mj86IiX1O5AzYjE9"

# Initialize bot client
if BOT_TOKEN is not None:
    try:
        pbot = Client("Chizuru", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
        print("❤️ Bot Connected")
    except Exception as e:
        print('😞 Error While Connecting To Bot')    
        print(e)
        sys.exit()

# Buttons for joining channels and verifying
F_Button = IKM(
    [
        [
            IKB("Join Channel 1", url=Fsub_Link1),
            IKB("Join Channel 2", url=Fsub_Link2)
        ],
        [
            IKB("Join Channel 3", url=Fsub_Link3),
            IKB("Join Channel 4", url=Fsub_Link4)
        ],
        [
            IKB("Verify", "verify")
        ]
    ]
)

# Function to generate a random 15-character alphanumeric redeem code
def generate_redeem_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

# Callback query handler (for button interactions)
@pbot.on_callback_query()
async def answer(client: Client, callback_query):
    id = callback_query.from_user.id
    if "verify" in callback_query.data:
        try:
            # Check if user is in all channels
            await client.get_chat_member(chat_id=Fsub1, user_id=id)
            await client.get_chat_member(chat_id=Fsub2, user_id=id)
            await client.get_chat_member(chat_id=Fsub3, user_id=id)
            await client.get_chat_member(chat_id=Fsub4, user_id=id)
        except UserNotParticipant:
            return await client.send_message(
                chat_id=id,
                text="**FIRST JOIN ALL CHANNELS ❤️💸\nAND CLICK ON VERIFY TO PROCEED 💸**",
                reply_markup=F_Button
            )

        # Generate the redeem code
        redeem_code = generate_redeem_code()

        # Send the redeem code message
        await client.send_message(
            chat_id=id,
            text=f"**Thank you for joining all of our channels, here is a free redeem code 👇:**\n\n"
                 f"`{redeem_code}`\n\n"
                 f"**⚠️ If you leave any channel, this promo code will not work ⚠️**",
        )
# _______________MTB DEVS________________ #
# Start command handler
@pbot.on_message(filters.command('start') & filters.private)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        caption="**FIRST JOIN ALL CHANNELS ❤️💸\n\nAND CLICK ON VERIFY TO PROCEED 💸**",
        photo="https://envs.sh/whE.jpg",
        reply_markup=F_Button
    )

# Handler for when a user leaves a channel
@pbot.on_chat_member_updated()
async def send_msg(bot: Client, m: Message):
    try:
        if m.old_chat_member.status == "member" and m.new_chat_member.status == "left":
            await bot.send_message(
                chat_id=m.old_chat_member.user.id,
                text="YOUR REDEEM CODE HAS EXPIRED ✅\n\n"
                     "ITS IS BECAUSE I DETECTED YOU HAVE LEFT OUR CHANNEL ✨\n\n"
                     "🏆 CLICK /start TO GET NEW REDEEM CODE 🏆"
            )
    except Exception as e:
        print(f"Error: {e}")

# Run the bot
pbot.run()
print(“MTB Bot is Running”)
