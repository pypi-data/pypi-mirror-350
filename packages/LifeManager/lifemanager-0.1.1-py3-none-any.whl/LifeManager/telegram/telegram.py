import asyncio
import os
import zipfile

from aiogram import F, types
from dotenv import load_dotenv

load_dotenv()
import datetime as dt
import random

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = os.environ["TELEGRAM_TOKEN"]

from aiogram.types import FSInputFile, InputMediaPhoto

admins = [7860498898, 6739019257]
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from LifeManager.LM import LifeManager
from LifeManager.logger_config import logger
from LifeManager.TM import CTimer

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
lm = LifeManager()
tm = CTimer()
lm.bank
bnk = lm.banker

# $ Just Some Stickers to make the bot feel better when I use /panel. You can remove it.
greetings_stickers = {
    "CAACAgEAAxkDAAIF8mgoljxXu4cOATpntCR4am3xerdsAAK6CAACv4yQBD76oe4k-VsjNgQ",
    "CAACAgEAAxkBAAIGOmgomJY58hUN5ktUaDUh0tiFacuMAAK8CAACv4yQBIh7DqWx87_qNgQ",
    "CAACAgEAAxkBAAIGQGgomJuITCbraQ9W8D-6LDqG92mxAAK_CAACv4yQBDfiaQyBhaE8NgQ",
    "CAACAgEAAxkBAAIGQ2gomKDe4Dp7FerU-vlykD32QaNtAALFCAACv4yQBEv8iQmoZ8RdNgQ",
    "CAACAgEAAxkBAAIGT2gomKucMP2Ec6w_DIAseaBSsD7pAALQCAACv4yQBPKFEqs70wjINgQ",
    "CAACAgEAAxkBAAIGMWgomIj2PECis2xgiL2FbsSEWcClAAKxCAACv4yQBGXO3y8nkM42NgQ",
    "CAACAgEAAxkBAAIGNGgomI6iiWpngCPySxrF-pgI54qQAAKyCAACv4yQBPukvERwiE7xNgQ",
    "CAACAgEAAxkBAAIGSWgomKRbBZBtOC57No_cHsb66dzLAALKCAACv4yQBGmBuoEe-tDoNgQ",
    "CAACAgEAAxkBAAIGPWgomJnTVEXeVWPPjZjPfm8hQ54eAAK9CAACv4yQBFwhpxphQFLjNgQ",
    "CAACAgEAAxkBAAIGVWgomK_f0jEpY7PGyM_8bsjY2ZSKAALkCAACv4yQBAp4Myz2u0UxNgQ",
    "CAACAgEAAxkBAAIGLmgomIK5GUv0pdhNyy4cvs8V5nGIAALGCAACv4yQBDqECXvzUl6ENgQ",
    "CAACAgEAAxkBAAIGN2gomJIms6eSCfwBHL7ZreyXuMLUAAK0CAACv4yQBN0UndkxfeZoNgQ",
    "CAACAgEAAxkBAAIGUmgomK1ztWjeIwt3QtQsRQ9FhWGNAALlCAACv4yQBFF9pHeBVnyNNgQ",
    "CAACAgEAAxkBAAIGW2gomMHzIMLJGofMpIz9ImpTkKYBAAK1CAACv4yQBDfDX6YAAdyOMTYE",
    "CAACAgEAAxkBAAIGXmgomMi7dwvW1LxiV6adjFD2-2EPAALRCAACv4yQBDCBtOEKh2ORNgQ",
    "CAACAgEAAxkBAAIGRmgomKJ8cCBfRZ-jV6WhwKwR8rGaAALICAACv4yQBFfKmbh-BZmKNgQ",
    "CAACAgEAAxkBAAIGTGgomKj9F97ErfQzSRmG0TOJjoEfAALPCAACv4yQBKsJSWpxRk2RNgQ",
}


def is_admin(id) -> bool:
    return id in admins


# TODO: Add a function to user uses its own time in if the selected output is no async def process_duration(call: types.CallbackQuery, state: FSMContext):
#! I want to work with inlines and callbacks. It is my preference.


@dp.message(lambda x: x.text == "/panel" and is_admin(x.from_user.id))
async def main_panel(msg):

    builder = InlineKeyboardBuilder()

    builder.button(text="DTM", callback_data="daily_task_manager")
    builder.button(text="Banking", callback_data="banking")
    builder.button(text="Chartings", callback_data="charting")
    builder.button(text="Backup/Restore", callback_data="go_to_backups")

    builder.adjust(2)

    __keyboard = builder.as_markup()
    random_sticker = random.choice(list(greetings_stickers))
    await msg.answer_sticker(sticker=random_sticker)
    # ~ Assign the sticker in a global variable to delete it when recalling this to prevent the un necessary pollution.

    await msg.answer(text="🎛 Admin Panel", reply_markup=__keyboard)


@dp.callback_query(F.data == "/panel")
async def main_panel_callback(call: types.CallbackQuery):
    await call.answer()
    if not is_admin(call.from_user.id):
        return

    await call.message.delete()

    await call.bot.send_message(call.message.chat.id, "/panel")
    await main_panel(call.message)


#! ------------------------------- START | DAILY TASK MANAGER SECTION -------------------------------------
def main_dmt_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(text="Tasks", callback_data="go_to_tasks")

    builder.button(text="Timer", callback_data="timer")

    builder.button(text="⬅️ Return", callback_data="/panel")
    builder.adjust(2)

    return builder.as_markup()


def dmt_tasks_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Add New Records.",
                    callback_data="insert_into_weekly_table",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Add New Daily Task", callback_data="add_daily_task"
                )
            ],
            [
                InlineKeyboardButton(
                    text="All Parent Tasks", callback_data="get_all_parent_tasks"
                ),
                InlineKeyboardButton(
                    text="All Tables", callback_data="show_all_tables"
                ),
            ],
            [InlineKeyboardButton(text="⬅️ Return", callback_data="daily_task_manager")],
        ]
    )


def dmt_backup_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Backup", callback_data="backup"),
                InlineKeyboardButton(
                    text="Restore backup", callback_data="restore_backup"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Back up the whole Backup folder.",
                    callback_data="backup_whole_folder",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Back up log folder.",
                    callback_data="backup_whole_log_folder",
                )
            ],
            [InlineKeyboardButton(text="⬅️ Return", callback_data="daily_task_manager")],
        ]
    )


@dp.callback_query(F.data == "daily_task_manager")
async def dmt(call):
    await call.answer()
    if not is_admin(call.from_user.id):
        return

    await call.message.delete()
    await call.message.answer(text="Choose: ", reply_markup=main_dmt_keyboard())


@dp.callback_query(F.data == "go_to_tasks")
async def tasks_dmt(call):

    await call.answer()
    if not is_admin(call.from_user.id):
        return
    try:
        await call.message.delete()
    except:
        pass
    await call.message.answer(text="Choose2: ", reply_markup=dmt_tasks_keyboard())


@dp.callback_query(F.data == "go_to_backups")
async def backup_dmt(call):
    await call.answer()
    if not is_admin(call.from_user.id):
        return

    await call.message.delete()
    await call.message.answer(text="Choose2: ", reply_markup=dmt_backup_keyboard())


# ~ -----------START |  Timer section ---------------


def timer_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Start Timer", callback_data="s_timer"),
                InlineKeyboardButton(text="End Timer", callback_data="e_timer"),
            ],
            [
                InlineKeyboardButton(text="Pause Timer", callback_data="p_timer"),
                InlineKeyboardButton(text="Resume Timer", callback_data="r_timer"),
            ],
            [InlineKeyboardButton(text="⬅️ Return", callback_data="daily_task_manager")],
        ]
    )


