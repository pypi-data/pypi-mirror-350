import logging


class FunctionExecutor:
    """Singleton - Executor de funções com gerenciamento de resultados"""

    def __init__(self) -> None:
        self.results = []

    def add_function(self, func, *args, **kwargs) -> None:
        """Adiciona uma função e seus argumentos
        à lista de funções a serem executadas."""
        self.results.append((func, args, kwargs))

    def execute_all(self, *params, **kwparams) -> None:
        """Executa todas as funções armazenadas e registra os resultados."""

        class_name = self.__class__.__name__
        logging.info(
            f'({class_name}) Executando funções armazenadas')

        if self.results:
            for func, args, kwargs in self.results:
                try:
                    func(*args, *params, **kwargs, **kwparams)
                except Exception as e:
                    logging.error(f"Erro ao executar {func.__name__}: {e}")
        else:
            logging.info(
                f"({class_name}) Nenhuma função armazenada para execução")

    def clear_results(self) -> None:
        """Limpa a lista de funções armazenadas."""
        self.results.clear()
