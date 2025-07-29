from pymnz.utils import replace_invalid_values


def update_table_from_dataframe(
    df,
    table_name: str,
    primary_keys: list[str] | str,
    conn,
    exclude_update_columns: list[str] | str = None
) -> int:
    """
    Atualiza uma tabela no banco de dados MySQL de forma sincrona com base em um DataFrame.

    :param df: pandas.DataFrame contendo os dados a serem atualizados.
    :param table_name: Nome da tabela no banco de dados.
    :param primary_keys: Lista de colunas que são chaves primárias ou índices únicos.
    :param conn: Conexão sincrona com o banco de dados via SQLAlchemy.
    :param exclude_update_columns: Lista de colunas que não devem ser atualizadas no upsert.
    :return: Número de linhas atualizadas.
    """

    # Importar somente quando necessário
    from sqlalchemy import text

    # Verificar se primary_keys é uma string
    if isinstance(primary_keys, str):
        primary_keys = [primary_keys]
  
    # Verificar se exclude_update_columns é uma string
    if isinstance(exclude_update_columns, str):
        exclude_update_columns = [exclude_update_columns]
  
    # Verificar se todas as colunas de chave primária existem no DataFrame
    if not all(pk in df.columns for pk in primary_keys):
        raise ValueError("Uma ou mais colunas de chave primária não existem no DataFrame.")

    exclude_update_columns = set(exclude_update_columns or [])
    columns = list(df.columns)
    placeholders = ", ".join([f":{col}" for col in columns])

    # Definir as colunas que serão atualizadas, excluindo as chaves primárias e as excluídas
    update_columns = [col for col in columns if col not in primary_keys and col not in exclude_update_columns]
    update_placeholders = ", ".join([f"{col}=VALUES({col})" for col in update_columns])

    query = text(f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE {update_placeholders};
    """)

    values = df.to_dict(orient="records")

    # Substituir valores indesejados por None
    values = replace_invalid_values(values)

    # Executar a query em massa com SQLAlchemy
    # Passa o texto da query e os valores
    conn.execute(query, values)
    conn.commit()

    return len(df)


async def async_update_table_from_dataframe(
    df,
    table_name: str,
    primary_keys: list[str] | str,
    conn,
    exclude_update_columns: list[str] | str = None
) -> int:
    """
    Atualiza uma tabela no banco de dados MySQL de forma assíncrona com base em um DataFrame.

    :param df: pandas.DataFrame contendo os dados a serem atualizados.
    :param table_name: Nome da tabela no banco de dados.
    :param primary_keys: Lista de colunas que são chaves primárias ou índices únicos.
    :param conn: Conexão assíncrona com o banco de dados via SQLAlchemy.
    :param exclude_update_columns: Lista de colunas que não devem ser atualizadas no upsert.
    :return: Número de linhas atualizadas.
    """

    # Importar somente quando necessário
    from sqlalchemy import text

    # Verificar se primary_keys é uma string
    if isinstance(primary_keys, str):
        primary_keys = [primary_keys]
  
    # Verificar se exclude_update_columns é uma string
    if isinstance(exclude_update_columns, str):
        exclude_update_columns = [exclude_update_columns]
  
    # Verificar se todas as colunas de chave primária existem no DataFrame
    if not all(pk in df.columns for pk in primary_keys):
        raise ValueError("Uma ou mais colunas de chave primária não existem no DataFrame.")

    exclude_update_columns = set(exclude_update_columns or [])
    columns = list(df.columns)
    placeholders = ", ".join([f":{col}" for col in columns])

    # Definir as colunas que serão atualizadas, excluindo as chaves primárias e as excluídas
    update_columns = [col for col in columns if col not in primary_keys and col not in exclude_update_columns]
    update_placeholders = ", ".join([f"{col}=VALUES({col})" for col in update_columns])

    query = text(f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE {update_placeholders};
    """)

    values = df.to_dict(orient="records")

    # Substituir valores indesejados por None
    values = replace_invalid_values(values)

    await conn.execute(query, values)
    await conn.commit()

    return len(df)
