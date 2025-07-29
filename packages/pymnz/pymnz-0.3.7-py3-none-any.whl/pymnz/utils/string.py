def search_str(
    string: str,
    string_padrao: str,
    inicio_padrao: str = '[',
    fim_padrao: str = ']',
    up=True
):
    """
    Busca um padrão específico dentro de uma string e retorna o conteúdo
    encontrado entre os delimitadores.

    Args:
        string (str): A string a ser verificada.
        string_padrao (str): A chave padrão que precede o conteúdo desejado.
        inicio_padrao (str): Caractere que indica o início do conteúdo
        (padrão: '[').
        fim_padrao (str): Caractere que indica o fim do conteúdo (padrão: ']').
        up (bool): Se True, retorna o conteúdo encontrado em maiúsculas.

    Returns:
        str: O conteúdo encontrado entre os delimitadores,
        ou uma string vazia se não encontrado.
    """
    # Localiza a posição da string padrão
    pos_padrao = string.find(string_padrao)

    # Verifica se a string padrão foi encontrada
    if pos_padrao == -1:
        return ""

    # Calcula a posição inicial para a busca do conteúdo
    pos_inicial = pos_padrao + len(string_padrao)
    conteudo = ""
    dentro_do_conteudo = False

    # Itera sobre os caracteres da string a partir da posição inicial
    for char in string[pos_inicial:]:
        if char == fim_padrao:
            break
        elif dentro_do_conteudo:
            conteudo += char
        elif char == inicio_padrao:
            dentro_do_conteudo = True

    # Retorna o conteúdo encontrado, aplicando a formatação desejada
    return conteudo.strip().upper() if up else conteudo.strip()
