def total_by_week(df):
    """
    Soma calorias e duração total por semana.
    """
    df = df.copy()
    df['semana'] = df['data'].dt.to_period('W').apply(lambda r: r.start_time)
    resumo = df.groupby('semana')[['duracao_min', 'calorias']].sum().reset_index()
    return resumo

def atividade_mais_frequente(df):
    """
    Retorna a atividade mais praticada.
    """
    return df['atividade'].value_counts().idxmax()

def dias_mais_ativos(df):
    """
    Retorna os dias da semana com mais prática de atividade física.
    """
    df['dia_semana'] = df['data'].dt.day_name()
    return df['dia_semana'].value_counts()