# Why I made LM(LifeManager)?


I have a lot of time slippage in my life and time passes without me realizing what I was doing with my time,So I decided to use my knowledge and make a python package that I track my day with better precision and then make a telegram interface for to use this everywhere using a telegramBOT.

____
# What is LifeManager?

It is basically a program that helps you track you daily tasks and expense and then you can get a report on what you done or how much you spend on something. You can get chart and excel files for your spend time and money.


# How to set it up

First You need to run:
```python
pip install LifeManager
```


Then Its time to set PostgreSQL <b>Username,Password,Host,port</b> :(If you know how to work with .env file, you can set it manually):
```python
from LifeManager.config import Config

cfg = Config()

cfg.change_PostgreSQL_user("your_username")
cfg.change_PostgreSQL_password("your_password")
cfg.change_PostgreSQL_host("your_host")   # e.g. "localhost"
cfg.change_PostgreSQL_port(5432) # or your custom port
```

## How to use Telegram BOT
If you don't want to work with the CLI version and just simply work with the a telegram bot, 

* first activate its flag with
```python
from LifeManager.config import Config

cfg = Config()

cfg.change_telegram_bot_status() # Remember That every time you run this you turn it on/off
```

* Then, you have to provide a valid <b>TELEGRAM BOT TOKEN</b>(You can fetch it from <a href="https://t.me/BotFather" target="_blank" rel="noopener noreferrer">BotFather</a>
) using:
```python
from LifeManager.config import Config

cfg = Config()

cfg.change_telegram_TOKEN(token="TELEGRAM_TOKEN")
# Remember if you enter invalid token, you get an error when you want to start the bot not here!!
```

* Now you simply can start/stop the bot with `start`/`stop` methods:

```python
import asyncio
from LifeManager.telegram_launcher import TelegramLauncher

async def main():
    launcher = TelegramLauncher()
    
    # Start the bot (checks flags, validates token, launches subprocess)
    started = await launcher.start()
    if not started:
        return

    # Keep the script running until interrupted
    try:
        print("Bot is running. Press Ctrl+C to stop.")
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the bot subprocess gracefully
        await launcher.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

Your Done! Enjoy ....

## How to use it raw

In LifeManager Package we have several modules and one sub-package(telegramBOT) :

<table border="1" cellpadding="5" cellspacing="0">
  <thead>
    <tr>
      <th>Module Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>BM</td><td>Controls Banking Section</td></tr>
    <tr><td>LM</td><td>Controls Main Task Section</td></tr>
    <tr><td>TM</td><td>Controls Time Object</td></tr>
    <tr><td>config</td><td>Configs for run the package</td></tr>
    <tr><td>Cursor</td><td>A postgreSQL cursor</td></tr>
    <tr><td>logger_config</td><td>A logger file</td></tr>
    <tr><td>telegram_launcher</td><td>Validate and launches telegram sub-package</td></tr>
    
  </tbody>
</table>

Now I will Explain each module in depth.

## BM Module

The **BM module** provides a comprehensive class `CBanker` designed to manage banking data and transactions efficiently. It handles the creation and management of banking tables, allows you to add banks and expense types, make transactions, and retrieve bank records with ease.

### Key Features:

- **Table Management:** Automatically creates and manages necessary database tables related to banks, bankers, and expense types.
- **Bank Management:** Add new banks and retrieve bank details seamlessly.
- **Expense Types:** Organize and add expense types with support for parent-child hierarchies.
- **Transactions:** Record transactions with detailed information including bank name, amount, expense type, and optional descriptions.
- **Data Retrieval:** Fetch transaction records between specified dates and export them to Excel for analysis.
- **Analytics:** Generate simple charts for recent transaction data (e.g., last 30 days).
- **Bank Initialization:** Retrieve the first recorded transaction date for any bank.

### Usage Overview:

```python
from LifeManager.BM import CBanker

banker = CBanker()

# Create necessary tables (banks, bankers, expense types)
banker.make_tables()

# Add a new bank
banker.add_bank("MyBank")

