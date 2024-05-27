import pytest

from utils.date_utils import get_month_name_br


@pytest.mark.parametrize(
    "month, expected",
    [
        (1, "01-JANEIRO"),
        (2, "02-FEVEREIRO"),
        (3, "03-MARÇO"),
        (4, "04-ABRIL"),
        (5, "05-MAIO"),
        (6, "06-JUNHO"),
        (7, "07-JULHO"),
        (8, "08-AGOSTO"),
        (9, "09-SETEMBRO"),
        (10, "10-OUTUBRO"),
        (11, "11-NOVEMBRO"),
        (12, "12-DEZEMBRO"),
    ],
)
def test_get_month_name_br(month, expected):
    assert get_month_name_br(month) == expected
