import os

from datetime import datetime, timedelta

from utils import date_utils


class Manager:
    def __init__(self, cashier_type_folder, cashier, year, month):
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

    def get_day_path(self, day):
        return os.path.join(self.get_month_path(), day)

    def get_period_month(self):
        first_day_of_month = datetime(self.year, self.month, 1)
        last_day_of_month = (
            datetime(self.year, self.month + 1, 1) - timedelta(days=1)
            if self.month < 12
            else datetime(self.year, 12, 31)
        )

        return first_day_of_month, last_day_of_month

    def list_days(self):
        month_path = self.get_month_path()
        days = [
            day
            for day in os.listdir(month_path)
            if os.path.isdir(os.path.join(month_path, day))
        ]
        return days

    def list_months_year(self):
        year_path = self.get_year_path()
        months = [
            name
            for name in os.listdir(year_path)
            if os.path.isdir(os.path.join(year_path, name))
        ]
        return months
