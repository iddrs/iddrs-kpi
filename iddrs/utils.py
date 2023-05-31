from datetime import date, timedelta, datetime
import calendar
import pandas as pd
import numpy as np


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

def completa_data_base(df: pd.DataFrame, ano: int, campos: list, index: str) -> pd.DataFrame:
    n = len(df)
    dates = pd.date_range(f'{str(ano)}-01-31', f'{str(ano)}-12-31', freq='M')
    df1 = pd.DataFrame({index: dates})
    for campo in campos:
        if campo == index:
            continue
        df1[campo] = pd.concat([df[campo], pd.Series(np.nan, index=list(range(n, 12)))])
    return df1

def xlimites_data_base(data_base: pd.Series) -> tuple:
    inicio = data_base.min()
    fim = data_base.max()
    ano = inicio.year
    mes = inicio.month - 1
    if mes < 1:
        mes = 12
        ano -= 1
    anterior = get_database(ano, mes)
    ano = fim.year
    mes = fim.month + 1
    if mes > 12:
        mes = 1
        ano += 1
    posterior = get_database(ano, mes)
    return(anterior, posterior)