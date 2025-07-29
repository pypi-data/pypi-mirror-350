from .changes import unique_column, id_autoincrement, async_create_table
from .updates import update_table_from_dataframe, async_update_table_from_dataframe
from .inspections import table_exists, async_table_exists
import logging


def upsert_table_database(
    df,
    conn,
    table_name: str,
    key_col: str,  # coluna de chave primária
    chunk_size: int = 500,
    exclude_update_columns: list[str] | str = None
) -> int:
    """
    Insere ou atualiza registros de cercas na web.

    :param df: pandas.DataFrame contendo os dados a serem inseridos
    ou atualizados.
    :param conn: Conexão ativa com o banco de dados.
    :return: Número de linhas afetadas ou None.
    """

    # Importar somente quando necessário
    import pandas as pd

    # Verificar se a coluna de chave primária existe
    if key_col not in df.columns:
        raise ValueError(f"A coluna '{key_col}' não existe no DataFrame")

    # Substituir valores NaN por None
    df = df.where(pd.notna(df), None)

    # Verifica se a tabela existe
    if not table_exists(conn, table_name):

        # Criar tabela usando pandas.to_sql
        df.to_sql(
            table_name,
            conn,
            if_exists='replace',
            index=False,
            chunksize=chunk_size,
        )

        # Definir uma coluna id com autoincrement
        id_autoincrement(conn, table_name)

        # Definir coluna key unique
        unique_column(conn, table_name, key_col)

        return len(df)  # Número de linhas inseridas

    # Atualizar a tabela existente em chunks
    chunksize = chunk_size

    # Para rastrear o total de linhas afetadas
    total_rows_affected = 0

    # Iterar sobre os chunks do DataFrame
    for start in range(0, len(df), chunksize):
        # Separar chunk
        chunk = df.iloc[start:start + chunksize]

        # Atualizar chunk
        rows_affected = update_table_from_dataframe(
            chunk, table_name, key_col, conn, exclude_update_columns
        )

        # Somar as linhas afetadas
        total_rows_affected += rows_affected

    return total_rows_affected


async def async_upsert_table_database(
    df,
    conn,
    table_name: str,
    key_col: str,
    chunk_size: int = 500,
    exclude_update_columns: list[str] | str = None
) -> int:
    """
    Insere ou atualiza registros em uma tabela do banco de dados de forma assíncrona.

    :param df: pandas.DataFrame contendo os dados.
    :param conn: Conexão assíncrona com o banco de dados.
    :param table_name: Nome da tabela a ser modificada.
    :param key_col: Nome da coluna chave primária.
    :param chunk_size: Número de registros a serem processados por vez.
    :param exclude_update_columns: Lista de colunas a serem excluídas do update.
    :return: Número de registros inseridos ou atualizados.
    """

    # Importar somente quando necessário
    import pandas as pd

    # Verificar se a coluna de chave primária existe
    if key_col not in df.columns:
        raise ValueError(f"A coluna '{key_col}' não existe no DataFrame")

    # Substituir valores NaN por None
    df = df.where(pd.notna(df), None)

    # Verifica se a tabela existe
    if not await async_table_exists(conn, table_name):
        logging.info(f"A tabela '{table_name}' não existe. Criando agora...")
        await async_create_table(conn, df, table_name, key_col, chunk_size)
        return len(df)  # Todas as linhas foram inseridas

    # Atualizar a tabela existente em chunks
    total_rows_affected = 0

    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start:start + chunk_size]

        rows_affected = await async_update_table_from_dataframe(
            chunk, table_name, key_col, conn, exclude_update_columns
        )

        total_rows_affected += rows_affected

    return total_rows_affected
