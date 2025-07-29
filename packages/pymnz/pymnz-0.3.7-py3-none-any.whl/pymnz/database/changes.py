def unique_column(conn, table_name: str, key_col: str) -> None:
    """Alterar coluna para que seja única"""
    # Importar somente o que é necessário
    from sqlalchemy import text

    query = text(f"""
        ALTER TABLE {table_name}
        ADD CONSTRAINT UNIQUE ({key_col});
    """)
    conn.execute(query)


def id_autoincrement(conn, table_name: str) -> None:
    """Alterar tabela para adicionar a coluna 'id' com autoincrement"""
    # Importar somente o que é necessário
    from sqlalchemy import text

    # Montar query diretamente
    query = text(f"""
        ALTER TABLE {table_name}
        ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;
    """)

    # Executar query
    conn.execute(query)


async def async_unique_column(conn, table_name: str, key_col: str) -> None:
    """Altera uma coluna para que seja única no banco de dados."""
    
    # Importar somente quando necessário
    from sqlalchemy import text
    
    query = text(f"""
        ALTER TABLE {table_name} ADD CONSTRAINT UNIQUE ({key_col});
    """)
    await conn.execute(query)


async def async_id_autoincrement(conn, table_name: str) -> None:
    """Adiciona uma coluna 'id' com autoincrement na tabela."""
    
    # Importar somente quando necessário
    from sqlalchemy import text
    
    query = text(f"""
        ALTER TABLE {table_name} ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;
    """)
    await conn.execute(query)


async def async_create_table(conn, df, table_name: str, key_col: str, chunk_size: int):
    """Cria uma nova tabela com base no DataFrame e define colunas únicas e autoincrement."""
    
    await conn.run_sync(lambda sync_conn: df.to_sql(
        table_name, sync_conn, if_exists='replace', index=False, chunksize=chunk_size
    ))
    await async_id_autoincrement(conn, table_name)
    await async_unique_column(conn, table_name, key_col)
    await conn.commit()
