import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Вычисляет расстояние между двумя точками на Земле с использованием формулы Haversine.
    Результат возвращается в километрах.
    """
    # Радиус Земли в километрах
    R = 6371.0

    # Преобразование градусов в радианы
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Разница между широтами и долготами
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Вычисление расстояния с помощью формулы Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


# Координаты точек вертикали
lat1 = 50.7124420
lon1 = 37.5853695
lat2 = 50.7028348
lon2 = 37.5855733

# Вычисление расстояния
distance = haversine_distance(lat1, lon1, lat2, lon2)
print(f"Расстояние между координатами по вертикали: {distance} км")

# Координаты точек по горизонтали
lat3 = 50.7129855
lon3 = 37.5730970
lat4 = 50.7129583
lon4 = 37.5944045

# Вычисление расстояния
distance = haversine_distance(lat3, lon3, lat4, lon4)
print(f"Расстояние между координатами по горизонтали: {distance} км")


import geocoder
g = geocoder.geonames('Mountain View, CA')
#g.geojson
#g.json
#g.wkt
#g.osm
for result in g:
    print(result)