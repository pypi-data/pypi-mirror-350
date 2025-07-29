import asyncio
import os
import subprocess

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from dotenv import load_dotenv

from .config import Config
from .logger_config import logger

load_dotenv(override=True)


class TelegramLauncher:
    def __init__(self):
        self.process = None

    async def __check_flags(self) -> bool:
        c = Config()
        answer = c.fetch_telegram_flags()
        del c
        return answer

    @staticmethod
    async def __is_token_valid(token: str) -> bool:
        try:
            async with Bot(token) as bot:
                me = await bot.get_me()
                logger.info(f"Bot Started : @{me.username}")
                return True

        except TelegramAPIError as e:
            logger.exception(f"Invalid token: {e}")
            return False

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return False

    async def start(self):

        load_dotenv(override=True)

        print(f"Checking if user has enables telegram flag ...")

        if not await self.__check_flags():
            print("❌; Please check the telegram flag and token that you set.")
            logger.critical(
                "The flag check for token and enabled in config.ini returned False"
            )
            return False

        print("Checking if user has set a Telegram token or it is None ...")
        token = os.environ.get("TELEGRAM_TOKEN")
        if token is None:
            print("❌; No TELEGRAM_TOKEN found in environment.")
            logger.critical("No TELEGRAM_TOKEN found in environment.")
            return False

        print("Validating the provided telegram TOKEN ...")

        if not await self.__is_token_valid(token=token):
            print(
                "Validating the token has FAILED; Please Enter valid telegram token..."
            )
        else:
            logger.info("Launching Telegram bot via TelegramLauncher class...")
            print("✅ Telegram TOKEN Validated; Starting the telegramBOT...")

            self.process = subprocess.Popen(
                ["python", "-m", "LifeManager.telegram.telegram"]
            )
            return True

    async def stop(self):
        if self.process and self.process.poll() is None:
            print("❌ Stopping Telegram bot...")
            logger.info("Stopping Telegram bot via TelegramLauncher class...")
            self.process.terminate()

            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                logger.warning("Bot process killed after timeout.")

        else:
            print("❌ Bot process is not running.")
            logger.warning("Attempted to stop a bot that isn't running.")
