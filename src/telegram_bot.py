import os
from typing import Union

from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ReactionEmoji

from jobspy.jobs import JobPost
from jobspy.scrapers.utils import create_logger

load_dotenv()

logger = create_logger("TelegramBot")


class TelegramBot:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TelegramBot, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._api_token = os.getenv("TELEGRAM_API_TOKEN")
        self.bot = Bot(token=self._api_token)

    def get_reply_markup(self):
        keyboard = [
            [
                InlineKeyboardButton(ReactionEmoji.FIRE,
                                     callback_data=ReactionEmoji.FIRE.name),
                InlineKeyboardButton(
                    ReactionEmoji.PILE_OF_POO, callback_data=ReactionEmoji.PILE_OF_POO.name)
            ],
        ]

        return InlineKeyboardMarkup(keyboard)

    async def send_job(self, chat_id: Union[int, str], job: JobPost):
        """
        Send JobPost details to Telegram chat.
        """
        message = f"Job ID: {job.id}\n" \
                  f"Job Title: {job.title}\n" \
                  f"Company: {job.company_name}\n" \
                  f"Location: {job.location.display_location()}\n" \
                  f"Link: {job.job_url}\n"
        reply_markup = self.get_reply_markup()

        try:
            await self.bot.sendMessage(chat_id=chat_id, text=message, reply_markup=reply_markup)
            logger.info(f"Sent job to Telegram: {job.id}")
        except Exception as e:
            logger.error(f"Failed to send job to Telegram: {job.id}")
            logger.error(f"Error: {e}")

    async def send_text(self, chat_id: Union[int, str], message: str, reply_markup: InlineKeyboardMarkup = None):
        """
        Send Text han Message to Telegram chat.
        """
        try:

            await self.bot.sendMessage(chat_id=chat_id, text=message, reply_markup=reply_markup)
            logger.info("Sent text message to Telegram")
        except Exception as e:
            logger.error("Failed to send text message to Telegram")
            logger.error(f"Error: {e}")

    async def send_test_message(self):
        """
        Send Test Message to Telegram chat.
        """
        message = "Test Test Testing"
        try:
            reply_markup = self.get_reply_markup()
            await self.bot.sendMessage(chat_id=self.chatId, text=message, reply_markup=reply_markup)
            logger.info("Sent test message to Telegram")
        except Exception as e:
            logger.error("Failed to send test message to Telegram")
            logger.error(f"Error: {e}")

    async def set_message_reaction(self, chat_id: Union[int, str], message_id: int, emoji_reaction: ReactionEmoji):
        """
        Send Test Message to Telegram chat.
        """
        try:
            await self.bot.set_message_reaction(chat_id=chat_id, message_id=message_id,
                                                reaction=emoji_reaction)
            logger.info(f"Reaction set to message: {message_id}")
        except Exception as e:
            logger.error(f"Failed to set Reaction to message: {message_id}")
            logger.error(f"Error: {e}")
