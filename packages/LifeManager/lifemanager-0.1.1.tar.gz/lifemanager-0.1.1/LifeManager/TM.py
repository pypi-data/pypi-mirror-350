"""
This module provides a simple `CTimer` class that allows tracking multiple timer instances concurrently.

Each timer instance is assigned a unique UUID and automatically registered in a class-level `_instances` dictionary.
You can access all existing timers via `CTimer._instances` and retrieve a specific instance using its UUID.

To reliably access a timer later, make sure to store its `uid` when you create it.
You can retrieve the `uid` using the `get_uid` method.
"""

import datetime as dt
import uuid
from typing import ClassVar, Dict

from .logger_config import logger


class CTimer:
    """
    This Class Represents a unique way of making a Timer object to measure time by using two datetime object.
    """

    _instances: ClassVar[Dict[uuid.UUID, "CTimer"]] = dict()

    def __init__(self):
        self.uid = uuid.uuid4()
        CTimer._instances[self.uid] = self
        logger.info(f"Made new instance of CTimer class with the UUID of : {self.uid}")
        self.__start = None
        self.__end = None
        self.__pause = None
        self.__total_pause_duration = dt.timedelta(0)

    def get_uid(self):
        return self.uid

    @classmethod
    def get_instance(cls, uid):
        return cls._instances.get(uid)

    def time_it(self) -> float | bool:
        """This Method returns a float number representing the number of seconds between start and finish.

        Raises:
            ValueError: It raises when you dont initiate start Method.

        Returns:
            float | bool: Return the seconds in float; Or returns False if any exceptions happens; check logs.
        """
        try:
            if not self.__start:
                raise ValueError(
                    f"Object CTimer with UUID of `{self.uid}` does not have any start attribute."
                )
            if self.__pause is not None:
                self.resume()

            end_time = self.__end or dt.datetime.now()
            _ = (end_time - self.__start - self.__total_pause_duration).total_seconds()

            self.__start = None
            return _
        except Exception:
            logger.exception("In CTimer time_it method: ")
            return False

    def start(self) -> None:
        """Makes a new datetime.datetime.now object and sets it to the start attribute"""
        self.__start = dt.datetime.now()
        self.__pause = None
        self.__total_pause_duration = dt.timedelta(0)

    def end(self) -> None:
        """Makes a new datetime.datetime.now object and sets it to the start attribute"""
        if not self.__start:
            raise ValueError("First Initiate the start using **start** method")
        self.__end = dt.datetime.now()

    def pause(self):
        """Pauses the timer and records the pause duration"""

        if not self.__start:
            raise ValueError("First initiate the start using **start** method")

        if self.__pause is not None:
            raise ValueError("Timer is already paused.")

        self.__pause = dt.datetime.now()

    def resume(self) -> None:
        """Resumes the timer after being paused"""
        if self.__pause is None:
            raise ValueError("Timer has not been paused.")

        pause_duration = dt.datetime.now() - self.__pause
        self.__total_pause_duration += pause_duration
        self.__pause = None
