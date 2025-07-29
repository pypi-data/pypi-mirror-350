import time
import asyncio
import logging
from functools import wraps
from typing import Callable, Literal


async def async_countdown_timer(wait_seconds: int, msg_wait: str = ""):
    """
    Contagem regressiva assíncrona.

    Parameters:
        wait_seconds (int): Número de segundos para a contagem regressiva.
        msg_wait (str): Mensagem a ser exibida durante a contagem regressiva.
    """
    for i in range(wait_seconds, 0, -1):
        print(f"{msg_wait} {i} second(s)...{' '*10}", end='\r')
        await asyncio.sleep(1)  # Espera assíncrona de 1 segundo

    # Encerramento
    print(' ' * 100, end='\r')


def countdown_timer(wait_seconds: int, msg_wait: str = ""):
    """
    Contagem regressiva assíncrona.

    Parameters:
        wait_seconds (int): Número de segundos para a contagem regressiva.
        msg_wait (str): Mensagem a ser exibida durante a contagem regressiva.
    """
    for i in range(wait_seconds, 0, -1):
        print(f"{msg_wait} {i} second(s)...{' '*10}", end='\r')
        time.sleep(1)  # Espera assíncrona de 1 segundo

    # Encerramento
    print(' ' * 100, end='\r')


def retry_on_failure(max_retries: int, retry_interval: int = 5):
    """
    Decorator that retries the execution of a function in case of failure.
    Supports both synchronous and asynchronous functions.

    Parameters:
        max_retries (int): Maximum number of retry attempts.

    Returns:
        The decorated function which will be executed with retries.
    """
    def decorator(function: Callable):
        @wraps(function)
        async def async_wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    if asyncio.iscoroutinefunction(function):
                        return await function(*args, **kwargs)
                    else:
                        return function(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.error(f"Attempt {attempts}/{max_retries} failed with error: {e}")
                    if attempts < max_retries:
                        await async_countdown_timer(retry_interval * attempts, 'Retrying in')  # Exponential backoff
                    else:
                        logging.error("All retry attempts failed.")
                        return None

        @wraps(function)
        def sync_wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.error(f"Attempt {attempts}/{max_retries} failed with error: {e}")
                    if attempts < max_retries:
                        countdown_timer(retry_interval * attempts, 'Retrying in')  # Exponential backoff
                    else:
                        logging.error("All retry attempts failed.")
                        return None

        # Retorna o wrapper apropriado dependendo se a função é assíncrona ou não
        if asyncio.iscoroutinefunction(function):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def convert_time_to_unit(
    time_str: str,
    unit: Literal['seconds', 'minutes', 'hours'] = 'hours'
) -> float:
    """
    Converte um horário no formato HH:MM:SS para a
    unidade de tempo especificada.

    Parameters:
    time_str (str): String representando o horário no formato HH:MM:SS.
    unit (str): Unidade de tempo para a conversão
    ('seconds', 'minutes', 'hours').

    Returns:
    float: O total de tempo na unidade especificada.
    Retorna 0 se o input for inválido ou None.
    """
    if time_str:
        try:
            # Dividir a string em horas, minutos e segundos
            hours, minutes, seconds = map(int, time_str.split(':'))

            # Calcular o total de segundos
            total_seconds = (hours * 3600) + (minutes * 60) + seconds

            # Converter para a unidade desejada
            if unit == 'seconds':
                return float(total_seconds)
            elif unit == 'minutes':
                return total_seconds / 60
            elif unit == 'hours':
                return total_seconds / 3600
            else:
                raise ValueError(f"Invalid unit: {unit}")
        except ValueError:
            # Retornar 0 se a string não estiver no formato correto
            return 0.0
    return 0.0


def convert_unit_to_time(
    value: float,
    unit: Literal['seconds', 'minutes', 'hours'] = 'seconds'
) -> str:
    """
    Converts a value in hours, minutes, or seconds to HH:MM:SS format.

    Parameters:
    value (int, float, or str): The value to be converted.
    unit (str): The unit of the value ('hours', 'minutes', or 'seconds').

    Returns:
    str: A string representing the time in HH:MM:SS format.
    """
    if value:
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return '00:00:00'

        # Ensure value is not negative
        value = max(0, float(value))

        # Convert value to total seconds based on the unit
        match unit:
            case'hours':
                total_seconds = int(value * 3600)
            case 'minutes':
                total_seconds = int(value * 60)
            case 'seconds':
                total_seconds = int(value)
            case _:
                raise ValueError(
                    "Invalid unit. Use 'hours', 'minutes', or 'seconds'.")

        # Calculate hours, minutes, and seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the output in the desired format
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    return '00:00:00'


if __name__ == "__main__":

    horas = 25.555555555555

    time_str = convert_unit_to_time(horas, unit='hours')

    horas_converted = convert_time_to_unit(time_str, 'hours')

    print(horas, time_str, horas_converted)  # Output: 25 25:00:00 25.0
