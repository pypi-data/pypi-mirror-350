def replace_invalid_values(values: list[dict]) -> list[dict]:
    """Função para substituir valores indesejados por None"""

    # Importar somente quando necessário
    import pandas as pd

    # Verificar se o argumento é uma lista
    if not isinstance(values, list):
        raise TypeError("O argumento deve ser uma lista de dicionários")

    # Criar uma nova lista para evitar modificar a original
    new_values = []

    for record in values:
        new_record = {}
        for key, value in record.items():
            # Substituir pd.NaT, np.nan, e datas inválidas por None
            if pd.isna(value):
                new_record[key] = None
            elif isinstance(value, pd.Timestamp):
                new_record[key] = value.to_pydatetime()
            else:
                new_record[key] = value  # Mantém o valor original
        new_values.append(new_record)

    return new_values