@dp.callback_query(F.data == "timer")
async def _timer(call: types.CallbackQuery):
    await call.answer()
    if not is_admin(call.from_user.id):
        return

    await call.message.delete()
    await call.message.answer(
        text="<b>NOTE: Starting New timer will overwrite the old time</b>",
        reply_markup=timer_keyboard(),
        parse_mode="HTML",
    )


@dp.callback_query(F.data == "s_timer")
async def start_timer(call: types.CallbackQuery):
    await call.answer()
    if not is_admin(call.from_user.id):
        return

    try:

        tm.start()

        await call.message.answer(
            text="⏰ Your Time Has Been <b>Started</b>!",
            parse_mode="HTML",
        )
    except:
        await call.message.answer(text="An Error HasBeen occurred. Read Log Files")
        logger.exception("Cannot Start Timer in TelegramBOT.")


@dp.callback_query(F.data == "e_timer")
async def end_timer(call: types.CallbackQuery):

    await call.answer()
    if not is_admin(call.from_user.id):
        return
    global user_time_elapsed

    try:

        user_time_elapsed = tm.time_it()

        if not user_time_elapsed:
            await call.message.answer(
                text=f"You Need To First, <b>Start</b> the timer.",
                parse_mode="HTML",
            )
            return

        await call.message.answer(
            text=f"⏰ You Timer Has Been <b>Ended</b> Successfully.\nYou'r Time: {user_time_elapsed} Seconds.",
            parse_mode="HTML",
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Yes", callback_data="timer_yes"),
                    InlineKeyboardButton(text="No", callback_data="timer_no"),
                ],
                [InlineKeyboardButton(text="⬅️ Return", callback_data="timer")],
            ]
        )

        await call.message.answer(
            text=f"""<b>Note:</b> You can only store one time at a time. 
If you choose to store, it will replace the previous saved time.\n\n
<i>Please select an option below to proceed:</i>""",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

    except:
        await call.message.answer(text="An Error HasBeen occurred. Read Log Files")
        logger.exception("Cannot End Timer in TelegramBOT.")


@dp.callback_query(F.data == "p_timer")
async def pause_timer(call: types.CallbackQuery):
    await call.answer()
    if not is_admin(call.from_user.id):
        return
    try:
        tm.pause()
        await call.message.answer(
            text=f"⏰ You Timer Has Been <b>Paused</b> Successfully.",
            parse_mode="HTML",
        )

    except:
        await call.message.answer(
            text=f"You Need To First, <b>Start</b> the timer.",
            parse_mode="HTML",
        )
        logger.exception("Cannot Pause Timer in TelegramBOT.")


@dp.callback_query(F.data == "r_timer")
async def resume_timer(call: types.CallbackQuery):
    await call.answer()
    if not is_admin(call.from_user.id):
        return

    try:
        tm.resume()
        await call.message.answer(
            text=f"⏰ You Timer Has Been <b>Resumed</b> Successfully.",
            parse_mode="HTML",
        )

    except:
        await call.message.answer(
            text=f"You Need To First, <b>Start</b> the timer.",
            parse_mode="HTML",
        )
        logger.exception("Cannot Resume Timer in TelegramBOT.")


@dp.callback_query(lambda x: x.data.startswith("timer_"))
async def wanna_use_time(call: types.CallbackQuery):
    response = call.data[6:]

    global user_duration  # $ For Using in the Inserting into table

    if response == "yes":
        user_duration = user_time_elapsed
        await call.answer(f"✅ Selected {user_duration} ✅")
        await tasks_dmt(call)
    else:
        await call.answer(f"❌ Ignored The Time ❌")
        await _timer(call)
    try:
        await call.message.delete()
    except TelegramBadRequest:
        pass  # ! This Means The message is Already deleted


# ~ -----------END |  Timer section ---------------
#! ------------START | TASKS -------------------
class TasksState(StatesGroup):
    adding_daily_tasks = State()
    parent_or_child = State()
    which_parent = State()


# * -------START | add_daily_task query handler ---------
@dp.callback_query(lambda x: x.data == "add_daily_task")
async def add_daily_task(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if not is_admin(call.from_user.id):
        return
    await call.message.answer(
        "Now Send Me The Task that you want to add, So in the future you can work on it and use adding it to the weekly table : "
    )
    await state.set_state(TasksState.adding_daily_tasks)


@dp.message(TasksState.adding_daily_tasks)
async def process_adding_daily_tasks_state(message: Message, state: FSMContext):

    builder = InlineKeyboardBuilder()

    builder.button(text="👨 Parent", callback_data="parent_task")
    builder.button(text="👶 Child", callback_data="child_task")
    builder.button(text="❌ Abort", callback_data="abort")
    builder.adjust(2)
    keyboard = builder.as_markup()

    await message.answer(
        f"""Do you want to add the `<b>{message.text}</b>` as an parent task or a child task?\n
<b>NOTE:</b> For example watching `Youtube Tutorials` about programming can be a child class for `Programming`. Or it can be a PARENT that has for example `FreeCodeCamp` as its child.\n
The Parent/Chile relation comes back at YOUR PERSPECTIVE of the subject.""",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await state.update_data(task_name=message.text)  # User Response will be store here
    await state.set_state(TasksState.parent_or_child)


@dp.callback_query(TasksState.parent_or_child)
async def process_parent_or_child_state(call: types.CallbackQuery, state: FSMContext):

    if call.data == "abort":
        return await process_abort(call, state)  # Directly call the abort handler
    await call.answer()
    await state.update_data(
        parent_or_child=call.data
    )  # User Choice parent or child wil be store here

    data = await state.get_data()
    task_name = data.get("task_name")
    task_type = data.get("parent_or_child")

    if task_type == "parent_task":
        if lm.add_daily_task(task_name=task_name):
            await call.message.answer(
                text=f"✅ The {task_name} Has Been Added Successfully to the database."
            )
            return
        await call.message.answer(
            text=f"❌ There Was An Error Wile Adding {task_name} to the database."
        )
        return

    if task_type == "child_task":
        all_parents = lm.get_all_parent_tasks()
        builder = InlineKeyboardBuilder()
        for i in all_parents:
            builder.button(text=i, callback_data=f"parent_{i}")

        builder.button(text="❌ Abort", callback_data="abort")
        builder.adjust(2)
        keyboard = builder.as_markup()

        await call.message.answer(
            "Please Choose Your Desired Parent Task:", reply_markup=keyboard
        )
        await state.update_data(task_name=task_name)
        await state.set_state(TasksState.which_parent)


@dp.callback_query(TasksState.which_parent)
async def process_which_parent_state(call: types.CallbackQuery, state: FSMContext):
    if call.data == "abort":
        return await process_abort(call, state)  # Directly call the abort handler

    await call.answer()

    await state.update_data(which_parent=call.data)
    data = await state.get_data()
    task_name = data.get("task_name")
    parent_name = data.get("which_parent")[7:]

    if lm.add_daily_task(task_name=task_name, ref_to=parent_name):
        await call.message.answer(
            text=f"✅ The {task_name} Has Been Added Successfully to the database with {parent_name} as its Parent."
        )
        await state.clear()  # Clear FSM  state
        return
    else:
        await call.message.answer(
            text=f"❌ There Was An Error Wile Adding {task_name} to the database with {parent_name} as its Parent.\nHINT: Maybe the Parent Doesn't Exists."
        )
        await state.clear()  # Clear FSM state
        return


@dp.callback_query(lambda x: x.data == "abort")
async def process_abort(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Operation cancelled ❌", show_alert=True)
    await state.clear()  # Clear FSM state

    try:  #! Delete the message only if it was sent by the bot

        if call.message.from_user.id == call.bot.id:
            await call.message.delete()
    except:
        logger.exception(
            "an error while deleting the message in telegram.py's process_abort callback_query handler."
        )


# * -------END | add_daily_task query handler ---------


# $-------START | INSERT INTO WEEKLY TABLE ------
class InsertingIntoTABLE(StatesGroup):
    start_or_use_time = State()
    ask_duration = State()
    custom_duration = State()
    custom_duration_confirmation = State()
    custom_duration_H_M_S = State()
    which_task = State()
    which_child_task = State()
    update_which_task = State()
    update_which_child_task = State()
    description = State()
    confirmation = State()
    changing = State()


@dp.callback_query(F.data == "insert_into_weekly_table")
async def insert_into_weekly_tables(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
    try:
        if not user_duration:
            # $ Added This user_duration when the user Ended timer and said yes to saving it.
            raise NameError
    except NameError:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Start the timer", callback_data="start_or_use_time_timer"
                    ),
                    InlineKeyboardButton(
                        text="Enter Custom Time",
                        callback_data="start_or_use_time_custom",
                    ),
                ]
            ]
        )
        await call.message.answer(
            f"You Do not have a valid TIMER, Do you want to start the time or use custom timer?",
            reply_markup=keyboard,
        )

        await state.set_state(InsertingIntoTABLE.start_or_use_time)
        return
    except:
        logger.exception(
            "an Exception inside telegram.py module in insert_into_weekly_tables callback query handler."
        )
        return

    await call.answer()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes 👍", callback_data="insert_duration_yes"
                ),
                InlineKeyboardButton(text="NO 👎", callback_data="insert_duration_no"),
            ],
            [
                InlineKeyboardButton(
                    text="Yes - Send Your Own time",
                    callback_data="insert_duration_yup",
                ),
            ],
        ]
    )
    await call.message.answer(
        text=f"You Have `{user_duration}` Time Saved up, Do you want to use this?",
        reply_markup=keyboard,
        parse_mode="HTML",
    )

    await state.set_state(InsertingIntoTABLE.ask_duration)


