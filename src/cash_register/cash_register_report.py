import os
import re

from datetime import datetime
from enum import Enum

from utils import pdf_utils

REPORT_NAME = "Relação de movimentações por abertura de caixa.pdf"

PERIOD_REPORT_PATTERN = re.compile(
    r"Relação de movimentações com data de abertura entre (\d{2}/\d{2}/\d{4}) e (\d{2}/\d{2}/\d{4})"
)
CASH_REGISTER_OPENING_PATTERN = re.compile(
    r"Data de abertura: (\d{2}/\d{2}/\d{4}) \d{2}:\d{2}:\d{2}"
)
MOVEMENT_PATTERN = re.compile(r"Movimentação:\s*(\d+)")
WITHDRAWAL_PATTERN = re.compile(r"\(Retirada\)\s*([\w\s-]+)\s*R\$\s*(-?\d+,\d+)")
INFLOW_PATTERN = re.compile(r"\(Recebimento\)\s*([\w\s-]+)\s*R\$\s*(\d+,\d+)")


class TransactionType(Enum):
    CARD = "cartão"
    ONLINE = "recebimento on-line"
    CASH = "dinheiro"


class CashRegisterReport:
    def __init__(self, path):
        self.report_file = os.path.join(path, REPORT_NAME)
        self.content = self._read()

    def _read(self):
        self._validate()
        return pdf_utils.extract_content_pages_to_str(self.report_file)

    def _validate(self):
        if not os.path.isfile(self.report_file):
            raise FileExistsError("Arquivo de movimentação de caixa não encontrado")

    def get_period(self):
        period_match = PERIOD_REPORT_PATTERN.search(self.content)
        if not period_match:
            raise ValueError(
                "Não foi possível encontrar a data inicial e final no relatório."
            )

        start_date_str, end_date_str = period_match.groups()
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

        return start_date, end_date

    def get_list_days_with_transactions(self):
        transactions_date = set(CASH_REGISTER_OPENING_PATTERN.findall(self.content))
        return sorted({day.split("/")[0] for day in transactions_date})

    def get_cash_withdrawals(self):
        return self.process_transactions(WITHDRAWAL_PATTERN, TransactionType.CASH.value)

    def get_card_inflows(self):
        return self.process_transactions(INFLOW_PATTERN, TransactionType.CARD.value)

    def get_online_inflows(self):
        return self.process_transactions(INFLOW_PATTERN, TransactionType.ONLINE.value)

    def process_transactions(self, pattern, transaction_type):
        transactions = []
        lines = self.content.split("\n")
        current_transaction_number = None

        for line in lines:
            current_transaction_number = self._update_transaction_number(
                current_transaction_number, line
            )

            transaction = self._extract_transaction(
                current_transaction_number, pattern, transaction_type, line
            )

            if transaction:
                transactions.append(transaction)

        return transactions

    def _update_transaction_number(self, current_number, line):
        new_transaction_match = MOVEMENT_PATTERN.match(line)
        if new_transaction_match:
            return new_transaction_match.group(1).strip()

        return current_number

    def _extract_transaction(self, transaction_number, pattern, transaction_type, line):
        match = pattern.match(line)
        if match:
            type_inflow, amount_str = match.groups()
            if type_inflow.strip().lower() == transaction_type:
                amount = self._convert_amount_to_float(amount_str)
                return {
                    "transaction_number": transaction_number,
                    "transaction_type": transaction_type,
                    "transaction_amount": amount,
                    "receipt_found": False,
                }

        return None

    def _convert_amount_to_float(self, amount_str):
        try:
            amount = float(amount_str.replace(",", "."))
            return -amount if amount < 0 else amount
        except ValueError:
            return 0.0

    @staticmethod
    def is_report_exist(path):
        return os.path.isfile(os.path.join(path, REPORT_NAME))
