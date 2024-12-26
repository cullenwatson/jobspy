import os
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from .jobs import JobPost
from .scrapers.utils import create_logger

load_dotenv()

logger = create_logger("TelegramBot")


class TelegramBot:

    def __init__(self):
        self._api_token = os.getenv("TELEGRAM_API_TOKEN")
        self.chatId = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = Bot(token=self._api_token)
        # Create the Application and pass it your bot's token.
        self.application = Application.builder().token(self._api_token).build()
        # Run the bot until the user presses Ctrl-C
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def sendJob(self, job: JobPost):
        """
        Send JobPost details to Telegram chat.
        """
        message = f"Job ID: {job.id}\n" \
            f"Job Title: {job.title}\n" \
            f"Company: {job.company_name}\n" \
            f"Location: {job.location.display_location()}\n" \
            f"Link: {job.job_url}\n"
        try:
            await self.bot.sendMessage(chat_id=self.chatId, text=message)
            logger.info(f"Sent job to Telegram: {job.id}")
        except Exception as e:
            logger.error(f"Failed to send job to Telegram: {job.id}")
            logger.error(f"Error: {e}")