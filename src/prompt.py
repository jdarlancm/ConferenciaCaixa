from enum import Enum


class Options(Enum):
    CREATE_CASH_FOLDER = 1
    STANDARD_CASH_FOLDER = 2
    CHECK_CASH_REGISTER = 3


def main_menu():
    text = "1) Criar pastas dos caixas \n"
    text += "2) Normalizar pastas dos caixas \n"
    text += "3) Verificar caixas \n"
    text += "\nEscolha a opção desejada: "

    option = input(text)
    if not option.isdigit() or int(option) not in [e.value for e in Options]:
        print("Opção indexistente")
        exit()

    return int(option)


def month():
    month_str = input("Digite o mês (1-12): ")
    month = int(month_str) if month_str.isdigit() else 0
    if not 1 <= month <= 12:
        print("Mês inválido. Por favor, digite um número entre 1 e 12.")
        exit()

    return int(month)


def year():
    year_str = input("Digite o ano: ")
    year = int(year_str) if year_str.isdigit() else 0
    if len(year_str) != 4:
        print("Ano inválido.")
        exit()

    return int(year)


def cashier():
    cashier_name = input("Informe o nome do operador: ")
    if not cashier_name:
        print("Operador não informado.")
        exit()

    return cashier_name
