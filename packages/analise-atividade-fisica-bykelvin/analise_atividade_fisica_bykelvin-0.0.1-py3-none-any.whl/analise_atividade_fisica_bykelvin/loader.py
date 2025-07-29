import pandas as pd

def load_data(filepath):
    """
    Lê um arquivo CSV com colunas: data, atividade, duracao_min, calorias.
    Retorna um DataFrame com coluna data convertida para datetime.
    """
    df = pd.read_csv(filepath)
    df['data'] = pd.to_datetime(df['data'])
    return df