@dp.callback_query(InsertingIntoTABLE.start_or_use_time)
async def process_duration(call: types.CallbackQuery, state: FSMContext):
    call.answer()

    data = call.data.split("start_or_use_time_")[1]
    if data == "timer":
        await _timer(call)
    else:

        await call.message.answer(
            "Please Enter Your Custom Duration <b>(the Second/Hour/Minute will pop up after you entered this)</b> : ",
            parse_mode="HTML",
        )
        await state.set_state(InsertingIntoTABLE.custom_duration_H_M_S)


@dp.callback_query(InsertingIntoTABLE.ask_duration)
async def process_duration(call: types.CallbackQuery, state: FSMContext):

    data = call.data[-3:]
    try:
        await call.message.delete()
    except:
        pass

    if data == "yes":
        builder = InlineKeyboardBuilder()
        for i in lm.get_all_parent_tasks():
            builder.button(text=i, callback_data=f"{i}_parent_task")
        builder.adjust(2)
        keyboard = builder.as_markup()

        await call.answer(
            f"You Selected {user_duration} as your time.",
            show_alert=True,
        )
        await call.message.answer(
            f"Which of these parent task you want add your task to ?:",
            reply_markup=keyboard,
        )
        await state.update_data(user_duration=user_duration)

        await state.set_state(InsertingIntoTABLE.which_child_task)

    elif data == "yup":
        await call.message.answer(
            "Please Enter Your Custom Duration <b>(the Second/Hour/Minute will pop up after you entered this)</b> : ",
            parse_mode="HTML",
        )
        await state.set_state(InsertingIntoTABLE.custom_duration_H_M_S)
    else:
        await call.answer(
            f"❌ Did not use the {user_duration} as your time, Please Start the new Timer(if you want to have new Timer) and try again ❌",
            show_alert=True,
        )
        await call.message.delete()
        await _timer(call)
        return


@dp.message(InsertingIntoTABLE.custom_duration_H_M_S)
async def process_custom_duration(msg: Message, state: FSMContext):
    try:
        custom_duration = int(msg.text)
        await state.update_data(user_custom_duration=custom_duration)
    except Exception:
        await msg.reply("PLEASE ENTER A VALID NUMBER.\n❌ABORTING...❌")
        await state.clear()
        await main_panel(msg)
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Hour", callback_data="custom_duration_1"),
                InlineKeyboardButton(
                    text="Minute", callback_data="custom_duration_0.5"
                ),
                InlineKeyboardButton(text="Seconds", callback_data="custom_duration_0"),
            ]
        ]
    )

    await msg.reply(f"What time entity is the time you sent?", reply_markup=keyboard)
    await state.set_state(InsertingIntoTABLE.custom_duration)


@dp.callback_query(InsertingIntoTABLE.custom_duration)
async def process_custom_duration(call: types.CallbackQuery, state: FSMContext):

    duration_aspect = float(call.data.split("custom_duration_")[1])
    data = await state.get_data()
    duration = data.get("user_custom_duration")
    # Because I save sec in the db, I have to transform it
    match duration_aspect:
        case 1:  # hour
            custom_duration = duration * 3600
            flag = "Hour"
        case 0.5:  # min
            custom_duration = duration * 60
            flag = "Minute"
        case 0:  # sec
            custom_duration = duration
            flag = "Seconds"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes 👍", callback_data="custom_duration_yes"
                ),
                InlineKeyboardButton(text="NO 👎", callback_data="custom_duration_no"),
            ]
        ]
    )
    await call.message.reply(
        f"Use <b>{duration} {flag}</b> as the Time?",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await state.update_data(custom_duration=custom_duration)
    await state.set_state(InsertingIntoTABLE.custom_duration_confirmation)


@dp.callback_query(InsertingIntoTABLE.custom_duration_confirmation)
async def process_which_child_task(call: types.CallbackQuery, state: FSMContext):
    _answer = call.data.split("custom_duration_")[1]

    data = await state.get_data()

    if _answer == "yes":
        user_duration = data.get("custom_duration")
        builder = InlineKeyboardBuilder()
        for i in lm.get_all_parent_tasks():
            builder.button(text=i, callback_data=f"{i}_parent_task")
        builder.adjust(2)
        keyboard = builder.as_markup()

        await call.answer(
            f"You Selected {user_duration} as your time.",
            show_alert=True,
        )
        await call.message.answer(
            f"Which of these parent task you want add your task to ?:",
            reply_markup=keyboard,
        )
        await state.update_data(user_duration=user_duration)

        await state.set_state(InsertingIntoTABLE.which_child_task)
    else:
        await insert_into_weekly_tables(call, state)


@dp.callback_query(InsertingIntoTABLE.which_child_task)
async def process_which_child_task(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    parent = call.data[:-12]
    tasks = lm.fetch_child_tasks_of(parent_task_name=parent)

    if not tasks:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Add a child", callback_data="add_daily_task"
                    )
                ]
            ]
        )
        await call.message.answer(
            text=f"No child tasks found for {parent}, Try Adding one..",
            reply_markup=keyboard,
        )
        await state.clear()
        return

    builder = InlineKeyboardBuilder()
    for i in tasks:
        builder.button(text=i, callback_data=f"{i}_task")
    builder.adjust(2)
    keyboard = builder.as_markup()

    await call.message.answer(
        text="Which of These Tasks You have done : ", reply_markup=keyboard
    )

    await state.set_state(InsertingIntoTABLE.which_task)


@dp.callback_query(InsertingIntoTABLE.which_task)
async def process_which_task(call: types.CallbackQuery, state: FSMContext):

    task_name = call.data[:-5]
    await state.update_data(user_task_name=task_name)

    await call.answer(f"✅ {task_name} ✅")
    await call.message.answer(
        f"🗞 Now Send me a DESCRIPTION of you'r work.\n\n<b>Send -1 to leave it empty.</b>",
        parse_mode="HTML",
    )

    await state.set_state(InsertingIntoTABLE.description)


