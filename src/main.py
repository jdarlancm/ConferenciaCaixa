import prompt as p

from dotenv import load_dotenv
from monthly_conference import MonthlyConference
from filesystem.manager import Manager
from filesystem.generator import Generator
from filesystem.standardizer import Standardizer

load_dotenv()

if __name__ == "__main__":
    option = p.main_menu()
    cashier = p.cashier()
    year = p.year()

    if option == p.Options.STANDARD_CASH_FOLDER.value:
        standardizer = Standardizer("Conferir", cashier, year)
        standardizer.normatize()
    else:
        month = p.month()

        if option == p.Options.CREATE_CASH_FOLDER.value:
            manager = Manager("Conferir", cashier, year, month)
            generator = Generator(manager)
            generator.generate()
        elif option == p.Options.CHECK_CASH_REGISTER.value:
            MonthlyConference(cashier, year, month).check()
