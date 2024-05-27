import os

from utils import date_utils


class CashierFolderNavigator:
    def __init__(self, cashier_type_folder, cashier=None, year=None, month=None):
        self.base_path = os.getenv("BASE_FOLDER")
        self.cashier_type_folder = cashier_type_folder
        self.cashier = cashier
        self.year = year
        self.month = month

    def get_cashiers_path(self):
        return os.path.join(self.base_path, self.cashier_type_folder)

    def get_cashier_path(self):
        return (
            os.path.join(self.get_cashiers_path(), self.cashier) if self.cashier else ""
        )

    def get_year_path(self):
        return (
            os.path.join(self.get_cashier_path(), str(self.year)) if self.year else ""
        )

    def get_month_path(self):
        month_name = date_utils.get_month_name_br(self.month)
        return os.path.join(self.get_year_path(), month_name) if self.month else ""

    def is_exist_month_path(self):
        return os.path.exists(self.get_month_path())

    def list_operators(self):
        operators = [
            operator
            for operator in os.listdir(self.get_cashiers_path())
            if os.path.isdir(self.get_operator_path(operator))
        ]
        return operators

    def list_years(self, operator):
        operator_path = self.get_operator_path(operator)
        years = [
            year
            for year in os.listdir(operator_path)
            if os.path.isdir(os.path.join(operator_path, year))
        ]
        return years

    def list_months(self, operator, year):
        year_path = os.path.join(self.get_cashiers_path(), operator, year)
        months = [
            month
            for month in os.listdir(year_path)
            if os.path.isdir(os.path.join(year_path, month))
        ]
        return months

    def list_days(self, operator, year, month):
        month_path = os.path.join(self.get_cashiers_path(), operator, year, month)
        days = [
            day
            for day in os.listdir(month_path)
            if os.path.isdir(os.path.join(month_path, day))
        ]
        return days

    def check_if_day_has_box(self, operator, year, month, day):
        day_path = os.path.join(self.get_cashiers_path(), operator, year, month, day)
        return os.path.exists(day_path)

    def list_files(self, day):
        day_path = os.path.join(self.get_month_path(), str(day))

        if not os.path.exists(day_path):
            return []

        files = [
            os.path.join(day_path, file)
            for file in os.listdir(day_path)
            if os.path.isfile(os.path.join(day_path, file))
        ]
        return files

    def list_files_name(self, day):
        day_path = os.path.join(self.get_month_path(), str(day))

        if not os.path.exists(day_path):
            return []

        files = [
            file
            for file in os.listdir(day_path)
            if os.path.isfile(os.path.join(day_path, file))
        ]
        return files
