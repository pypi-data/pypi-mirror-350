"""
Configuration management for the LifeManager package.

This module provides the `Config` class which handles reading from and writing to
a `config.ini` file and updating the Telegram bot settings. It also supports safely
updating the Telegram API token in a `.env` file without altering other values.

Classes:
    Config: Handles the application's configuration logic for Telegram integration.
"""

import configparser
import os
from pathlib import Path

from .logger_config import logger


class Config:
    """
    Manages configuration settings for the LifeManager application.

    This includes reading and writing from a `config.ini` file,
    updating environment variables stored in a `.env` file,
    and managing Telegram and PostgreSQL-related settings.
    """

    def __init__(self, config_file="config.ini"):
        """
        Initializes the configuration handler.

        Args:
            config_file (str): Path to the configuration file. Defaults to 'config.ini'.
        """
        self.config = configparser.ConfigParser()
        self.config_file = config_file

        self._load_config()

    def _load_config(self):
        """Loads the configuration from the config file or creates it with defaults if it doesn't exist."""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            logger.info(f"Loaded configuration from '{self.config_file}'.")
        else:
            logger.warning(
                f"Config file '{self.config_file}' not found. Creating with default values."
            )

            # Set default values
            self.config["telegram"] = {"enabled": "false", "token": "false"}
            self.config["backup"] = {"path": "backup"}
            self.config["postgresql"] = {
                "user": "",
                "host": "",
                "port": "",
            }

            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)

            logger.info(f"Created default configuration at '{self.config_file}'.")
            print(f"Created default configuration at '{self.config_file}'.")

    def change_telegram_bot_status(self) -> bool:
        """
        Toggles the enabled status of the Telegram bot in the configuration file.

        Returns:
            bool: True if the bot is now enabled, False otherwise.
        """
        current_status = self.config.getboolean("telegram", "enabled", fallback=False)
        new_status = not current_status

        self.config.set("telegram", "enabled", str(new_status).lower())
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

        return new_status

    def change_telegram_TOKEN(self, token: str) -> bool:
        """
        Updates the TELEGRAM_TOKEN in the .env file.

        Args:
            token (str): The new Telegram bot token.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            self.__set_env_variable(f"TELEGRAM_TOKEN={token}")
            self.config.set("telegram", "token", "true")
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)
            logger.info(
                f"User Set `{token}` as his .env TELEGRAM_TOKEN= variable using Config.change_telegram_TOKEN"
            )
            return True
        except:
            logger.exception(f"An error in config.Change_telegram_TOKEN ")
            return False

    def change_PostgreSQL_user(self, user_name):
        """
        Updates the PostgreSQL username in the .env and config file.

        Args:
            user_name (str): New PostgreSQL username.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.__set_env_variable(full_text=f"PGUSER={user_name}")
            self.config.set("postgresql", "user", f"{user_name}")
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)

            logger.info(
                f"User set `{user_name}` as his .env `PGUSER` environment variable in Config.change_PostgreSQL_user "
            )
            return True
        except:
            logger.exception(f"An error in config.change_PostgreSQL_user ")
            return False

    def change_PostgreSQL_password(self, password):
        """
        Updates the PostgreSQL password in the .env file.

        Args:
            password (str): New password.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.__set_env_variable(f"PGPASSWORD={password}"):
            logger.info("User Has set a new password for the database")
            return True

        logger.critical(
            "User wanted to set a new password for the database but it failed."
        )
        return False

    def change_PostgreSQL_host(self, host):
        """
        Updates the PostgreSQL host in the .env and config file.

        Args:
            host (str): New PostgreSQL host.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.__set_env_variable(full_text=f"PGHOST={host}")
            self.config.set("postgresql", "host", f"{host}")
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)

            logger.info(
                f"User set `{host}` as his .env `PGHOST` environment variable in Config.change_PostgreSQL_host "
            )
            return True
        except:
            logger.exception(f"An error in config.change_PostgreSQL_host ")
            return False

    def change_PostgreSQL_port(self, port):
        """
        Updates the PostgreSQL port in the .env and config file.

        Args:
            port (str or int): New port number.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.__set_env_variable(full_text=f"PGPORT={port}")
            self.config.set("postgresql", "port", f"{port}")
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)

            logger.info(
                f"User set `{port}` as his .env `PGPORT` environment variable in Config.change_PostgreSQL_port "
            )
            return True
        except:
            logger.exception(f"An error in config.change_PostgreSQL_port ")
            return False

    @staticmethod
    def __set_env_variable(full_text):
        """
        Updates or adds an environment variable in the .env file.

        Args:
            full_text (str): The environment variable in `KEY=value` format.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            env_file = Path(".env")
            if not env_file.exists():
                env_file.write_text(f"{full_text}\n")
                return True

            lines = env_file.read_text().splitlines()
            flag = False
            new_lines = []

            for line in lines:
                if line.strip().startswith(f"{full_text.split('=')[0]}="):
                    new_lines.append(full_text)
                    flag = True
                else:
                    new_lines.append(line)

            if not flag:
                new_lines.append(full_text)

            env_file.write_text("\n".join(new_lines) + "\n")
            return True
        except:
            logger.exception(f"An error in config.__set_env_variable for `{full_text}`")
            return False

    def fetch_telegram_flags(self):
        first = self.config.getboolean("telegram", "enabled", fallback=False)
        second = self.config.getboolean("telegram", "token", fallback=False)
        return first and second
