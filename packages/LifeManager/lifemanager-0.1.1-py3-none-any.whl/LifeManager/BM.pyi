import datetime as dt
from typing import Optional

class CBanker:
    """
    This class handles creation and interaction with banking tables.
    """

    def __init__(self) -> None: ...
    def make_tables(self) -> bool:
        """
        This method creates banks and banker TABLES.

        Returns:
            bool: True if all tables were created or already exist, otherwise False.
        """
        ...

    def __make_banks_table(self) -> bool:
        """
        Internal method to create the banks table.

        Returns:
            bool: True if created or already exists, otherwise False.
        """
        ...

    def __make_banker_table(self) -> bool:
        """
        Internal method to create the banker table and its trigger/function.

        Returns:
            bool: True if created or already exists, otherwise False.
        """
        ...

    def __fetch_bank_id(self, bank_name: str) -> int | bool:
        """
        Fetch bank ID from bank name.

        Args:
            bank_name (str): The bank name.

        Returns:
            int | bool: Returns the bank ID if it exists, otherwise False.
        """
        ...

    def add_bank(self, bank_name: str) -> bool:
        """
        Add a bank name to the banks table.

        Args:
            bank_name (str): The bank name.

        Returns:
            bool: True if added, False otherwise.
        """
        ...

    def make_transaction(
        self,
        bank_name: str,
        amount: float,
        expense_type: str,
        description: str | None = None,
    ) -> bool:
        """
        Make a transaction for a bank.

        Args:
            bank_name (str): The bank name.
            amount (float): The amount of the transaction.
            description (str | None, optional): Optional description.
            expense_type (str) : Type of expense.
        Returns:
            bool: True if transaction succeeded, otherwise False.
        """
        ...

    def __create_bank_expense_type_table(self):
        """
        Makes bankexpensetype(Bank Expense Type) TABLE.
        """
        ...

    def fetch_expense_id(self, expense_name: str) -> int | bool:
        """Fetch the expense id from the bankexpensetype TABLE if its exists.

        Args:
            expense_name (str): Expense name to fetch its id.

        Returns:
            int | bool: Returns the id of said expense name, otherwise False.
        """
        ...

    def add_expense(self, expense_name: str, ref_to=None) -> bool:
        """Adds a expense to bankexpensetype TABLE.
        NOTE: If the ref_to is None, it creates a parent expense.


        Args:
            expense_name (str): The expense name that you want to add.
            ref_to (str, optional): The Parent Expense that you want to add expense_name under it . Defaults to None.

        Returns:
            bool: Returns True if expense, added successfully, otherwise False.
        """
        ...

    def __get_all_parent_expenses(self) -> list:
        """Returns all the parent expense in a list.

        Returns:
            list: list of parent expense.
        """
        ...

    def _get_all_child_expenses(self, parent_name: str) -> list:
        """Gets a parent name and searches for its children in bankexpensetype TABLE.

        Args:
            parent_name (str): you desired parent name

        Returns:
            list: empty list is it cant find the name or the name is child not parent, otherwise a list of children
        """
        ...

    def show_all_banks(self):
        """Show All of the Banks."""
        ...

    def fetch_records(
        self,
        bank_name: str,
        start_date: str,
        end_date: Optional[str] = None,
    ) -> bool:
        """Fetches two dates as *YEAR-MONTH-DAY* format and returns all of the transactions between these two dates in a excel file for desired bank.

        Args:
            bank_name (str): The Bank Name that you want to fetch data for.
            start_date (str): The Starting date in *YEAR-MONTH-DAY* format
            end_date (Optional[str], optional): Ending date in *YEAR-MONTH-DAY* format. Defaults to None; if sets to None, it gets current time.

        Returns:
            bool : True if it makes an excel file for your data, otherwise false.
        """

    def bank_first_init_time(self, bank_name: str) -> bool | dt.datetime:
        """Gives a date of the banks, first initial.

        Args:
            bank_name (str): Your desired bank name.

        Returns:
            bool | dt.datetime: Return first initial date as datetime object, otherwise False.
        """
        ...

    def chart_it(self, last_x_days: int = 30): ...
