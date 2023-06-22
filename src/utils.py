import pandas as pd

def df_table(df, spec, fmt=None):
    if fmt != None:
        for c, f in fmt.items():
            df[c] = df[c].map(f)
    df = df[list(spec.keys())]
    df.columns = list(spec.values())
    return df

def int_formatter(x, pos):
    x = int(x)
    return f'{x:,.0f}'.replace(',', '_').replace('.', ',').replace('_', '.')

def money_formatter(x):
    if pd.isnull(x):
        return ''
    if x < 0.0:
        return f'({x:,.2f})'.replace(',', '_').replace('.', ',').replace('_', '.').replace('-', '')
    if x > 0.0:
        return f'{x:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
    if x == 0.0:
        return '-'
    

def perc0_formatter(x):
    if pd.isnull(x):
        return ''
    x = round(x, 2)
    if x < 0.0:
        return f'({x:,.0%})'.replace(',', '_').replace('.', ',').replace('_', '.').replace('-', '')
    if x > 0.0:
        return f'{x:,.0%}'.replace(',', '_').replace('.', ',').replace('_', '.')
    if x == 0.0:
        return '-'
    
def date_to_month_name(x):
    if pd.isnull(x):
        return ''
    return x.strftime('%b')