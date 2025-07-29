from typing import List, Tuple
from decimal import Decimal
import math


def geographic_center(positions: List[Tuple[float, float]]) -> Tuple[float, float]:
    """
    Calcula o centro geográfico a partir de uma lista de coordenadas de latitude e longitude.

    :param positions: Lista de tuplas (latitude, longitude).
    :return: Uma tupla (latitude_central, longitude_central).
    """
    if not positions:
        raise ValueError("A lista de posições não pode estar vazia.")

    # Validar as coordenadas
    if not all(isinstance(coord, (float, int, Decimal)) for coords in positions for coord in coords):
        return None

    # Separa as latitudes e longitudes
    latitudes, longitudes = zip(*positions)

    # Calcula a média das latitudes e longitudes
    lat_centro = sum(latitudes) / len(latitudes)
    lon_centro = sum(longitudes) / len(longitudes)

    return lat_centro, lon_centro


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine.

    :param lat1: Latitude do primeiro ponto.
    :param lon1: Longitude do primeiro ponto.
    :param lat2: Latitude do segundo ponto.
    :param lon2: Longitude do segundo ponto.
    :return: Distância em quilômetros entre os dois pontos.
    """
    # Raio médio da Terra em km
    R = 6371.0  

    # Validar as coordenadas
    if not all(isinstance(coord, (float, int, Decimal)) for coord in [lat1, lon1, lat2, lon2]):
        return None

    # Converter para float se os valores forem Decimal
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

    # Converter graus para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Diferença das coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distância final
    distance = R * c
    return distance


if __name__ == "__main__":
    positions = [
        (-22.85907757964191, -43.60302741824395),
        (-22.864870669842283, -43.60151212148426),
        (-22.871756839811688, -43.61064701478057),
        (-22.86364283007362, -43.615350147549016)
    ]
    centro = geographic_center(positions)
    print(f"O centro geográfico entre {positions} é {centro}")
    
    destino = (-22.874471011545886, -43.61149614023986)
    distance = calculate_distance(*centro, *destino)
    print(f"A distância entre {centro} e {destino} é de {distance:.2f} km")