# Add an expense type (optionally under a parent category)
banker.add_expense("Utilities")

# Make a transaction
banker.make_transaction(
    bank_name="MyBank",
    amount=150.0,
    expense_type="Utilities",
    description="Electricity bill"
)

# Fetch transactions between dates for a bank and export to Excel
banker.fetch_records("MyBank", "2025-01-01", "2025-01-31")

# Show all banks
banker.show_all_banks()

# Get the date of the first transaction for a bank
first_date = banker.bank_first_init_time("MyBank")
print(f"First transaction date: {first_date}")
```

## LM Module

The **LM module** provides the `LifeManager` class, a robust solution for personal productivity and time-tracking built on PostgreSQL. It enables you to create and manage daily and weekly task tables, track time spent on tasks, backup and restore your database, and visualize your productivity with charts.

### Key Features:

- **Database Initialization:**  
  - `make_psql_db()`: Create a PostgreSQL database using your `.env` `PSQ_*` settings.  
  - `_create_daily_tasks_table()`: Create the master daily tasks table.  
  - `make_weekly_tables()`: Dynamically create a table for the current year & week (e.g., `y2025w21`).  

- **Task Management:**  
  - `add_daily_task(task_name, ref_to=None)`: Add a parent task or subtask (if `ref_to` is provided).  
  - `get_all_parent_tasks()`: List all parent (top-level) tasks.  
  - `fetch_all_non_parent_tasks()`: List all subtasks.  
  - `fetch_task_id(task_name)`: Retrieve the database ID for any task.  
  - `fetch_child_tasks_of(parent_task_name)`: Get all subtasks under a given parent.

- **Time Tracking:**  
  - `insert_into_weekly_table(duration, task_id, description=None)`: Log minutes spent on a task in the current week’s table.  
  - `timer()`: Start a timer session and return its UUID.

- **Backup & Restore:**  
  - `backup()`: Dump the entire database into a timestamped backup folder.  
  - `restore_backup(backup_path="latest")`: Restore from a specific backup file or the most recent one.

- **Data Retrieval & Analysis:**  
  - `fetch_all_rows(week=None) → pd.DataFrame`: Load all records from a specific weekly table into a pandas DataFrame.  
  - `show_all_tables(schema="public", table_type="BASE TABLE")`: List all tables in your database schema.

- **Visualization:**  
  - `chart_it(week=None, start_day="Saturday")`: Produce three charts saved in `figures/`:  
    1. **Pie chart** of task-duration distribution for the selected week  
    2. **Horizontal bar chart** of daily total durations (with custom start day)  
    3. **Line chart** of total weekly durations over time  

- **Cursor Pooling (Internal):**  
  - `__cursor()`: Context-managed cursor pool for safe, efficient DB access.

- **Banker Integration:**  
  - `@property bank`: Instantiates a `CBanker` object for integrated banking features.

### Usage Overview

```python
from LifeManager.LM import LifeManager

# Initialize manager with default connection pool settings
lm = LifeManager(minconn=1, maxconn=5)

# 1. Setup database and tables
lm.make_psql_db()
lm._create_daily_tasks_table()
lm.make_weekly_tables()

# 2. Add tasks
lm.add_daily_task("Health")
lm.add_daily_task("Morning Run", ref_to="Health")

# 3. Log time
task_id = lm.fetch_task_id("Morning Run")
lm.insert_into_weekly_table(duration=45, task_id=task_id, description="Park jog")

# 4. View tasks
print("Parents:", lm.get_all_parent_tasks())
print("Subtasks:", lm.fetch_child_tasks_of("Health"))

# 5. Backup & Restore
lm.backup()
lm.restore_backup()

# 6. Fetch & analyze
df = lm.fetch_all_rows("y2025w21")
if isinstance(df, pd.DataFrame):
    print(df.head())

# 7. Generate charts
lm.chart_it(start_day="Monday")

# 8. Use banking features
if lm.bank:
    lm.bank.add_bank("MyFinance")
