import os

from filesystem.manager import Manager


class Generator:
    def __init__(self, filesystem_manager: Manager):
        self.filesystem_manager = filesystem_manager

    def generate(self):
        self._validate_exists_dirs()
        self._create_month_dir()
        self._create_days_dir()

    def _validate_exists_dirs(self):
        if not os.path.isdir(self.filesystem_manager.get_year_path()):
            raise FileNotFoundError(
                f"O diretorio para o ano referência não existe: {self.filesystem_manager.year}"
            )

        self._validate_exists_month_dir()

    def _validate_exists_month_dir(self):
        if os.path.isdir(self.filesystem_manager.get_month_path()):
            raise FileExistsError(
                f"Já existe um diretorio para o mês referência: {self.filesystem_manager.month} / {self.filesystem_manager.year}"
            )

        month_exist = [
            m
            for m in self.filesystem_manager.list_months_year()
            if m.startswith(str(self.filesystem_manager.month).zfill(2))
        ]

        if month_exist:
            raise FileExistsError(
                f"Já existe um diretorio simliar ao mês referência, fora do padrão: {month_exist}"
            )

    def _create_month_dir(self):
        os.mkdir(self.filesystem_manager.get_month_path())

    def _create_days_dir(self):
        first_day_month, last_day_month = self.filesystem_manager.get_period_month()
        for day in range(first_day_month.day, last_day_month.day + 1):
            day_path = self.filesystem_manager.get_day_path(str(day).zfill(2))
            os.mkdir(day_path)


"""
Gerar a estrutura de pasta de um determinado ano e mes (se não existir)
1. Verificar se existe a pasta do mês (verificar se existe uma pasta com o numero do mes, mas outro padrao - execption)

"""
