from datetime import date
import calendar

import pandas as pd


def get_database(ano: int, mes: int) -> date:
    """
    Retorna a data final do mês especificado.

    Args:
        ano (int): O ano especificado.
        mes (int): O mês especificado.

    Returns:
        date: A data final do mês especificado.
    """
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    return date(ano, mes, ultimo_dia)

def get_primeiro_dia_ano(ano: int) -> date:
    """
    Retorna a data do primeiro dia do ano especificado.

    Args:
        ano (int): O ano especificado.

    Returns:
        date: A data do primeiro dia do ano especificado.
    """
    return date(ano, 1, 1)