```

## CTimer Module

The **CTimer module** provides the `CTimer` class, a versatile timer utility that lets you start, pause, resume, and stop multiple timers concurrently. Each timer is identified by a unique UUID and stored in a global registry for easy retrieval.

### Key Features:

- **Unique Timer Instances:**  
  - Each `CTimer()` generates a UUID and registers itself in `CTimer._instances`.  
  - Retrieve any timer later using `CTimer.get_instance(uid)`.

- **Basic Timing Operations:**  
  - `start()`: Begin timing.  
  - `end()`: Stop timing (must have called `start()`).  
  - `time_it()`: Calculate elapsed time in seconds (automatically resumes if paused).

- **Pause & Resume:**  
  - `pause()`: Temporarily halt the timer.  
  - `resume()`: Continue timing, automatically accounting for pause durations.

- **Logging:**  
  - Automatically logs creation of new timer instances via the configured logger.

- **UUID Management:**  
  - `get_uid()`: Retrieve the UUID for later reference.  
  - `CTimer._instances`: Class-level dict of all active timers.

### Usage Overview

```python
from LifeManager.TM import CTimer  # adjust import path as needed

# Create a new timer
timer = CTimer()
uid = timer.get_uid()

# Start timing
timer.start()

# ... perform some operations ...
timer.pause()
# ... during pause, code runs without being counted ...
timer.resume()

# Stop timing and get elapsed seconds
timer.end()
elapsed = timer.time_it()
print(f"Elapsed time: {elapsed} seconds")

# Retrieve the same timer later using its UUID
same_timer = CTimer.get_instance(uid)
assert same_timer is timer
```

## Config Module

The **Config module** provides the `Config` class to manage application settings for LifeManager. It handles reading and writing a `config.ini` file, safely updating environment variables in a `.env` file, and toggling Telegram and PostgreSQL credentials.

### Key Features:

- **Config File Management**  
  - `_load_config()`: Load `config.ini` or create it with sensible defaults (`telegram`, `backup`, `postgresql` sections).  
  - Reads and writes values to `config.ini` automatically.

- **Telegram Bot Configuration**  
  - `change_telegram_bot_status()`: Toggle the `telegram.enabled` flag in `config.ini`.  
  - `change_telegram_TOKEN(token)`: Safely set `TELEGRAM_TOKEN` in `.env` and mark `telegram.token = true` in `config.ini`.

- **PostgreSQL Credentials**  
  - `change_PostgreSQL_user(user_name)`, `change_PostgreSQL_password(password)`,  
    `change_PostgreSQL_host(host)`, `change_PostgreSQL_port(port)`:  
    Update PGUSER, PGPASSWORD, PGHOST, PGPORT in `.env` and mirror user/host/port in `config.ini`.

- **Environment Variable Handling**  
  - `__set_env_variable(full_text)`: Add or update a single `KEY=value` line in the project’s `.env` file without disturbing other entries.

- **Flag Retrieval**  
  - `fetch_telegram_flags()`: Return `True` only if both `telegram.enabled` and `telegram.token` are `true`.

### Usage Overview

```python
from LifeManager.config import Config

# Initialize (loads or creates config.ini + defaults)
cfg = Config("config.ini")

# Toggle Telegram bot on/off
enabled = cfg.change_telegram_bot_status()
print("Telegram enabled:", enabled)

