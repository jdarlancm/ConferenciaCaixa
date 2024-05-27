import os
import re

from utils import date_utils
from filesystem.manager import Manager

MONTH_PATTERN = re.compile(r"(\d{1,2})[-_\s]*(\w*)", re.IGNORECASE)
DAY_PATTERN = re.compile(r"(\d{1,2})[-_\s]*\d{0,2}", re.IGNORECASE)


class Standardizer:
    def __init__(self, conference_type, cashier, year):
        self.filesytem_manager = Manager(conference_type, cashier, year, None)

    def normatize(self):
        months_path_name = self.filesytem_manager.list_months_year()
        for month_path_name in months_path_name:
            self._normatize_month(month_path_name)

    def _normatize_month(self, month_path_name):
        month_number = self._extract_month_number(month_path_name)
        if month_number:
            self._rename_month_path(month_path_name, month_number)
            self._normatize_days(month_number)

    def _extract_month_number(self, month_path_name):
        month_number = None
        match = MONTH_PATTERN.match(month_path_name)
        if match:
            month_number_str, _ = match.groups()
            month_number = int(month_number_str)

        return month_number

    def _rename_month_path(self, month_path_name, month_number):
        correct_month_path_name = date_utils.get_month_name_br(month_number)
        if month_path_name != correct_month_path_name:
            year_path = self.filesytem_manager.get_year_path()
            self._rename_path(year_path, month_path_name, correct_month_path_name)

    def _normatize_days(self, month_number):
        self.filesytem_manager.month = month_number
        days_path_name = self.filesytem_manager.list_days()
        for day_path_name in days_path_name:
            self._normatize_day(day_path_name)

    def _normatize_day(self, day_path_name):
        correct_day_path_name = self._extract_day(day_path_name)
        if correct_day_path_name and correct_day_path_name != day_path_name:
            month_path = self.filesytem_manager.get_month_path()
            self._rename_path(month_path, day_path_name, correct_day_path_name)

    def _extract_day(self, day_path_name):
        day = None
        match = DAY_PATTERN.match(day_path_name)
        if match:
            day = match.group(1).zfill(2)

        return day

    def _rename_path(self, parent_path, actual_name, old_name):
        actual_path = os.path.join(parent_path, actual_name)
        correct_path = os.path.join(parent_path, old_name)
        os.rename(actual_path, correct_path)


"""
[] mudar toda estrutura que não estiver no padrão
cashier
  yyyy
    01-JANEIRO
      01
      02
      ...
      31
    02-FEVEREIRO
    ...
    12-DEZEMBRO
"""
