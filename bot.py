from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from llm_response import send_message, new_program_prompt
from datetime import datetime

# دیکشنری برای ذخیره داده‌های کاربر
user_data = {}

keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ایجاد برنامه کاری جدید", callback_data="new_program")],
        [InlineKeyboardButton("برنامه روز بعد", callback_data="next_day")],
        [InlineKeyboardButton("ارسال گزارش روزانه", callback_data="send_report")],
        [InlineKeyboardButton("برنامه ماه آینده", callback_data="next_month")],
    ])

# پیام شروع
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    user_data[user_id]= {}
    user_data[user_id]["chats"] = []

    await update.message.reply_text("به ربات برنامه‌ریزی روزانه خوش آمدید! یکی از گزینه‌ها را انتخاب کنید:", reply_markup=keyboard)

# مدیریت کلیک‌ها
async def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "new_program":
        await query.message.reply_text("چند ساعت در روز می‌خواهید بخوابید؟")
        user_data[query.from_user.id]["state"] = "sleep"
    elif query.data == "next_day":
        await query.message.reply_text("در حال پردازش!")
        text = send_message(user_data[query.from_user.id]["chats"], message=f"next_day: {datetime.now().strftime('%A')}")
        user_data[query.from_user.id]["chats"].append({
            "role": "assistant", "content": text
        })
        await query.message.reply_markdown(text, reply_markup=keyboard)
    elif query.data == "send_report":
        await query.message.reply_text("لطفاً گزارش روزانه خود را بنویسید:")
        user_data[query.from_user.id]["state"] = "send_report"
    elif query.data == "next_month":
        await query.message.reply_text("چند ساعت در روز می‌خواهید بخوابید؟")
        user_data[query.from_user.id]["state"] = "sleep"

# مدیریت پیام‌های متنی
async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in user_data and "state" in user_data[user_id]:
        state = user_data[user_id]["state"]

        if state == "sleep":
            user_data[user_id]["sleep"] = update.message.text
            user_data[user_id]["state"] = "work_hours"
            await update.message.reply_text("چند ساعت در روز می‌خواهید کار کنید؟")
        elif state == "work_hours":
            user_data[user_id]["work_hours"] = update.message.text
            user_data[user_id]["state"] = "monthly_goals"
            await update.message.reply_text("اهداف ماهانه خود را بنویسید و با استفاده زا | آنها را جدا کنید:")
        elif state == "monthly_goals":
            user_data[user_id]["monthly_goals"] = update.message.text
            user_data[user_id]["state"] = None
            await update.message.reply_text("در حال ایجاد برنامه جدید ...")
            
            text = send_message(user_data[user_id]["chats"], message=new_program_prompt(
                targets= user_data[user_id]['monthly_goals'].split("|"),
                work=user_data[user_id]['work_hours'],
                sleep=user_data[user_id]['sleep']
            ))
            user_data[user_id]["chats"].append({
                "role": "assistant", "content": text
            })
            await update.message.reply_markdown(text, reply_markup=keyboard)

            
        elif state == "send_report":
            report = update.message.text
            user_data[user_id]["report"] = report
            user_data[user_id]["state"] = None
            await update.message.reply_text("گزارش شما ثبت شد. سپاسگزاریم!")

# اجرای ربات
def main():
    application = Application.builder().token("7356639046:AAFHkI-7LqZsBIDw3ikRlrrCi5yI0XhV8x8").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
