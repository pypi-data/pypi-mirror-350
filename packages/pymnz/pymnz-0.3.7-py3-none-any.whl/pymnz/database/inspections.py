def table_exists(conn, table_name: str) -> bool:
    """
    Verifica se uma tabela existe no banco de dados.

    :param conn: Conexão ativa com o banco de dados.
    :param table_name: Nome da tabela para verificar.
    :return: True se a tabela existir, caso contrário, False.
    """

    # Importar somente quando necessário
    from sqlalchemy import text

    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = :table_name
              AND table_schema = DATABASE()
        );
    """)

    # Executar query
    params = {"table_name": table_name}
    result = conn.execute(query, params)

    return result.scalar()  # Retorna True ou False


async def async_table_exists(conn, table_name: str) -> bool:
    """Verifica de forma assíncrona se uma tabela existe no banco de dados."""
    
    # Importar somente quando necessário
    from sqlalchemy import text

    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = :table_name
              AND table_schema = DATABASE()
        );
    """)
    result = await conn.execute(query, {"table_name": table_name})
    return result.scalar()
