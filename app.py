import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot tokeningiz
BOT_TOKEN = "7879899171:AAH-XevwLQFIB6t2Z1otto7-W7TF6a9mbnU"
ADMIN_ID=7176798576
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=None)  
)
dp = Dispatcher(storage=MemoryStorage())

class PostStates(StatesGroup):
    waiting_channel = State()
    waiting_post = State()

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer("🔹 Avval kanal username ni yuboring:")
        await state.set_state(PostStates.waiting_channel)
    else:
        await message.answer("⛔ Siz admin emassiz!")
    

@dp.message(PostStates.waiting_channel)
async def get_channel(message: types.Message, state: FSMContext):
    await state.update_data(channel=message.text.strip())
    await message.answer("✅ Endi rasm, video yoki oddiy post yuboring:")
    await state.set_state(PostStates.waiting_post)

@dp.message(PostStates.waiting_post)
async def forward_with_inline(message: types.Message, state: FSMContext):
    data = await state.get_data()
    channel = data.get("channel")

    # Inline tugma (yangilangan)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Asilbek Hosting Bot", url="https://t.me/Hosting77_Bot")]
    ])

    try:
        if message.text:
            await bot.send_message(
                chat_id=channel,
                text=message.text,
                entities=message.entities,  # Formatni saqlash
                reply_markup=keyboard
            )

        elif message.photo:
            await bot.send_photo(
                chat_id=channel,
                photo=message.photo[-1].file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                reply_markup=keyboard
            )

        elif message.video:
            await bot.send_video(
                chat_id=channel,
                video=message.video.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                reply_markup=keyboard
            )

        else:
            await message.answer("❌ Bu turdagi kontent hozircha qo‘llab-quvvatlanmaydi.")

        await message.answer("✅ Post kanalga yuborildi!")
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
