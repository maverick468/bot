from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import asyncio

# 🔐 TOKEN
TOKEN = "8232179882:AAHo2FpUCRqoLPxRzA8AXVeuGwaFsMlpanE"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "project")
SPECIAL_DIR = os.path.join(BASE_DIR, "special")
RESEARCH_DIR = os.path.join(BASE_DIR, "research")

# 📋 MAIN NAME LIST (1.png, 2.png...)
names = [
    "Nathan Amarebeh","Noel Zelalem","Ezana Samson","Sofonyas Merid",
    "Brook Abenet","Salem Dilnesahu","Eyuel Zelalem","Tsion Simon",
    "Abigail Getu","Elizabeth Tigist","Edlawit Tewodros","Milkana Dereje",
    "Surafel Debebe","Saron Teklebrhan","Ruth Fekad","Eleni Temesgen",
    "Mariamawit Major","Amen Seifegebriel","Tsilat Temesgen","Amen F/slasie",
    "Yonatha Zewge","Bethel Fekade","Gelila Gezahegn","Maraki Theworos",
    "Soliyana Abraham","Mikyas Yosef","Emanda Addisu","Dawit Abraham",
    "Nolawit Elyas","Orkiya Million","Hanin Waeil","Hasset Mekurya",
    "Bitanya Ephrem","Ephrata Daniel","Amanuel Abebaw","Saron Awoke",
    "Arsema Gezahegn"
]

# ⭐ SPECIAL CERTIFICATE USERS
special_third = [
    "Ezana Samson",
    "Salem Dilnesahu",
    "Emanda Addisu",
    "Maraki Theworos",
    "Brook Abenet",
    "Arsema Gezahegn",
    "Noel Zelalem",
    "Sofonyas Merid"
]

special_map = {
    "Ezana Samson": "1.png",
    "Salem Dilnesahu": "2.png",
    "Emanda Addisu": "3.png",
    "Maraki Theworos": "4.png",
    "Brook Abenet": "5.png",
    "Arsema Gezahegn": "6.png",
    "Noel Zelalem": "7.png",
    "Sofonyas Merid": "8.png"
}

# 🧠 RESEARCH CERTIFICATE LIST
research_names = [
    "Elizabeth Tigist",
    "Noel Zelalem",
    "Sofonyas Merid",
    "Amen S/Gebriel",
    "Nathan Amarebeh",
    "Saron Awoke",
    "Eleni Temesgen",
    "Tsilat Temesgen",
    "Salem Dilnesahu",
    "Surafel Debebe",
    "Solyana Abraham",
    "Emanda Addisu",
    "Mikyas Yosef"
]

# 🧠 SAFE EDIT
async def safe_edit(msg, text):
    try:
        if msg and msg.text != text:
            await msg.edit_text(text)
    except:
        pass

# 🎯 KEYBOARDS
def main_menu():
    return ReplyKeyboardMarkup(
        [["🎓 Get Certificate"], ["ℹ️ Help"]],
        resize_keyboard=True
    )

def build_keyboard():
    keyboard = []
    row = []

    for name in names:
        row.append(name)
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append(["⬅️ Back"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AVC Certificate System\n\nChoose an option:",
        reply_markup=main_menu()
    )

# 📋 MENU
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Select your name:",
        reply_markup=build_keyboard()
    )

# ℹ️ HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "1. Click Get Certificate\n2. Select your name\n3. Receive certificates",
        reply_markup=main_menu()
    )

# ⏳ LOADING
async def loading_effect(update):
    msg = await update.message.reply_text("⏳ Preparing...")

    steps = [
        "🧾 Searching database...",
        "📄 Verifying record...",
        "📦 Generating certificates...",
        "📤 Sending files..."
    ]

    for step in steps:
        await asyncio.sleep(0.6)
        await safe_edit(msg, step)

    return msg

# 📤 MAIN LOGIC
async def send_certificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "🎓 Get Certificate":
        await show_menu(update, context)
        return

    if text == "ℹ️ Help":
        await help_command(update, context)
        return

    if text == "⬅️ Back":
        await start(update, context)
        return

    if text not in names:
        await update.message.reply_text("❌ Please use buttons only.")
        return

    index = names.index(text) + 1

    main_cert = os.path.join(BASE_DIR, f"{index}.png")
    project_cert = os.path.join(PROJECT_DIR, f"{index}.png")

    loading_msg = await loading_effect(update)

    await asyncio.sleep(1)
    await safe_edit(loading_msg, "📤 Sending certificates...")

    # 🏆 MAIN
    if os.path.exists(main_cert):
        with open(main_cert, "rb") as f:
            await update.message.reply_document(f, filename=f"{text}_main.png")

    # 📘 PROJECT
    if os.path.exists(project_cert):
        with open(project_cert, "rb") as f:
            await update.message.reply_document(f, filename=f"{text}_project.png")

    # ⭐ SPECIAL
    if text in special_third:
        file_name = special_map.get(text)
        special_cert = os.path.join(SPECIAL_DIR, file_name)

        if os.path.exists(special_cert):
            with open(special_cert, "rb") as f:
                await update.message.reply_document(f, filename=f"{text}_special.png")

    # 🧠 RESEARCH (NEW SYSTEM)
    if text in research_names:
        research_index = research_names.index(text) + 1
        research_cert = os.path.join(RESEARCH_DIR, f"{research_index}.png")

        if os.path.exists(research_cert):
            with open(research_cert, "rb") as f:
                await update.message.reply_document(f, filename=f"{text}_research.png")

    await loading_msg.delete()

    await update.message.reply_text(
        f"🎉 Thank you {text} for participating in AVC 🙌.If you have any questions contact @ezanasamson",
        reply_markup=main_menu()
    )

# ⚡ RUN BOT (STABLE)
app = ApplicationBuilder().token(TOKEN)\
    .connect_timeout(60)\
    .read_timeout(60)\
    .build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_certificate))

print("✅ AVC Certificate Bot Running...")
app.run_polling()