@dp.message(InsertingIntoTABLE.description)
async def process_description_task(msg: Message, state: FSMContext):

    data = await state.get_data()

    desc = msg.text
    try:
        if int(desc) == -1:
            desc = None

    except ValueError:
        pass

    await state.update_data(description=desc)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Confirm", callback_data="insert_confirm_yes"
                ),
                InlineKeyboardButton(
                    text="Change", callback_data="insert_confirm_change"
                ),
            ],
            [InlineKeyboardButton(text="Abort", callback_data="insert_confirm_abort")],
        ]
    )

    await msg.reply(
        f"Do you want to add <b>{data.get("user_task_name")}</b> With <b>{data.get("user_duration")}</b> as your time, With description of: <b>{desc}</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await state.set_state(InsertingIntoTABLE.confirmation)
    # $ Now I have to control the flow for the user, first I have to make a callback query handler for insert_confirm_ , Then use the 3 states in it.


@dp.callback_query(InsertingIntoTABLE.confirmation)
async def control_user_flow_for_inserting_task(
    call: types.CallbackQuery, state: FSMContext
):

    choice = call.data.split("insert_confirm_")[1]

    if choice == "yes":
        data = await state.get_data()
        task_id = lm.fetch_task_id(task_name=data.get("user_task_name"))

        if lm.insert_into_weekly_table(
            duration=data.get("user_duration"),
            task_id=task_id,
            description=data.get("description"),
        ):
            await call.answer(
                f"✅ Added to the database. ({lm.current_week_name} TABLE)✅"
            )
            await state.clear()

            await main_panel_callback(call)
        else:
            await call.answer(f"❌ An Error Occurred, ABORTING... ❌")
            await state.clear()
            await tasks_dmt(call)

    elif choice == "change":
        await call.answer()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Task", callback_data="insert_change_task"
                    ),
                    InlineKeyboardButton(
                        text="Description", callback_data="insert_change_desc"
                    ),
                ]
            ]
        )
        await call.message.answer(
            "Which Step YOu want to chang:", reply_markup=keyboard
        )
        await state.set_state(InsertingIntoTABLE.changing)
    elif choice == "abort":
        await call.answer(f"❌ ABORTING... ❌")
        await state.clear()
        await tasks_dmt(call)


@dp.callback_query(InsertingIntoTABLE.changing)
async def changing_user_flow_insert(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = call.data[-4:]

    if data == "desc":
        await call.answer("You can now update the description.")

        await call.message.answer(
            "Please send the new description (or send -1 to leave it empty):"
        )

        await state.set_state(InsertingIntoTABLE.description)
    else:
        builder = InlineKeyboardBuilder()
        for i in lm.get_all_parent_tasks():
            builder.button(text=i, callback_data=f"{i}_parent_task2")
        builder.adjust(2)
        keyboard = builder.as_markup()

        await call.answer(
            f"Pre Selected {user_duration} as time.",
            show_alert=True,
        )
        await call.message.answer(f"Select You parent task: ", reply_markup=keyboard)

        await state.set_state(InsertingIntoTABLE.update_which_child_task)


@dp.callback_query(InsertingIntoTABLE.update_which_child_task)
async def updating_which_child_task(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()
    parent = call.data[:-13]

    tasks = lm.fetch_child_tasks_of(parent_task_name=parent)

    if not tasks:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Add a child", callback_data="add_daily_task"
                    )
                ]
            ]
        )

        await call.message.answer(
            text=f"No child tasks found for {parent}, Try Adding one..",
            reply_markup=keyboard,
        )
        await state.clear()
        return

    builder = InlineKeyboardBuilder()
    for i in tasks:
        builder.button(text=i, callback_data=f"{i}_task")
    builder.adjust(2)
    keyboard = builder.as_markup()

    await call.message.answer(text="Select your NEW child:", reply_markup=keyboard)

    await state.set_state(InsertingIntoTABLE.update_which_task)


@dp.callback_query(InsertingIntoTABLE.update_which_task)
async def updating_which_task(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()

    task_name = call.data.replace("_task", "")

    await state.update_data(user_task_name=task_name)

    await call.answer(f"✅ {task_name} ✅")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Confirm", callback_data="insert_confirm_yes"
                ),
                InlineKeyboardButton(
                    text="Change", callback_data="insert_confirm_change"
                ),
            ],
            [InlineKeyboardButton(text="Abort", callback_data="insert_confirm_abort")],
        ]
    )

    await call.message.reply(
        f"Do you want to add <b>{task_name}</b> With <b>{data.get("user_duration")}</b> as your time, With description of: <b>{data.get("description")}</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await state.set_state(InsertingIntoTABLE.confirmation)


# $-------END | INSERT INTO WEEKLY TABLE ------


@dp.callback_query(F.data == "get_all_parent_tasks")
async def _get_all_parent_tasks(call: types.CallbackQuery):
    await call.answer()
    if not is_admin(call.from_user.id):
        return
    parents = lm.get_all_parent_tasks()

    _ = [f"{i}. {j}\n" for i, j in enumerate(parents, start=1)]
    text = "🚨 Parent <b>TASKS</b>\n\n" + "".join(_)

    await call.message.answer(text=text, parse_mode="HTML")


@dp.callback_query(F.data == "show_all_tables")
async def show_all_tables(call: types.CallbackQuery):
    await call.answer()
    if not is_admin(call.from_user.id):
        return

    tables = lm.show_all_tables()

    _ = [f"{i}. {j}\n" for i, j in enumerate(tables, start=1)]
    text = "🚨 Available <b>TABLES</b>\n\n" + "".join(_)

    await call.message.answer(text=text, parse_mode="HTML")


#! ------------END | TASKS -------------------
# ? ------------START | BACKUP -------------------
@dp.callback_query(F.data == "backup")
async def backup_latest_file(call: types.CallbackQuery):

    if not is_admin(call.from_user.id):
        return

    if lm.backup():
        backup_file = os.path.join(
            os.environ["BACKUP_PATH"], sorted(os.listdir(os.environ["BACKUP_PATH"]))[-1]
        )

        await call.answer("✅ Backup Successful ✅", parse_mode="HTML")
        await call.message.answer_document(document=types.FSInputFile(backup_file))
    else:
        await call.answer("❌ Backing up Failed . ❌", parse_mode="HTML")


@dp.callback_query(F.data == "restore_backup")
async def restore_backup(call: types.CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    await call.answer(
        "📁 Please upload the backup file you want to restore.", show_alert=True
    )


@dp.message(F.content_type == types.ContentType.DOCUMENT)
async def handle_backup_file(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return

    file_id = msg.document.file_id
    file = await bot.get_file(file_id)

    os.makedirs(os.path.join("backup", "from_telegram"), exist_ok=True)
    file_path = os.path.join(
        os.environ["BACKUP_PATH"], "from_telegram", msg.document.file_name
    )

    await bot.download_file(file.file_path, destination=file_path)

    _ = await msg.answer(
        f"✅ File downloaded, Please Wait for restoring",
        parse_mode="HTML",
    )

    if lm.restore_backup(backup_path=file_path):
        await _.bot.send_message(
            chat_id=_.chat.id,
            text=f"✅ From <code>{file_path}</code>, Backup <b>Restored Successfully.</b>",
            parse_mode="HTML",
            reply_to_message_id=_.message_id,
        )

    else:
        await msg.answer(
            f"❌ file download to <code>{file_path}</code>, But There Was an error while <b>RESTORING</b>",
            parse_mode="HTML",
        )


@dp.callback_query(F.data == "backup_whole_folder")
async def backup_whole_folder(call: types.CallbackQuery):
    folder_path = os.path.join("backup")

    with zipfile.ZipFile("BACKUP.zip", "w", zipfile.ZIP_DEFLATED) as zipf:

        for root, dirs, files in os.walk(folder_path):
            for file in files:

                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), folder_path),
                )

    await call.answer("✅ Backup Successful ✅", parse_mode="HTML")
    await call.message.answer_document(document=types.FSInputFile("BACKUP.zip"))
    if os.path.exists("BACKUP.zip"):
        os.remove("BACKUP.zip")


