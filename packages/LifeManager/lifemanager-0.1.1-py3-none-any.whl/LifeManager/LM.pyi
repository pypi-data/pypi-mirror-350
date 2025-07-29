import datetime as dt
from contextlib import contextmanager
from typing import Generator, Literal, Optional, Union
from uuid import UUID

import pandas as pd

class LifeManager:
    def __init__(self, minconn: int = 1, maxconn: int = 10): ...
    @contextmanager
    def __cursor(self) -> Generator:
        """Makes a cursor pool and yields a cursor from the pool."""
        ...

    def make_psql_db(self) -> bool:
        """Create a PostgreSQL database based on .env "PSQ_*" parameters.

        Returns:
            bool: True if the database is created successfully, otherwise False.
        """
        ...

    def add_daily_task(self, task_name: str, *, ref_to: Optional[str] = None) -> bool:
        """This method adds a task to the task table. For example, you might add 'Udemy' as a subtask of 'Learning'.

        **NOTE: If ref_to is None, it will create a parent task.**
        **NOTE: It will return False if ref_to does not exist; first, add it manually.**

        Args:
            task_name (str): The task name to add (could be a main task if ref_to is None).
            ref_to (Optional[str]): The task to refer to (parent task). Defaults to None.

        Returns:
            bool: True if the task was added successfully, otherwise False.
        """
        ...

    def _create_daily_tasks_table(self) -> bool:
        """Create the Tasks table in the database.

        Returns:
            bool: True if the table was created successfully, otherwise False.
        """
        ...

    def get_all_parent_tasks(self) -> list[str]:
        """Return a list of all parent tasks in the DailyTasks table.

        Returns:
            list[str]: A list of parent task names.
        """
        ...

    def make_weekly_tables(self) -> bool:
        """Create a table for the current year and week (e.g., y2025w16 for week 16 of 2025).

        Returns:
            bool: True if the table was created successfully, otherwise False.
        """
        ...

    def show_all_tables(
        self,
        table_schema: str = "public",
        table_type: Literal[
            "BASE TABLE", "VIEW", "FOREIGN TABLE", "LOCAL TEMPORARY"
        ] = "BASE TABLE",
    ) -> Union[str, bool]:
        """Return a string containing all tables using the provided schema and table type.

        Args:
            table_schema (str, optional): Defaults to "public".
            table_type (str, optional): Defaults to "BASE TABLE".

        Returns:
            str | bool: The list of tables as a string or False if no tables exist.
        """
        ...

    def insert_into_weekly_table(
        self, duration: float, task_id: int, description: Optional[str] = None
    ) -> bool:
        """Insert a row into the current weekly table with the provided duration, task ID, and description.

        Args:
            duration (float): The duration in minutes.
            task_id (int): The task ID to update.
            description (Optional[str]): A brief description. Defaults to None.

        Returns:
            bool: True if the insert was successful, otherwise False.
        """
        ...

    def timer(self) -> Union[UUID, bool]:
        """Create a CTimer object and return its UID.

        Returns:
            UUID | bool: The CTimer UID, or False if creation failed.
        """
        ...

    def backup(self) -> bool:
        """Generate a backup of the entire database and store it in the backup folder.

        Returns:
            bool: True if the backup process was successful, otherwise False.
        """
        ...

    def restore_backup(self, backup_path: str = "latest") -> bool:
        """Restore the desired backup file using its path.

        Args:
            backup_path (str, optional): Full path of the backup or "latest" to restore the most recent backup. Defaults to "latest".

        Returns:
            bool: True if the restore process was successful, otherwise False.
        """
        ...

    def fetch_all_rows(self, week: str = None) -> Union[pd.DataFrame, bool]:
        """
        Fetch all rows from the specified week table and return them as a pandas DataFrame.

        Args:
            week (str, optional): The name of the week table to fetch, in the format 'y{year}w{week_number}',
                e.g., 'y2025w18'. Defaults to None.

        Returns:
            pd.DataFrame | bool: A pandas DataFrame with the data, or False if the table does not exist.
        """

        ...

    def chart_it(
        self,
        week: str = None,
        start_day: Literal[
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ] = "Saturday",
    ):
        """
        Generate three different charts and save them in the **figures** folder:

        1. A pie chart showing the distribution of task durations for the selected week.
        2. A horizontal bar chart showing productivity (total duration) for each day of the selected week.
        3. A line chart showing total weekly durations across all weeks up to the current one.

        Args:
            week (str, optional): The week to inspect, in the format 'y{year}w{week_number}',
                e.g., 'y2025w18'. If not provided, the current week is used. Defaults to None.
            start_day (Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], optional):
                Specifies which day of the week should appear first on the horizontal bar chart.
                Defaults to "Saturday".
        """

        ...

    @property
    def bank(self) -> bool:
        """
        Create a CBanker object and store it in instance.banker.

        Returns:
            bool: True if the assignment was successful, otherwise False.
        """
        ...

    def fetch_task_id(self, task_name: str) -> int | bool:
        """Fetches and returns the id of desired task name.

        Args:
            task_name (str): The desired task name to fetch its id.

        Returns:
            int | bool: Returns the id if task name exists, otherwise False.
        """

    def fetch_all_non_parent_tasks(self) -> list:
        """Returns a list of all Non-Parent tasks in dailytasks TABLE.

        Returns:
            list: Returns a list of strings, otherwise an empty list.
        """
        ...

    def fetch_child_tasks_of(self, parent_task_name: str) -> list:
        """Retrieves all child tasks associated with the specified parent task name.

        Args:
            parent_task_name (str): The name of the parent task whose child tasks are to be fetched.

        Returns:
            list: An empty list if the specified task is not a parent, otherwise a list of its child tasks.

        Example:
            >>> task_manager.fetch_child_tasks_of("MainTask")
            ["SubTask1", "SubTask2"]
        """
        ...
