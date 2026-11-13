import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp
from .config import BOT_TOKEN, WEBAPP_URL, ADMIN_IDS
from .database import get_or_create_user, get_user_attempts, list_tests
from .material_finder import generate_mock_test_ai, save_generated_test_to_db

logger = logging.getLogger(__name__)

dp = Dispatcher()

def is_https_url(url: str) -> bool:
    return url.lower().startswith("https://")

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Returns the main interactive keyboard with Telegram Mini App button"""
    buttons = []
    
    if is_https_url(WEBAPP_URL):
        buttons.append([
            InlineKeyboardButton(
                text="🚀 IELTS Mock Testni Boshlash",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                text="🚀 IELTS Mock (Brauzerda: localhost:8080)",
                callback_data="tma_info"
            )
        ])

    buttons.extend([
        [
            InlineKeyboardButton(text="📊 Natijalarim", callback_data="my_stats"),
            InlineKeyboardButton(text="📚 Testlar Ro'yxati", callback_data="test_list")
        ],
        [
            InlineKeyboardButton(text="⚡ AI Yangi Mock Yaratish", callback_data="ai_generate_mock")
        ]
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def command_start(message: types.Message):
    user = message.from_user
    get_or_create_user(
        tg_id=user.id,
        username=user.username or "",
        full_name=user.full_name or "Candidate"
    )

    welcome_text = (
        f"👋 <b>Assalomu alaykum, {user.first_name}!</b>\n\n"
        "🎯 <b>IELTS Computer-Delivered Mock Platformasiga xush kelibsiz!</b>\n\n"
        "Bu bot orqali siz:\n"
        "• 🎧 <b>Listening</b> (haqiqiy britaniya/avstraliya audio bilan)\n"
        "• 📖 <b>Reading</b> (IDP/British Council kabi split-screen, highlighter va taymer bilan)\n"
        "• ✍️ <b>Writing</b> (so'z sanagich va AI tekshiruv bilan)\n"
        "• 🗣 <b>Speaking</b> (savol-javob simulyatori)\n"
        "• 🤖 <b>AI Material Finder</b> (1 tugma bilan yangi mock yaratish va topish)\n\n"
        "<i>Pastdagi tugmalar orqali platformaga kiring:</i>"
    )

    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@dp.message(Command("mock"))
async def command_mock(message: types.Message):
    if is_https_url(WEBAPP_URL):
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🎯 Mock Platformani Ochish", web_app=WebAppInfo(url=WEBAPP_URL))]
            ]
        )
    else:
        kb = get_main_keyboard()
        
    await message.answer(
        "📝 <b>IELTS Mock Test boshlash uchun quyidagi tugmani bosing:</b>",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "tma_info")
async def cb_tma_info(call: types.CallbackQuery):
    await call.answer()
    msg = (
        "ℹ️ <b>Mini App hozirda mahalliy kompyuteringizda ishlamoqda:</b>\n\n"
        "🌐 Brauzerda ochish uchun: <code>http://localhost:8080</code>\n\n"
        "📲 Telegram ichida ochilishi uchun esa <b>HTTPS</b> havola kerak.\n"
        "Buning uchun loyiha papkasidagi <b><code>tunnel.bat</code></b> ni ishga tushiring va chiqqan <code>https://...</code> havolani <b>.env</b> fayliga yozing!"
    )
    await call.message.answer(msg, parse_mode="HTML")

@dp.message(Command("stats"))
async def command_stats(message: types.Message):
    history = get_user_attempts(message.from_user.id)
    if not history:
        await message.answer(
            "📊 Siz hali hech qanday test topshirmagansiz.\n"
            "Sinab ko'rish uchun <b>'IELTS Mock Testni Boshlash'</b> tugmasini bosing!",
            reply_markup=get_main_keyboard(),
            parse_mode="HTML"
        )
        return

    text = "📈 <b>Oxirgi topshirgan testlaringiz:</b>\n\n"
    for idx, item in enumerate(history[:5], 1):
        text += (
            f"<b>{idx}. {item.get('test_title', 'IELTS Test')}</b>\n"
            f"   • Ball: {item['score']} / {item['max_score']}\n"
            f"   • 🏅 <b>IELTS Band: {item['band_score']}</b>\n"
            f"   • Vaqti: {item['created_at'][:16]}\n\n"
        )
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@dp.callback_query(F.data == "my_stats")
async def cb_stats(call: types.CallbackQuery):
    await call.answer()
    history = get_user_attempts(call.from_user.id)
    if not history:
        await call.message.answer("Siz hali test topshirmagansiz. Mini App orqali test topshiring!")
        return

    text = "📈 <b>Oxirgi IELTS Mock natijalaringiz:</b>\n\n"
    for idx, item in enumerate(history[:5], 1):
        text += (
            f"<b>{idx}. {item.get('test_title', 'IELTS Test')}</b>\n"
            f"   • Ball: {item['score']}/{item['max_score']} (<b>Band {item['band_score']}</b>)\n"
        )
    await call.message.answer(text, parse_mode="HTML")

@dp.callback_query(F.data == "test_list")
async def cb_test_list(call: types.CallbackQuery):
    await call.answer()
    tests = list_tests()
    text = "📚 <b>Mavjud IELTS Mock Testlar:</b>\n\n"
    for t in tests[:8]:
        text += f"• <b>{t['title']}</b> ({t['type'].upper()} - {t.get('question_count', 0)} savol)\n"
    text += "\n<i>Testni yechish uchun pastdagi Mini App tugmasini bosing!</i>"
    await call.message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@dp.callback_query(F.data == "ai_generate_mock")
async def cb_ai_generate(call: types.CallbackQuery):
    await call.answer("AI yangi mock yaratmoqda...")
    msg = await call.message.answer("⏳ <b>AI IELTS bo'yicha yangi akademik material qidirmoqda va test tayyorlamoqda...</b>", parse_mode="HTML")
    try:
        test_data = await generate_mock_test_ai()
        test_id = save_generated_test_to_db(test_data)
        await msg.edit_text(
            f"✅ <b>Yangi test tayyorlandi!</b>\n\n"
            f"📖 <b>Mavzu:</b> {test_data.get('title')}\n"
            f"📊 <b>Savollar soni:</b> {len(test_data.get('questions', []))} ta\n"
            f"⏱ <b>Vaqt:</b> {test_data.get('time_limit_minutes', 20)} daqiqa\n\n"
            f"<i>Testni Mini App orqali yechishingiz mumkin!</i>",
            reply_markup=get_main_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error("Error in bot AI mock generator: %s", e)
        await msg.edit_text("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")

async def start_bot(bot_instance: Bot):
    """Starts polling if token is valid"""
    try:
        if is_https_url(WEBAPP_URL):
            await bot_instance.set_chat_menu_button(
                menu_button=MenuButtonWebApp(
                    text="IELTS Mock",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            )
        logger.info("Bot started successfully. Polling...")
        await dp.start_polling(bot_instance)
    except Exception as e:
        logger.error("Failed to start bot: %s", e)
