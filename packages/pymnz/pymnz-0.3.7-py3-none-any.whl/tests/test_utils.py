from pymnz import utils
import pytest


def test_classes_singleton():
    # Classe
    @utils.classes.singleton
    class TestClass():
        ...

    # Teste de acerto
    assert TestClass() is TestClass(), \
        'Classe 1 e 2 não são a mesma instância'


def test_convert_unit_to_time():
    """ Testando função convert_time_to_unit """

    # Teste 1
    horas = 10
    minutos = 600
    segundos = 36000

    # Horas normais
    time_str = utils.convert_unit_to_time(horas, 'hours')
    assert time_str == '10:00:00', 'Horas não foram convertidas'

    # Minutos normais
    time_str = utils.convert_unit_to_time(minutos, 'minutes')
    assert time_str == '10:00:00', 'Minutos não foram convertidas'

    # Segundos normais
    time_str = utils.convert_unit_to_time(segundos, 'seconds')
    assert time_str == '10:00:00', 'Segundos não foram convertidas'

    # Horas anormais
    time_str = utils.convert_unit_to_time(segundos, 'hours')
    assert time_str == '36000:00:00'

    # Minutos anormais
    time_str = utils.convert_unit_to_time(segundos, 'minutes')
    assert time_str == '600:00:00'

    # Segundos anormais
    time_str = utils.convert_unit_to_time(segundos, 'seconds')
    assert time_str == '10:00:00'


def test_convert_time_to_unit():
    """ Testando função convert_time_to_unit """

    # Teste 1
    time_str: str = '10:20:30'
    time_str2: str = '10:20'
    time_str3: str = '10'
    time_str4: str = '54654:4w1:fk1'

    # Horas normais
    unit = utils.convert_time_to_unit(time_str, 'hours')
    assert unit == 10.341666666666667, 'Horas não foram convertidas'

    # Minutos normais
    unit = utils.convert_time_to_unit(time_str, 'minutes')
    assert unit == 620.5, 'Minutos não foram convertidas'

    # Segundos normais
    unit = utils.convert_time_to_unit(time_str, 'seconds')
    assert unit == 37230.0, 'Segundos não foram convertidas'

    # Horas anormais
    unit = utils.convert_time_to_unit(time_str2, 'hours')
    assert unit == 0.0, 'Horas não foram convertidas'

    # Minutos anormais
    unit = utils.convert_time_to_unit(time_str2, 'minutes')
    assert unit == 0.0, 'Minutos não foram convertidas'

    # Segundos anormais
    unit = utils.convert_time_to_unit(time_str2, 'seconds')
    assert unit == 0.0

    # Horas anormais 2
    unit = utils.convert_time_to_unit(time_str3, 'hours')
    assert unit == 0.0, 'Horas não foram convertidas'

    # Minutos anormais 2
    unit = utils.convert_time_to_unit(time_str3, 'minutes')
    assert unit == 0.0, 'Minutos não foram convertidas'

    # Segundos anormais 2
    unit = utils.convert_time_to_unit(time_str3, 'seconds')
    assert unit == 0.0

    # Horas anormais 3
    unit = utils.convert_time_to_unit(time_str4, 'hours')
    assert unit == 0.0, 'Horas não foram convertidas'

    # Minutos anormais 3
    unit = utils.convert_time_to_unit(time_str4, 'minutes')
    assert unit == 0.0, 'Minutos não foram convertidas'

    # Segundos anormais 3
    unit = utils.convert_time_to_unit(time_str4, 'seconds')
    assert unit == 0.0


def test_replace_invalid_values():
    import pandas as pd
    import datetime

    data = [
        {"name": "Alice", "age": 30, "birthdate": pd.Timestamp("1990-01-01")},
        {"name": "Bob", "age": pd.NA, "birthdate": pd.NaT},
        {"name": "Charlie", "age": 25, "birthdate": None}
    ]

    # Converter
    cleaned_data = utils.replace_invalid_values(data)

    saida = [
        {'name': 'Alice', 'age': 30, 'birthdate': datetime.datetime(
            1990, 1, 1, 0, 0)},
        {'name': 'Bob', 'age': None, 'birthdate': None},
        {'name': 'Charlie', 'age': 25, 'birthdate': None}
    ]

    assert cleaned_data == saida, 'Valores inválidos não foram substituídos'


def test_geometric_calculations():
    positions = [
        (-22.85907757964191, -43.60302741824395),
        (-22.864870669842283, -43.60151212148426),
        (-22.871756839811688, -43.61064701478057),
        (-22.86364283007362, -43.615350147549016)
    ]
    centro = utils.geographic_center(positions)
    
    assert centro == (-22.864836979842373, -43.60763417551445), 'Centro geográfico incorreto'

    destino = (-22.874471011545886, -43.61149614023986)
    distance = utils.calculate_distance(*centro, *destino)

    assert distance == 1.1419921539086124, 'Distância incorreta'


def test_geometric_calculations_incorrect():
    positions = []

    with pytest.raises(ValueError, match="A lista de posições não pode estar vazia."):
        utils.geographic_center(positions)

    centro = (None, None)
    destino = (-22.874471011545886, -43.61149614023986)
    result = utils.calculate_distance(*centro, *destino)
    assert result == None, 'Não está protegendo corretamente contra valores nulos'


def test_geometric_calculations_incorrect_2():
    positions = [
        (-22.85907757964191, -43.60302741824395),
        (None, -43.60151212148426),
        (-22.864870669842283, None),
        (-22.86364283007362, -43.615350147549016)
    ]
    centro = utils.geographic_center(positions)

    assert centro == None, 'Centro geográfico incorreto'