@dp.callback_query(F.data == "backup_whole_log_folder")
async def backup_whole_log_folder(call: types.CallbackQuery):
    folder_path = os.path.join("log")

    with zipfile.ZipFile("LOGS.zip", "w", zipfile.ZIP_DEFLATED) as zipf:

        for root, dirs, files in os.walk(folder_path):
            for file in files:

                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), folder_path),
                )

    await call.answer("✅ Backup Successful ✅", parse_mode="HTML")
    await call.message.answer_document(document=types.FSInputFile("LOGS.zip"))
    if os.path.exists("LOGS.zip"):
        os.remove("LOGS.zip")


# ? ------------END | BACKUP -------------------
#! ------------------------------- END | DAILY TASK MANAGER SECTION -------------------------------------


#! ------------------------------- START | BANK MANAGER SECTION -------------------------------------
class Banking(StatesGroup):
    add_bank = State()
    add_bank_confirmation = State()
    add_expense = State()
    add_expense_2 = State()
    child_expense = State()
    confirmation_expense = State()
    fetch_child_expense = State()
    making_transaction = State()
    making_transaction_1 = State()
    making_transaction_2 = State()
    making_transaction_3 = State()
    making_transaction_4 = State()
    making_transaction_5 = State()
    fetch_record = State()
    fetch_record_1 = State()
    fetch_record_2 = State()
    fetch_record_3 = State()
    fetch_record_4 = State()
    fetch_record_5 = State()
    fetch_record_6 = State()
    fetch_record_7 = State()


@dp.callback_query(F.data == "banking")
async def main_banking(call: types.CallbackQuery):
    """Shows banking keyboard."""

    if not is_admin(call.from_user.id):
        return
    call.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Add BANK", callback_data="add_bank"),
                InlineKeyboardButton(
                    text="Add Expense", callback_data="add_an_expense"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Add Transaction", callback_data="make_transaction"
                )
            ],
            [
                InlineKeyboardButton(text="Banks", callback_data="show_banks"),
                InlineKeyboardButton(text="Expenses", callback_data="show_expenses"),
            ],
            [
                InlineKeyboardButton(
                    text="Fetch Banking Records.", callback_data="banking_records"
                )
            ],
            [InlineKeyboardButton(text="⬅️ Return", callback_data="/panel")],
        ]
    )

    await call.message.answer(text="choose", reply_markup=keyboard)


# $ ---------------- START | ADD BANK ---------------
@dp.callback_query(F.data == "add_bank")
async def add_a_bank(call: types.CallbackQuery, state: FSMContext):
    """Prompt to user to give bank name"""
    if not is_admin(call.from_user.id):
        return
    await call.answer()
    await call.message.answer("Please Provide Your bank name :")
    await state.set_state(Banking.add_bank)


@dp.message(Banking.add_bank)
async def continue_add_bank(msg: Message, state: FSMContext):
    """confirm the bank name"""
    bank_name = str(msg.text)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes 👍", callback_data="add_bank_yes"),
                InlineKeyboardButton(text="NO 👎", callback_data="add_bank_no"),
            ],
            [InlineKeyboardButton(text="Abort ❌", callback_data="add_bank_abort")],
        ]
    )
    await msg.reply(
        f"Do you want to add <b>{bank_name}</b> to the database?",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await state.update_data(bank_name=bank_name)
    await state.set_state(Banking.add_bank_confirmation)


@dp.callback_query(Banking.add_bank_confirmation)
async def continue_add_bank(call: types.CallbackQuery, state: FSMContext):
    """add a bank name if user says yes or ignore it if user say no/abort"""
    await call.message.delete()
    if call.data == "add_bank_abort":
        await call.answer(f"❌ Adding Bank Aborted ❌")
        await main_banking(call)
        return

    if call.data == "add_bank_no":
        await call.answer(f"❌ Adding Bank Canceled ❌")
        await main_banking(call)
        return

    if call.data == "add_bank_yes":
        data = await state.get_data()
        bank_name = data.get("bank_name")

        if bnk.add_bank(bank_name=bank_name.lower()):
            await call.answer(f"✅ {bank_name} was added to database ✅")
            await main_banking(call)
        else:
            await call.answer(f"❌Inserting {bank_name} to database was unsuccessful❌")
            await main_banking(call)


# $ ---------------- END | ADD BANK ---------------
# ? ---------------- START | ADD EXPENSE ---------------
@dp.callback_query(F.data == "add_an_expense")
async def add_a_expense(call: types.CallbackQuery, state: FSMContext):
    """Asking the user to send a expense name"""

    await call.answer()
    if not is_admin(call.from_user.id):
        return
    await call.message.answer("Now Send me expense name that you want to add ")
    await state.set_state(Banking.add_expense)


@dp.message(Banking.add_expense)
async def add_a_expense(msg: Message, state: FSMContext):
    """determine if the expense if a child or parent expense"""

    await state.update_data(expense_name=msg.text)

    builder = InlineKeyboardBuilder()

    builder.button(text="👨 Parent", callback_data="parent_expense")
    builder.button(text="👶 Child", callback_data="child_expense")
    builder.button(text="❌ Abort", callback_data="abort_expense")
    builder.adjust(2)
    keyboard = builder.as_markup()

    await msg.reply(
        f"""Do you want to add the <b>{msg.text}</b> as an parent task or a child task?\n
<b>NOTE:</b> For Example Smoking can be a PARENT task and buying cigarette ot Tobacco can be a CHILD  expense\n
The Parent/Chile relation comes back at YOUR PERSPECTIVE of the subject.""",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await state.set_state(Banking.add_expense_2)


@dp.callback_query(Banking.add_expense_2)
async def add_a_expense_2(call: types.CallbackQuery, state: FSMContext):
    """Redirect to different parts based on being child or parent."""

    await call.message.delete()

    which = call.data.split("_expense")[0]

    if which == "abort":
        await call.answer("❌ Aborting Adding Expense... ❌")
        try:
            await call.message.delete()
            await state.clear()
        except:
            pass

        await main_banking(call)
        return

    if which == "parent":
        await state.update_data(parent_expense=None)
        data = await state.get_data()

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Yes 👍", callback_data="confirm_expense_yes"
                    ),
                    InlineKeyboardButton(
                        text="NO 👎", callback_data="confirm_expense_no"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Abort ❌", callback_data="confirm_expense_abort"
                    )
                ],
            ]
        )

        await call.message.answer(
            f"Do you want to add <b>{data.get("expense_name")}</b> as a <b>Parent?</b>",
            parse_mode="HTML",
            reply_markup=keyboard,
        )
        await state.set_state(Banking.confirmation_expense)

    elif which == "child":

        parent_expenses = bnk._get_all_parent_expenses()
        if parent_expenses:

            builder = InlineKeyboardBuilder()
            for tsk in parent_expenses:
                builder.button(text=tsk, callback_data=f"parent_expense_{tsk}")
            builder.adjust(2)
            keyboard = builder.as_markup()

            await call.message.answer(
                f"Choose the Parent Expense: ", reply_markup=keyboard
            )
            await state.set_state(Banking.child_expense)
        else:
            await call.answer(f"❌First Add Some PARENT expense.❌", show_alert=True)
            return
    else:
        await call.answer("❌ Canceling Adding Expense... ❌")
        await call.message.delete()
        await main_banking(call)


