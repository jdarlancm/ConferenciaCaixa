import os

from cash_register import CashRegister, CashRegisterReport
from filesystem import Manager
from utils import csv_utils

CONFERENCE_DIR = "Conferir"
MISSING_CASH_REGISTER_FILE = "_dias_faltando_arquivo.csv"
MISSING_REPORT_FILE = "_dias_faltando_relatorio.csv"


class MonthlyConference:
    def __init__(self, cashier, year, month):
        self.filesytem_manager = Manager(CONFERENCE_DIR, cashier, year, month)
        self.days_cash_register = self._get_days_cash_register()

    def _get_days_cash_register(self):
        days_in_dir = self.filesytem_manager.list_days()
        days_with_report = [
            day
            for day in days_in_dir
            if CashRegisterReport.is_report_exist(
                self.filesytem_manager.get_day_path(day)
            )
        ]
        return sorted(days_with_report)

    def check(self):
        self._validate_period()
        self._check_cash_registers()

    def _validate_period(self):
        month_path = self.filesytem_manager.get_month_path()
        report = CashRegisterReport(month_path)

        self._validate_report_period(report)
        self._compare_report_and_cash_register_days(report)

    def _validate_report_period(self, report):
        start_date_report, end_date_report = report.get_period()
        first_day_month, last_day_month = self.filesytem_manager.get_period_month()

        if start_date_report != first_day_month or end_date_report != last_day_month:
            raise Warning(
                f"O relatório de conferência não abrange todo o período mês {self.month}."
            )

    def _compare_report_and_cash_register_days(self, report):
        days_transactions_report = set(report.get_list_days_with_transactions())
        days_cash_register = set(self.days_cash_register)
        days_missing_cash_register = days_transactions_report - days_cash_register
        days_missing_report = days_cash_register - days_transactions_report

        self._save_conference_file(
            MISSING_CASH_REGISTER_FILE, days_missing_cash_register
        )
        self._save_conference_file(MISSING_REPORT_FILE, days_missing_report)

    def _save_conference_file(self, filename, data):
        if data:
            file_path = os.path.join(self.filesytem_manager.get_month_path(), filename)
            header = ["Dia"]
            csv_utils.save_to_csv(file_path, data, header)

    def _check_cash_registers(self):
        for day in self.days_cash_register:
            self._check_cahs_register(day)

    def _check_cahs_register(self, day):
        print(f"Processing day {day}")
        day_path = self.filesytem_manager.get_day_path(day)
        CashRegister(day_path).process()