# Set a new Telegram token
success = cfg.change_telegram_TOKEN("123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
print("Token update successful:", success)

# Update PostgreSQL credentials
cfg.change_PostgreSQL_user("dbuser")
cfg.change_PostgreSQL_password("s3cr3t")
cfg.change_PostgreSQL_host("localhost")
cfg.change_PostgreSQL_port(5432)

# Check if Telegram is fully configured
if cfg.fetch_telegram_flags():
    print("Telegram bot is configured and ready.")
else:
    print("Telegram bot is not yet configured.")
```

## Cursor Module

The **Cursor module** provides the `Cursor` class, a thin wrapper around a PostgreSQL connection pool with context-managed cursors. It simplifies acquiring connections, executing queries, and handling transactions (commit/rollback) automatically.

### Key Features:

- **Connection Pooling**  
  - Uses `psycopg2.pool.SimpleConnectionPool` to maintain a pool of reusable database connections.  
  - Configurable minimum and maximum connections (`minconn`, `maxconn`).

- **Environment-Driven Configuration**  
  - Loads `.env` with `python-dotenv` to populate `PGUSER`, `PGPASSWORD`, `PGHOST`, and `PGPORT`.  
  - Defaults to database name `workmanager` (override by editing `.env` or code).

- **Context-Managed Cursors**  
  - `@contextmanager _cursor()`:  
    - Acquires a connection and cursor.  
    - Yields the cursor for query execution.  
    - Commits on success or rolls back on exception.  
    - Ensures cursor is closed and connection is returned to the pool.

- **Logging**  
  - Exceptions during query execution are logged via the configured logger.

### Usage Overview

```python
from LifeManager.cursor import Cursor  # adjust import path if needed

# Initialize with a pool of 1–5 connections
db = Cursor(minconn=1, maxconn=5)

# Use the context-managed cursor for queries
with db._cursor() as cur:
    # Create a table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS example (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    # Insert a row
    cur.execute("INSERT INTO example (name) VALUES (%s)", ("Alice",))

# Fetch data
with db._cursor() as cur:
    cur.execute("SELECT id, name FROM example")
    rows = cur.fetchall()
    for row in rows:
        print(row)
```

## Logger Config Module

All logging functionality is centralized in the **logger_config** folder so every module writes to the same rotating log directory. The `logger` object provided here can be imported and used across your application.

### Key Features:

- **Shared Logger Instance**  
  - A single `shared_logger` is configured at `DEBUG` level.  
  - Prevents duplicate handlers by checking if handlers already exist.

- **Dynamic Log Files**  
  - Creates a `log/` directory (if not already present).  
  - Each run generates a new log file named with the current timestamp (`DD-MM-YYYY--HH-MM-SS.log`).

- **Structured Formatting**  
  - Log entries use the format:  
    ```
    2025-05-23 14:30:01,234 - INFO - Message text
    ```

### Usage Overview

```python
from LifeManager.logger_config import logger

# Log informational message
logger.info("Application started")

# Log debugging details
logger.debug("Debugging variable x = %s", x)

# Log warnings and errors
logger.warning("This is a warning")
logger.error("An error occurred", exc_info=True)
```

## Telegram Launcher Module

The **telegram_launcher** module provides `TelegramLauncher`, an async helper to validate and launch your Telegram bot process using `aiogram`. It checks configuration flags, verifies the bot token, and manages the bot subprocess lifecycle.

### Key Features:

- **Flag & Token Validation**  
  - `__check_flags()`: Ensures `telegram.enabled` and `telegram.token` are set in `config.ini`.  
  - `__is_token_valid(token)`: Asynchronously verifies the token by calling `Bot.get_me()` via `aiogram`.  

- **Bot Launch & Shutdown**  
  - `start()`:  
    1. Reloads environment variables.  
    2. Checks flags and presence of `TELEGRAM_TOKEN` in `.env`.  
    3. Validates token with Telegram API.  
    4. Spawns the bot subprocess (`python -m LifeManager.telegram.telegram`) on success.  
  - `stop()`: Gracefully terminates the bot process, with timeout and forced kill fallback.

- **Environment Loading**  
  - Uses `python-dotenv` to load/override `.env` variables each run.  

- **Logging & Console Feedback**  
  - Prints status messages to the console (`print`) and logs via shared `logger`.  
  - Logs critical failures (missing flags/token), invalid tokens, and process lifecycle events.

### Usage Overview

```python
import asyncio
from LifeManager.telegram_launcher import TelegramLauncher

async def main():
    launcher = TelegramLauncher()

    # Start the bot (validates config and token)
    success = await launcher.start()
    if not success:
        return

    # ... bot is running as a separate process ...

    # To stop the bot later:
    await launcher.stop()

if __name__ == "__main__":
    asyncio.run(main())
```