@dp.callback_query(Banking.child_expense)
async def choose_child_expense(call: types.CallbackQuery, state: FSMContext):
    """Get teh confirmation to add the child with its parent to the DB."""

    call.answer()
    await call.message.delete()

    parent_answer = call.data.split("parent_expense_")[1]
    await state.update_data(parent_expense=parent_answer)
    data = await state.get_data()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes 👍", callback_data="confirm_expense_yes"
                ),
                InlineKeyboardButton(text="NO 👎", callback_data="confirm_expense_no"),
            ],
            [
                InlineKeyboardButton(
                    text="Abort ❌", callback_data="confirm_expense_abort"
                )
            ],
        ]
    )

    await call.message.answer(
        f"Do you want to add <b>{data.get("expense_name")}</b> as a child for <b>{parent_answer}</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await state.set_state(Banking.confirmation_expense)


@dp.callback_query(Banking.confirmation_expense)
async def confirm_the_expense(call: types.CallbackQuery, state: FSMContext):
    """By using CBanker.add_expense add the expense to the 'bankexpensetype' TABLE."""

    data = await state.get_data()

    _answer = call.data.split("confirm_expense_")[1]

    if _answer == "no":

        await call.answer("❌ Cancelling ... ❌")
        await call.message.delete()
        await main_banking(call)
        await state.clear()
        return

    elif _answer == "abort":
        await call.answer("❌ ABORTING ... ❌")
        await call.message.delete()
        await main_banking(call)
        await state.clear()
        return

    expense_name = data.get("expense_name")
    parent = data.get("parent_expense")

    try:
        if bnk.add_expense(expense_name=expense_name, ref_to=parent):
            await call.answer(
                f"✅Added {expense_name} as {"parent" if parent is None else f"child of {parent}"}✅"
            )

        else:
            await call.answer(
                f"❌Failed to Add {expense_name} as {"parent" if parent is None else f"child of {parent}"}❌"
            )

        await call.message.delete()
        await main_banking(call)
        await state.clear()
        return
    except Exception:
        logger.exception("An Exception in confirm_the_expense in telegram.py")
        await call.message.answer(
            "❌ An UnExpected Error Happened, Please Check Log Files or Try Again Later.❌"
        )
        await state.clear()


# ? ---------------- END | ADD EXPENSE ---------------
# ~ ---------------- START | ADD TRANSACTION ---------------
@dp.callback_query(lambda x: x.data == "make_transaction")
async def make_transaction(call: types.CallbackQuery, state: FSMContext):
    """Asks the user for his desire bank"""

    await call.answer()

    _ = bnk.show_all_banks()
    builder = InlineKeyboardBuilder()
    for i in _:
        builder.button(text=i, callback_data=f"transaction_bank_{i}")
    builder.adjust(3)
    keyboard = builder.as_markup()

    await call.message.answer(
        text="Please Choose The Desired Bank:", reply_markup=keyboard
    )
    await state.set_state(Banking.making_transaction)


@dp.callback_query(Banking.making_transaction)
async def make_transaction_1(call: types.CallbackQuery, state: FSMContext):
    """Asks user to send an amount"""
    await call.message.delete()

    bank = call.data.split("transaction_bank_")[1]

    await call.answer(text=f"✅ {bank}")
    await state.update_data(user_bank=bank)

    await call.message.answer(
        text="Now send me a <b>AMOUNT</b> of your purchase", parse_mode="HTML"
    )
    await state.set_state(Banking.making_transaction_1)


@dp.message(Banking.making_transaction_1)
async def make_transaction_1(msg: Message, state: FSMContext):
    """Adds AMount to state and asks for main Task."""
    try:
        amount = float(msg.text)
    except:
        await msg.reply(
            text="❌Please Enter a valid <b>NUMBER</b>❌", parse_mode="HTML"
        )
        await state.clear()
        return

    await state.update_data(user_amount=amount)
    main_exp = bnk._get_all_parent_expenses()

    if main_exp:

        builder = InlineKeyboardBuilder()
        for i in main_exp:
            builder.button(text=i, callback_data=f"transaction_expense_{i}")
        builder.adjust(2)

        keyboard = builder.as_markup()
        await msg.answer(
            "Choose The Main Expense To Fetch its Sub-Expense: ", reply_markup=keyboard
        )

        await state.set_state(Banking.making_transaction_2)
    else:
        await msg.answer("<b>You dont have any main tasks, try adding one.</b>")


@dp.callback_query(Banking.making_transaction_2)
async def make_transaction_2(call: types.CallbackQuery, state: FSMContext):
    """bring parent expense child expenses"""

    parent = call.data.split("transaction_expense_")[1]

    await call.answer(f"✅ {parent}")
    await call.message.delete()

    children = bnk._get_all_child_expenses(parent_name=parent)

    if children:

        builder = InlineKeyboardBuilder()
        for i in children:
            builder.button(text=i, callback_data=f"transaction_expense_ch_{i}")
        builder.adjust(2)

        keyboard = builder.as_markup()

        await call.message.answer(
            text="Now Select You'r <b>Sub</b>-Expense: ",
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        await state.set_state(Banking.making_transaction_3)
    else:
        await call.message.answer(
            text=f"<b>{parent} Has No Sub-expense;</b> Try add one", parse_mode="HTML"
        )
        await main_banking(call)
        await state.clear()


@dp.callback_query(Banking.making_transaction_3)
async def make_transaction_3(call: types.CallbackQuery, state: FSMContext):
    """Adds user Expense to the state and asks for description."""
    expense = call.data.split("transaction_expense_ch_")[1]

    await call.answer(f"✅ {expense}")

    await state.update_data(user_expense=expense)

    await call.message.answer(
        f"🗞 Now Send me a DESCRIPTION of you'r work.\n\n<b>Send -1 to leave it empty.</b>",
        parse_mode="HTML",
    )

    await state.set_state(Banking.making_transaction_4)


@dp.message(Banking.making_transaction_4)
async def make_transaction_4(msg: Message, state: FSMContext):
    """CONFIRMATION"""

    data = await state.get_data()
    desc = msg.text

    try:
        if int(desc) == -1:
            desc = None

    except ValueError:
        pass

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes", callback_data="confirm_transaction_yes"
                ),
                InlineKeyboardButton(text="No", callback_data="confirm_transaction_no"),
            ],
            [
                InlineKeyboardButton(
                    text="Abort", callback_data="confirm_transaction_abort"
                ),
            ],
        ]
    )
    await state.update_data(user_description=desc)
    await msg.reply(
        text=f"Adding :\n<b>BANK : </b>{data.get("user_bank")}\n<b>AMOUNT : </b>{data.get("user_amount")}\n<b>EXPENSE : </b>{data.get("user_expense")}\n<b>DESCRIPTION : </b>{desc}\n",
        parse_mode="HTML",
        reply_markup=keyboard,
    )

    await state.set_state(Banking.making_transaction_4)


@dp.callback_query(Banking.making_transaction_4)
async def make_transaction_4(call: types.CallbackQuery, state: FSMContext):
    """ADDING TO THE DB"""
    conf = call.data.split("confirm_transaction_")[1]

    if conf == "abort":
        await call.answer("❌ ABORTING ...❌")
        await state.clear()
        await main_banking(call)
        return

    elif conf == "no":
        await call.answer("❌ Canceling ...❌")
        await state.clear()
        await main_banking(call)
        return

    data = await state.get_data()

    answer = bnk.make_transaction(
        bank_name=data.get("user_bank"),
        amount=data.get("user_amount"),
        expense_type=data.get("user_expense"),
        description=data.get("user_description"),
    )

    if answer:
        await call.answer("✅ TRANSACTION ADDED ✅")
        await state.clear()
        await main_banking(call)
        return

    await call.answer("❌ TRANSACTION FAILED ❌", show_alert=True)
    await state.clear()
    await main_banking(call)
    return


