import sys
import os
import asyncio
from typing import Callable, Optional
from pymnz.utils.classes import singleton
from pymnz.utils import countdown_timer, retry_on_failure


@singleton
class Script:
    def __init__(self, name: str, code: Callable, *args, **kwargs):
        self.name = name
        self.code_start: Optional[Callable] = None
        self.args_start: tuple = ()
        self.kwargs_start: dict = {}
        self.code = code
        self.args = args
        self.kwargs = kwargs
        self.execution_interval = 10
        self.execution_interval_msg = 'Executando novamente em'
        self.width = 80
        self.separator_format = '='
        self.terminator_format = 'x'
        self.terminator_msg = 'Fim do script'

    def _show_header(self):
        """Mostrar cabeçalho."""
        print(self.separator_format * self.width)
        print(str(self.name).upper().center(self.width))
        print(self.separator_format * self.width)

    def _run_code(self, code: Callable, *args, **kwargs):
        """Executar código assíncrono."""
        if code is not None:
            if asyncio.iscoroutinefunction(code):
                asyncio.run(code(*args, **kwargs))
            else:
                code(*args, **kwargs)
            print(self.separator_format * self.width)

    @retry_on_failure(1000)
    def _run_code_with_retry_on_failure(self, code: Callable, *args, **kwargs):
        """Executar código com repetição por falha."""
        self._run_code(code, *args, **kwargs)

    def _run(self, code: Callable, with_retry_on_failure: bool, *args, **kwargs):
        """Executar código de acordo com os parâmetros."""
        if with_retry_on_failure:
            self._run_code_with_retry_on_failure(code, *args, **kwargs)
        else:
            self._run_code(code, *args, **kwargs)

    def run(self, with_retry_on_failure: bool = True):
        """Executar o script"""
        # Limpar console
        os.system('cls')

        # Mostrar cabeçalho
        self._show_header()

        try:
            # Executar código inicial
            if self.code_start is not None:
                self._run(self.code_start, with_retry_on_failure, *self.args_start, **self.kwargs_start)

            # Executar código em loop
            while True:
                self._run(self.code, with_retry_on_failure, *self.args, **self.kwargs)
                countdown_timer(self.execution_interval, self.execution_interval_msg)

        except KeyboardInterrupt:
            print(self.terminator_format * self.width)
            sys.exit(self.terminator_msg)

    def set_code_start(self, code: Callable, *args, **kwargs):
        """Adicionar código inicial."""
        self.code_start = code
        self.args_start = args
        self.kwargs_start = kwargs
        return self
