import os
import re

from utils import pdf_utils

RECEIPT_IDENTIFIER = "COMPROVANTE DE CAIXA"

TRANSACTION_NUMBER_PATTERN = re.compile(r"Movimentac[aã]o:\s*(\d+)")
CARD_TRANSACTION_PATTERN = re.compile(r"Recebimento Cartao (\d+,\d{2})")
CARD_ID_PATTERN = re.compile(
    r"Stone\s*ID:\s*(\d+)|Stone\s*(10:)\s*(\d+)|Stone\s*1D:\s*(\d+)|STONE\s*ID:\s*(\d+)|sone\s*10:\s*(\d+)"
)
MERCHANT_COPY_PATTERN = re.compile(r"VIA\s?LOJISTA", re.IGNORECASE)
DATE_PATTERN = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")


class Receipt:
    def __init__(self, filepath):
        self._check_exist(filepath)
        self.content = pdf_utils.ocr_extract_content_to_str(filepath)

    def _check_exist(self, filepath):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(
                f"Arquivo do comprovante não encontrado: {filepath}"
            )

    def process(self):
        self._validate_receipt_file()
        return self._get_receipt_info()

    def _validate_receipt_file(self):
        if RECEIPT_IDENTIFIER not in self.content:
            raise ValueError("O arquivo não é um comprovante de caixa")

    def _get_receipt_info(self):
        receipt_info = {
            "transaction_number": self._get_transaction_number(),
            "transaction_amount": self._get_card_transaction_amount(),
            "card_id": None,
            "card_date": None,
        }

        if receipt_info["transaction_amount"]:
            receipt_info["card_id"] = self._get_card_id()
            receipt_info["card_date"] = self._get_card_date()

        return receipt_info

    def _get_transaction_number(self):
        return self._matcher(TRANSACTION_NUMBER_PATTERN, 1)

    def _get_card_transaction_amount(self):
        return self._matcher(CARD_TRANSACTION_PATTERN, 1)

    def _matcher(self, pattern, group):
        match = pattern.search(self.content)
        return match.group(group).strip() if match else None

    def _get_card_id(self):
        card_id_match = CARD_ID_PATTERN.search(self.content)
        if card_id_match:
            return next(
                group
                for group in card_id_match.groups()
                if group is not None and group.isdigit()
            )

        return None

    def _get_card_date(self):
        keyword_matches = list(MERCHANT_COPY_PATTERN.finditer(self.content))

        for match in keyword_matches:
            start_pos = match.end()

            # Captura os próximos 10 linhas
            next_lines = self.content[start_pos:].splitlines()[:10]

            for line in next_lines:
                date_match = DATE_PATTERN.search(line)
                if date_match:
                    return date_match.group(0)

        return None