# ~ ---------------- END | END TRANSACTION ---------------
# * ---------------- START | SHOW EXPENSES ---------------
@dp.callback_query(lambda x: x.data == "show_expenses")
async def show_expenses(call: types.CallbackQuery):
    """Ask user to select between showing all of the parent in 'bankexpensetype' or children."""
    await call.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="All main Expenses ", callback_data="show_expenses__parent"
                ),
                InlineKeyboardButton(
                    text="Certain Sub Expenses", callback_data="show_expenses__child"
                ),
            ]
        ]
    )

    await call.message.answer(text="Select :", reply_markup=keyboard)


@dp.callback_query(lambda x: x.data == "show_expenses__parent")
async def show_expenses_1(call: types.CallbackQuery):
    """Shows all of the parents in 'bankexpensetype'"""

    await call.answer()
    await call.message.delete()

    try:
        main_exp = bnk._get_all_parent_expenses()
        if main_exp:
            text = "<b>All Main Expenses:</b>\n\n" + "\n".join(
                [f"{i}. {j}" for i, j in enumerate(main_exp, start=1)]
            )

            await call.message.answer(text=text, parse_mode="HTML")
        else:
            await call.message.answer(
                "<b>You dont have any main tasks, try adding one.</b>"
            )
    except:
        logger.exception("An exception in show_expenses in telegram.py")
        await call.message.answer(
            text="An Error Occurred; Check Log Files Or Try Later.", parse_mode="HTML"
        )


@dp.callback_query(lambda x: x.data == "show_expenses__child")
async def show_expenses_2(call: types.CallbackQuery, state: FSMContext):
    """Shows a keyboard containing all of the main task for the user to select"""
    await call.answer()
    await call.message.delete()

    main_exp = bnk._get_all_parent_expenses()

    if main_exp:

        builder = InlineKeyboardBuilder()
        for i in main_exp:
            builder.button(text=i, callback_data=f"child_expense__{i}")
        builder.adjust(2)

        keyboard = builder.as_markup()
        await call.message.answer(
            "Choose The Main Task To Fetch its Sub-Tasks: ", reply_markup=keyboard
        )
        await state.set_state(Banking.fetch_child_expense)
    else:
        await call.message.answer(
            "<b>You dont have any main tasks, try adding one.</b>"
        )


@dp.callback_query(Banking.fetch_child_expense)
async def show_expenses_3(call: types.CallbackQuery, state: FSMContext):
    """Sends user the parents child expenses"""

    parent = call.data.split("child_expense__")[1]
    await call.answer(f"✅ {parent}")
    await call.message.delete()
    children = bnk._get_all_child_expenses(parent_name=parent)

    if children:

        text = f"<b>{parent} children:\n\n</b>" + "\n".join(
            [f"{i}. {j}" for i, j in enumerate(children, start=1)]
        )

        await call.message.answer(text=text, parse_mode="HTML")
        await main_banking(call)
    else:
        await call.message.answer(
            text=f"<b>{parent} Has No Sub-expense;</b> Try add one", parse_mode="HTML"
        )
        await main_banking(call)
        await state.clear()


# * ---------------- END | SHOW EXPENSES ---------------
# () ---------------- START | SHOW BANKS  ---------------
@dp.callback_query(lambda x: x.data == "show_banks")
async def show_banks(call: types.CallbackQuery):
    await call.answer()

    _ = bnk.show_all_banks()

    text = "<b>All Added Banks:</b>\n\n"

    text += "\n".join([f"{i}. {j}" for i, j in enumerate(_, start=1)])

    await call.message.answer(text=text, parse_mode="HTML")


# () ---------------- END | SHOW BANKS  ---------------
# () ---------------- START | BANKING RECORDS  ---------------
@dp.callback_query(lambda x: x.data == "banking_records")
async def banking_records(call: types.CallbackQuery, state: FSMContext):
    """Prompt user to fetch the Bank Name."""

    await call.answer()

    builder = InlineKeyboardBuilder()
    for i in bnk.show_all_banks():
        builder.button(text=i, callback_data=f"bank_record_{i}")
    builder.adjust(3)
    keyboard = builder.as_markup()

    await call.message.answer(
        text="With this method you can Get your Banking Spent, between two dates for your desired BANK, Now First Select your desired <b>BANK</b>:",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await state.set_state(Banking.fetch_record)


@dp.callback_query(Banking.fetch_record)
async def banking_records__2(call: types.CallbackQuery, state: FSMContext):
    """Fetching bank name and then ask for a start date."""

    bank_name = call.data.split("bank_record_")[1]
    await call.answer(f"✅ {bank_name}")
    try:
        await call.message.delete()
    except:
        pass

    await state.update_data(user_bank_rec=bank_name)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="From First Initial", callback_data="bank_record_start"
                )
            ]
        ]
    )
    await call.message.answer(
        text="Now please Send Me an start date in <b>YEAR-MONTH-DAY</b> format:",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await state.set_state(Banking.fetch_record_1)


@dp.message(Banking.fetch_record_1)
async def banking_records_1(msg: Message, state: FSMContext):
    """Fetches the start date in text from user, and prompt a yes/no question to go into callback_queries"""

    try:
        dt.datetime.strptime(msg.text, "%Y-%m-%d")
    except:  # Value Error
        msg.reply(
            "❌ Please Send a Valid Date in <b>YEAR-MONTH-DAY</b> format ❌",
            parse_mode="HTML",
        )
        return

    await state.update_data(user_start_date=msg.text)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes", callback_data="Banking_fetch_record_1_yes"
                ),
                InlineKeyboardButton(
                    text="No", callback_data="Banking_fetch_record_1_no"
                ),
            ]
        ]
    )

    await msg.reply(
        text=f"Do You Want to use <b>{msg.text}</b> as your start date?",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await state.set_state(Banking.fetch_record_2)


@dp.callback_query(Banking.fetch_record_2)
async def banking_records_2(call: types.CallbackQuery, state: FSMContext, flag=True):
    """Asking the end date"""

    # ! Made this flag because in banking_records_2_1 I am about to call this function but if it want to split it it cause error and I dont want to use try-except
    if flag:
        _answer = call.data.split("Banking_fetch_record_1_")[1]

        if _answer == "no":  # Stop it here...
            await call.answer(text="❌ Cancelling...")
            await state.clear()
            await main_banking(call)
            return
    await call.answer(text="✅")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Today", callback_data="bank_record_end")]
        ]
    )
    await call.message.answer(
        text="Now please Send Me an end date in <b>YEAR-MONTH-DAY</b> format:",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await state.set_state(Banking.fetch_record_3)


@dp.message(Banking.fetch_record_3)
async def banking_records_3(msg: Message, state: FSMContext):

    try:
        dt.datetime.strptime(msg.text, "%Y-%m-%d")
    except:  # Value Error
        msg.reply(
            "❌ Please Send a Valid Date in <b>YEAR-MONTH-DAY</b> format ❌",
            parse_mode="HTML",
        )
        return

    await state.update_data(user_end_date=msg.text)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes", callback_data="Banking_fetch_record_3_yes"
                ),
                InlineKeyboardButton(
                    text="No", callback_data="Banking_fetch_record_3_no"
                ),
            ]
        ]
    )

    await msg.reply(
        text=f"Do You Want to use <b>{msg.text}</b> as your end date?",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await state.set_state(Banking.fetch_record_4)


@dp.callback_query(Banking.fetch_record_4)
async def banking_records_4(call: types.CallbackQuery, state: FSMContext):
    """Making excel file and give it back."""

    _answer = call.data.split("Banking_fetch_record_3_")[1]

    if _answer == "no":  # Stop it here...
        await call.answer(text="❌ Cancelling...")
        await state.clear()
        await main_banking(call)
        return

    await call.answer(text="✅ Please Wait....")

    data = await state.get_data()

    await banking_record_make_excel(
        call=call,
        start_date=data.get("user_start_date"),
        end_date=data.get("user_end_date"),
        bank_name=data.get("user_bank_rec"),
    )
    await state.clear()
    await main_banking(call)
    return


@dp.callback_query(lambda x: x.data == "bank_record_start")
async def banking_records_2_1(call: types.CallbackQuery, state: FSMContext):
    """uses the bank first init as its start time"""

    await call.answer("✅")

    try:
        await call.message.delete()
    except:
        pass
    data = await state.get_data()

    start_ = bnk.bank_first_init_time(bank_name=data.get("user_bank_rec")).strftime(
        "%Y-%m-%d"
    )

    await state.update_data(user_start_date=start_)

    await banking_records_2(call, state, flag=False)


@dp.callback_query(lambda x: x.data == "bank_record_end")
async def banking_records_3_1(call: types.CallbackQuery, state: FSMContext):
    """uses the current time as the end time"""

    data = await state.get_data()

    await call.answer(text="✅ Please Wait....")

    try:
        await call.message.delete()
    except:
        pass

    await banking_record_make_excel(
        call=call,
        start_date=data.get("user_start_date"),
        end_date=dt.datetime.now().strftime("%Y-%m-%d"),
        bank_name=data.get("user_bank_rec"),
    )
    await state.clear()
    await main_banking(call)
    return


async def banking_record_make_excel(
    call: types.CallbackQuery, start_date, end_date, bank_name
):
    bnk.fetch_records(start_date=start_date, end_date=end_date, bank_name=bank_name)
    path = os.path.join("Banking_records", sorted(os.listdir("Banking_records"))[-1])
    await call.message.answer_document(document=types.FSInputFile(path))


# () ---------------- END | BANKING RECORDS ---------------
#! ------------------------------- END | BANK MANAGER SECTION -------------------------------------


#! ------------------------------- START | CHARTING SECTION -------------------------------------
class ChartingSection(StatesGroup):
    task_1 = State()
    task_2 = State()
    bank_1 = State()


@dp.callback_query(lambda x: x.data == "charting")
async def charting(call: types.CallbackQuery):
    """Prompt CHarting Keyboard"""

    await call.answer()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Banking Section", callback_data="banking_chart"
                ),
                InlineKeyboardButton(
                    text="Tasks Section", callback_data="task_charting"
                ),
            ],
            [InlineKeyboardButton(text="⬅️ Return", callback_data="/panel")],
        ]
    )

    await call.message.answer(text="What do you want to chart?", reply_markup=keyboard)


