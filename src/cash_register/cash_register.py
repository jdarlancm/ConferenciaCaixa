import os

from cash_register.receipt import Receipt
from cash_register.cash_register_report import CashRegisterReport, REPORT_NAME
from utils import csv_utils

CASH_WITHDRAWAL_FILE = "_retirada_dinheiro.csv"
CARD_INFLOW_FILE = "_recebimento_cartao.csv"
ONLINE_INFLOW_FILE = "_recebimento_online.csv"


class CashRegister:
    def __init__(self, path):
        self.path = path
        self.report = CashRegisterReport(path)
        self.receipts = self._load_receipts()

    def _load_receipts(self):
        return [
            file
            for file in os.listdir(self.path)
            if file.lower().endswith(".pdf") and file != REPORT_NAME
        ]

    def process(self):
        self._process_report()
        self._process_receipts()
        self._save_conference_files()

    def _process_report(self):
        self.cash_withdrawals = self.report.get_cash_withdrawals()
        self.card_inflows = self.report.get_card_inflows()
        self.online_inflows = self.report.get_online_inflows()

    def _process_receipts(self):
        for receipt in self.receipts:
            try:
                self._process_receipt(receipt)
            except (ValueError, FileNotFoundError) as e:
                print(str(e))

    def _process_receipt(self, receipt):
        filename = os.path.join(self.path, receipt)
        receipt_info = Receipt(filename).process()
        transaction_number = receipt_info["transaction_number"]
        if transaction_number:
            self._rename(filename, transaction_number)

            self._update_transactions_status_found(
                transaction_number, (self.online_inflows + self.cash_withdrawals)
            )

            self._update_card_info_found(receipt_info)

    def _rename(self, filename, transaction_number):
        os.rename(
            filename,
            os.path.join(self.path, f"{transaction_number}.pdf"),
        )

    def _update_transactions_status_found(self, transaction_number, transactions):
        for transaction in transactions:
            transaction["receipt_found"] = (
                transaction_number == transaction["transaction_number"]
            )

    def _update_card_info_found(self, receipt_info):
        transaction_number = receipt_info["transaction_number"]
        for transaction in self.card_inflows:
            transaction["receipt_found"] = (
                transaction_number == transaction["transaction_number"]
            )
            transaction["card_id"] = receipt_info["card_id"]
            transaction["card_date"] = receipt_info["card_date"]

    def _save_conference_files(self):
        self._save_conference_file(CASH_WITHDRAWAL_FILE, self.cash_withdrawals)
        self._save_conference_file(ONLINE_INFLOW_FILE, self.online_inflows)
        self._save_conference_file(CARD_INFLOW_FILE, self.card_inflows)

    def _save_conference_file(self, filename, data):
        file_path = os.path.join(self.path, filename)

        if os.path.exists(file_path):
            os.remove(file_path)

        if data:
            csv_utils.save_dict_to_csv(file_path, data)
