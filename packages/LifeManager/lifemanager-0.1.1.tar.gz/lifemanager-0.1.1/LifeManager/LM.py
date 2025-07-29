import datetime as dt
import inspect
import os
import subprocess
from collections import deque
from contextlib import contextmanager
from typing import Literal, Union
from uuid import UUID

import matplotlib.pyplot as plt
import pandas as pd
import psycopg2 as psql
from dotenv import load_dotenv
from matplotlib import colormaps
from psycopg2 import sql
from psycopg2.errors import (
    DuplicateDatabase,
    DuplicateTable,
    ForeignKeyViolation,
    InvalidTextRepresentation,
    UndefinedTable,
    UniqueViolation,
)
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from .BM import CBanker
from .Cursor import Cursor
from .logger_config import logger
from .TM import CTimer


class LifeManager(Cursor):

    def __init__(self, minconn=1, maxconn=10):

        load_dotenv()
        super().__init__(minconn, maxconn)

        self.make_psql_db()

        self.current_week_name = None

        self.make_weekly_tables()

        # * Append the file path of where this class was called into the log file.
        stack = inspect.stack()
        if len(stack) > 1:
            caller_frame = stack[1]
            caller_info = f"{caller_frame.filename}:{caller_frame.lineno} in {caller_frame.function}"
        else:
            caller_info = "Caller info not available"

        logger.info(f"Made new instance of LifeManage — called from {caller_info}")

    def make_psql_db(self):

        #! NOTE: I specifically DID NOT use connection pool for this one because I the dbname is set to postgres and
        #! this method is a kick start for the database creation and What pool should give to a db that it isn't created
        #! Yet! LOL

        conn_params = {
            "dbname": "postgres",  # Connect to the default 'postgres' database
            "user": self._config["user"],
            "password": self._config["password"],
            "host": self._config["host"],
            "port": self._config["port"],
        }
        try:
            # Connect to the PostgreSQL server
            conn = psql.connect(**conn_params)
            conn.autocommit = True  # Enable autocommit for CREATE DATABASE

            cursor = conn.cursor()

            # Create the new database
            cursor.execute(sql.SQL("CREATE DATABASE workmanager;"))

            logger.info(f"Postgres Database initiated successfully!")
            return True

        except DuplicateDatabase:

            logger.info("Database is already initiated")
            return True

        except Exception as e:
            logger.exception(f"In database creation")
            return False

        finally:
            cursor.close()
            conn.close()

    def add_daily_task(self, task_name: str, *, ref_to=None) -> bool:

        if not self._create_daily_tasks_table():
            logger.critical(
                f"In add_daily_task WHEN it was Calling _create_daily_tasks_table Method."
            )
            return False  # ? It means that if the table creation fails, this method will fail as well

        # GOAL: If The referrer is None; Then if the task_name is not already a PARENT, It will make a parent row.
        if ref_to is None:
            if task_name not in self.get_all_parent_tasks():
                with self._cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO dailytasks (taskname) VALUES (%s)", (task_name,)
                    )
                    logger.info(f"Parent row {task_name} added successfully!")
                    return True

        try:
            with self._cursor() as cursor:

                # GOAL: This will fetch the PARENT id from db from the dailytasks.
                cursor.execute(
                    "SELECT id FROM dailytasks WHERE taskname = %s", (ref_to,)
                )
                parent_id = cursor.fetchone()[0]
                # If the fetchone be none, it raise an error and prevents the flow from going further.

                # GOAL: This will add the sub task to the TABLE.
                cursor.execute(
                    "INSERT INTO dailytasks (taskName, parentTaskId) VALUES (%s, %s)",
                    (task_name, parent_id),
                )

            return True

        except UniqueViolation:
            # CONCLUSION: Although Normally if would raise an error because od UNIQUE CONSTRAINT that I put, but here is will
            # CONCLUSION: return true because if this UniqueViolation occurs. it mean the user row is already in db and does not need to return False.
            logger.exception(f"In add_daily_task method, A dupe Key: ")
            return True
        except Exception as e:

            logger.exception(f"In add_daily_task method")
            return False

    def _create_daily_tasks_table(self) -> bool:

        with self._cursor() as cursor:
            try:
                # GOAL: This Created The Table with Unique Constrain on both columns but not (taskName,NULL)
                cursor.execute(
                    """CREATE TABLE dailytasks (id SERIAL PRIMARY KEY, taskName TEXT, parentTaskId INTEGER,
                            CONSTRAINT FK_self_parent_name FOREIGN KEY (parentTaskId) REFERENCES dailytasks(id),
                            CONSTRAINT unique_rows UNIQUE(taskName, parentTaskId));"""
                )

                # GOAL: Now I manually made (taskName,NULL) a UNIQUE.
                cursor.execute(
                    """CREATE UNIQUE INDEX unique_null_parent_task ON dailytasks(taskName) WHERE parentTaskId IS NULL;"""
                )

                return True

            except DuplicateTable:
                return True

            except UniqueViolation:
                logger.exception(
                    f"In _create_daily_tasks_table Method You have Duplicate Key: "
                )
                return True
            except Exception as e:
                logger.exception(f"In _create_daily_tasks_table Method:")

                return False

    def get_all_parent_tasks(self):
        with self._cursor() as cursor:
            cursor.execute("SELECT * from dailytasks WHERE parentTaskId IS NULL")
            return [i[1] for i in cursor.fetchall()]

    def make_weekly_tables(self):
        date = dt.datetime.now(dt.timezone.utc).isocalendar()
        year, week = date.year, date.week

        self.current_week_name = f"y{year}w{week}"

        table_name = f"y{year}w{week}"

        with self._cursor() as cursor:
            try:
                query = sql.SQL(
                    """CREATE TABLE IF NOT EXISTS {table} (
                                id SERIAL PRIMARY KEY, 
                                weekDay INT,
                                duration NUMERIC(12,2) NOT NULL, 
                                taskID INT NOT NULL , 
                                description TEXT,
                                CONSTRAINT {const} FOREIGN KEY (taskID) REFERENCES dailytasks(id)
                                )
                                """
                ).format(
                    table=sql.Identifier(table_name),
                    const=sql.Identifier(f"FK_{table_name}_taskid"),
                )

                cursor.execute(query)
                logger.info(f"TABLE {table_name} has created successfully.")
                return True

            except:
                logger.exception(f"An Error occurred while making {table_name} TABLE: ")
                return False

    def show_all_tables(
        self, table_schema: str = "public", table_type: str = "BASE TABLE"
    ) -> list | bool:

        try:
            with self._cursor() as cursor:
                query = sql.SQL(
                    """
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = {schema} 
                    AND table_type = {ttype}
                    ORDER BY table_name
                """
                ).format(
                    schema=sql.Literal(table_schema), ttype=sql.Literal(table_type)
                )

                cursor.execute(query)
                tables = cursor.fetchall()

            return [x[0] for x in tables]
            return "\n".join(f"{i}. {j[0]}" for i, j in enumerate(tables, start=1))

        except:
            logger.exception("In show_all_tables Method: ")
            return False

    def insert_into_weekly_table(
        self, duration: float, task_id: int, description: str = None
    ) -> bool:

        if not self.make_weekly_tables():
            logger.error("In insert_into_weekly_table, make_weekly_tables got an error")
            return False

        with self._cursor() as cursor:
            s_i = sql.Literal

            try:
                query = sql.SQL(
                    "INSERT INTO {} (weekDay, duration, taskid, description) VALUES ({},{},{},{})"
                ).format(
                    sql.Identifier(self.current_week_name),
                    s_i(f"{dt.datetime.now(dt.timezone.utc).isocalendar().weekday}"),
                    s_i(f"{duration}"),
                    s_i(f"{task_id}"),
                    s_i(description),
                )
                cursor.execute(query)
                logger.info(
                    f"Inserted {duration} {task_id} {description} to the {[self.current_week_name]} TABLE."
                )
                return True
            except ForeignKeyViolation:
                logger.exception("insert_into_weekly_table Violated a FK CONSTRAINT: ")
                return False
            except InvalidTextRepresentation:
                logger.exception("Entered TEXT instead of int for duration/task_id")
                return False

            except Exception:
                logger.exception("An Uncached Exception Has Happened:")
                return False

    def timer(self) -> UUID | bool:
        """Makes a CTimer object. Use the uid that it returns to access the CTimer object using CTimer.get_instance() and then use the instance methods.


        Returns:
            UUID | bool: Returns the made CTimer uid, otherwise False
        """
        # ! have to make a timer object
        try:
            _ = CTimer()
            return _.uid
        except Exception:
            logger.exception("In Making a CTimer Object in LM.timer Method.")
            return False

    def backup(self):

        os.makedirs("backup", exist_ok=True)
        timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_path = f"backup/workmanager_backup_{timestamp}.backup"

        command = [
            "pg_dump",
            "-F",
            "c",
            "-f",
            output_path,
            "workmanager",
        ]

        try:
            subprocess.run(command, check=True)
            logger.info(f"✅ Backup successful: {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.info(f"❌ Backup failed: {e}")
            return False

    def restore_backup(self, backup_path: Literal["latest"] = "latest") -> bool:

        if backup_path == "latest":
            backup_path = os.path.abspath(
                os.path.join("backup", sorted(os.listdir("backup"))[-1])
            )
        restore_command = (
            f"pg_restore  -d workmanager --clean --if-exists {backup_path}"
        )

        try:
            subprocess.run(restore_command, check=True, shell=True)
            logger.info(
                f"Database 'workmanager' restored successfully from {backup_path}."
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.exception(f"Error occurred during restore: ")
            return False

    def fetch_all_rows(self, week: str = None) -> Union[pd.core.frame.DataFrame, bool]:

        if week is None:
            week = self.current_week_name
        try:
            # Makes an engin to connect to psql using pandas.
            engin = create_engine(
                f"postgresql://{os.environ["PGUSER"]}:{os.environ["PGPASSWORD"]}@{os.environ.get("PGHOST", "localhost")}:{os.environ.get("PGPORT", "5432")}/workmanager",
                pool_size=10,
            )

            query = f'SELECT * FROM "{week}"'
            logger.info(f"User Fetched {week} data.")
            return pd.read_sql(query, engin)

        except ProgrammingError as e:

            if isinstance(e.orig, UndefinedTable):
                logger.exception(
                    f"User tried to access a table '{week}' that is not in the DB."
                )
            else:
                logger.exception(f"An error occurred: {e}")
            return False

        except Exception:
            logger.exception(f"An error in fetch_all_rows")
            return False

    def chart_it(
        self,
        week: str = None,
        start_day: Literal[
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ] = "Saturday",
    ):
        if week is None:
            week = self.current_week_name

        # Makes an engin to connect to psql using pandas.
        try:
            engin = create_engine(
                f"postgresql://{os.environ["PGUSER"]}:{os.environ["PGPASSWORD"]}@{os.environ.get("PGHOST", "localhost")}:{os.environ.get("PGPORT", "5432")}/workmanager",
                pool_size=10,
            )

            query = f"SELECT weekday,duration,taskname FROM {week} as t JOIN dailytasks as d ON t.taskid = d.id;"

            df = pd.read_sql(query, engin)
            df["duration"] = df["duration"].apply(lambda x: round(x / 3600, 2))

        except UndefinedTable:
            return False
        except ProgrammingError:
            return False
        # ? Making a deque for flags

        flag: deque = deque(maxlen=3)

        #! Start to make the pie chart
        try:
            num_colors = df["taskname"].nunique()
            cmap = colormaps.get_cmap(cmap="Set3")
            colors = [cmap(i / num_colors) for i in range(num_colors)]

            df_data = df.groupby("taskname")["duration"].sum()
            plt.figure(figsize=(20, 10))
            plt.pie(
                x=df_data,
                labels=df_data.index,
                autopct="%1.2f%%",
                startangle=90,
                colors=colors,
                textprops={"fontweight": "bold"},
            )
            plt.legend()
            plt.title("What % You Spend on What", fontsize=20, fontweight="bold")
            plt.savefig(fname=f"figures/pie")

            logger.info("PIE chart created successfully.")
            flag.append(True)
        except Exception:
            logger.exception("An Error in making pie chart.")
            flag.append(False)

        #! Start TO make Barchart
        try:
            # GOAL: This is a mapping for week days and in my country week starts at Saturday thus, it is set to 1.
            week_days_map = {
                "Monday": 3,
                "Tuesday": 4,
                "Wednesday": 5,
                "Thursday": 6,
                "Friday": 7,
                "Saturday": 1,
                "Sunday": 2,
            }

            # GOAL: Reverse map of above for x axis in barchart.
            week_day_names = {
                3: "Monday",
                4: "Tuesday",
                5: "Wednesday",
                6: "Thursday",
                7: "Friday",
                1: "Saturday",
                2: "Sunday",
            }

            start_day_num = week_days_map[start_day]

            # GOAL: Make a df to just have weekday number and Sum of the durations, then sort it.
            df_data = df.groupby("weekday")["duration"].sum()

            weekly_data = {i: df_data.get(i, 0) for i in range(1, 8)}

            ordered_data = {
                ((i - start_day_num) % 7 + 1): weekly_data[i] for i in range(1, 8)
            }

            values = list(ordered_data.values())
            labels = [week_day_names[i] for i in ordered_data.keys()]

            # GOAL: plot it.
            plt.figure(figsize=(10, 6))
            plt.barh(list(ordered_data.keys()), values, color="skyblue")
            plt.yticks(list(ordered_data.keys()), labels)

            plt.title(
                "Total Duration for Each Day of the Week",
                fontsize=20,
                fontweight="bold",
            )
            plt.ylabel(f"Day of the Week (Starts on {start_day})", fontsize=14)
            plt.xlabel("Total Duration(In HOUR)", fontsize=14)
            plt.savefig(fname="figures/bar")

            flag.append(True)
        except Exception:
            logger.exception("An Error in making pie chart.")
            flag.append(False)

        #! Now let make the line chart
        try:
            eligible_weeks = [x for x in self.show_all_tables() if x.startswith("y20")]

            sub_query = (
                "SELECT '{week}' AS week, SUM(duration) AS total_duration FROM {week}"
            )

            main_query = [
                " UNION ALL ".join([sub_query.format(week=i) for i in eligible_weeks])
            ]

            df = pd.read_sql(main_query[0], engin)

            plt.figure(figsize=(20, 10))
            plt.plot(
                df["week"], df["total_duration"], marker="o", label="Total Duration"
            )
            if week in df["week"].values:
                current_week_index = df[df["week"] == week].index[
                    0
                ]  # Get the index of the current week
                plt.plot(
                    df["week"][current_week_index],
                    df["total_duration"][current_week_index],
                    marker="D",
                    color="red",
                    markersize=10,
                    label="Current Week",
                )

            plt.title("Weekly Total Duration")
            plt.xlabel("Week")
            plt.ylabel("Total Duration(In Hour)")
            plt.legend()

            plt.savefig(fname="figures/line")
            logger.info("LINE chart created successfully.")
            flag.append(True)
        except:
            logger.exception("An Error in making Line chart")
            flag.append(False)
        if flag[0] and flag[1] and flag[2]:
            return True
        else:
            return False

    def fetch_task_id(self, task_name: str):
        try:
            with self._cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM dailytasks WHERE taskname = %s;", (task_name,)
                )

                task_id = cursor.fetchone()

            if task_id is None:
                return False

            return task_id[0]
        except:
            logger.exception(
                "there was an error while fetching task id in LifeManager.fetch_task_id"
            )
            return False

    def fetch_all_non_parent_tasks(self) -> list:
        try:
            with self._cursor() as cursor:
                cursor.execute(
                    "SELECT taskname FROM dailytasks WHERE parenttaskid is not null;"
                )
                all_tasks = cursor.fetchall()

            return [x[0] for x in all_tasks]
        except:
            logger.exception(
                "there was an error while fetching non parent tasks. in LifeManager.fetch_all_non_parent_tasks"
            )
            return []

    @property
    def bank(self) -> bool:
        try:
            self.banker = CBanker()
            return True
        except Exception:
            logger.exception(
                "An Exception in making an CBanker instance in LM.bank method."
            )
            return False

    def fetch_child_tasks_of(self, parent_task_name: str) -> list:
        if parent_task_name not in self.get_all_parent_tasks():
            return []

        parent_id = self.fetch_task_id(task_name=parent_task_name)
        with self._cursor() as cursor:
            cursor.execute(
                "SELECT * FROM dailytasks WHERE parenttaskid = %s", (parent_id,)
            )
            return [i[1] for i in cursor.fetchall()]