# ~ ------- CHART THE BANK -----
@dp.callback_query(lambda x: x.data == "banking_chart")
async def charting_b(call: types.CallbackQuery, state: FSMContext):
    await call.answer("✅")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Last Month", callback_data="charting_bank_default"
                )
            ]
        ]
    )

    await call.message.answer(
        f"Now send me the <b>number of days</b> you want to look at you bank details?(eg. 10)",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await state.set_state(ChartingSection.bank_1)


@dp.message(ChartingSection.bank_1)
async def charting_b_1(msg: Message):
    try:
        days = int(msg.text)
    except:
        await msg.reply(f"Please provide a number <b>{msg.text}</b> is not an number!")

        return

    if not bnk.chart_it(last_x_days=days):
        await msg.reply(f"There was an error in charting! Try Again ...")
        return

    try:
        charts_path = [
            InputMediaPhoto(media=FSInputFile(os.path.join("figures", filename)))
            for filename in os.listdir("figures")
            if filename.startswith("bank")
        ]
        await bot.send_media_group(
            chat_id=msg.chat.id, media=charts_path, reply_to_message_id=msg.message_id
        )
    except:
        logger.exception(
            "An error in telegram charting_b_1 in sending files to telegram."
        )
        await msg.reply(f"There was an error in sending figures! Read Logs ...")
        return


@dp.callback_query(ChartingSection.bank_1)
async def charting_b_2(call: types.CallbackQuery, state: FSMContext):
    days = 30
    await call.answer("✅")
    if not bnk.chart_it(last_x_days=days):
        await call.message.reply(f"There was an error in charting! Try Again ...")
        return

    try:
        charts_path = [
            InputMediaPhoto(media=FSInputFile(os.path.join("figures", filename)))
            for filename in os.listdir("figures")
            if filename.startswith("bank")
        ]
        await bot.send_media_group(
            chat_id=call.message.chat.id,
            media=charts_path,
            reply_to_message_id=call.message.message_id,
        )
        await state.clear()
    except:
        logger.exception(
            "An error in telegram charting_b_2 in sending files to telegram."
        )
        await call.message.reply(
            f"There was an error in sending figures! Read Logs ..."
        )
        await state.clear()
        return


# ~ ------- CHART THE TASKS -----
@dp.callback_query(lambda x: x.data == "task_charting")
async def charting_t(call: types.CallbackQuery, state: FSMContext):

    await call.answer(text="✅ Tasks")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Current Week", callback_data="chart_task_current_week"
                )
            ]
        ]
    )
    await call.message.answer(
        text="What week you want to chart?\nNOTE: If you want to chart the 17th <b>WEEK</b> of <b>YEAR</b>  2025 you should enter <b>y2025w17</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await state.set_state(ChartingSection.task_1)


@dp.message(ChartingSection.task_1)
async def charting_t_1(msg: Message, state: FSMContext):

    week = msg.text

    try:
        [int(i) for i in week.split("y")[1].split("w")]
    except ValueError:
        await msg.reply(f"Invalid format : {week} \nCORRECT format ==> <b>y2025w17</b>")
        return

    await state.update_data(task_chart_week=week)

    builder = InlineKeyboardBuilder()
    for day in [
        "Saturday",
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    ]:
        builder.button(text=day, callback_data=f"charting_start_{day.lower()}")

    builder.adjust(3)
    keyboard = builder.as_markup()

    await msg.reply(
        "Now select the first day of a week for charting:", reply_markup=keyboard
    )

    await state.set_state(ChartingSection.task_2)


@dp.callback_query(ChartingSection.task_1)
async def charting_t_2(call: types.CallbackQuery, state: FSMContext):
    await call.answer(f"✅ {lm.current_week_name}")
    await state.update_data(task_chart_week=lm.current_week_name)

    builder = InlineKeyboardBuilder()
    for day in [
        "Saturday",
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    ]:
        builder.button(text=day, callback_data=f"charting_start_{day}")

    builder.adjust(3)
    keyboard = builder.as_markup()

    await call.message.reply(
        "Now select the first day of a week for charting:", reply_markup=keyboard
    )

    await state.set_state(ChartingSection.task_2)


@dp.callback_query(ChartingSection.task_2)
async def charting_t_2(call: types.CallbackQuery, state: FSMContext):

    day = call.data.split("charting_start_")[1]

    data = await state.get_data()
    week = data.get("task_chart_week")

    try:

        if not lm.chart_it(week=week, start_day=day):
            await call.answer(
                text=f"❌ week {week} DOESN'T exists. Please add some task to your week",
                show_alert=True,
            )
            await state.clear()
            await charting(call)
            return

        charts_path = [
            InputMediaPhoto(media=FSInputFile(os.path.join("figures", filename)))
            for filename in os.listdir("figures")
            if not filename.startswith("bank")
        ]
        await call.answer(text="✅")
        await bot.send_media_group(chat_id=call.message.chat.id, media=charts_path)
        await state.clear()
        await charting(call)
        return

    except:
        await call.answer(text="❌An Error Occurred.")
        await state.clear()
        await charting(call)
        return


#! ------------------------------- END | CHARTING SECTION -------------------------------------
async def main() -> None:

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
