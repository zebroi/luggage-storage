# linking.py

def get_nearby_cities(current_city_slug, all_cities, count=5):
    """
    Приоритет выбора соседних городов:
    1. Та же страна — берём ближайшие по алфавиту
    2. Если в стране < 5 городов — добираем из других стран
    """
    current = all_cities[current_city_slug]
    same_country = [
        c for slug, c in all_cities.items()
        if c["country_code"] == current["country_code"]
        and slug != current_city_slug
    ]

    # Детерминированный рандом по slug
    rng = random.Random(current_city_slug + "-links")
    selected = rng.sample(same_country, min(count, len(same_country)))

    # Добираем из других стран если не хватает
    if len(selected) < count:
        other = [
            c for slug, c in all_cities.items()
            if c["country_code"] != current["country_code"]
            and slug != current_city_slug
        ]
        extra = rng.sample(other, count - len(selected))
        selected += extra

    return selected


def get_country_tags(current_country_code, all_countries, count=10):
    """10 стран для тегов внизу — исключая текущую"""
    rng = random.Random(current_country_code + "-countries")
    other_countries = [
        c for code, c in all_countries.items()
        if code != current_country_code
    ]
    return rng.sample(other_countries, min(count, len(other_countries)))


def build_city_card(city_data):
    """Генерирует HTML одной карточки города"""
    template = open("template_city_card.html").read()
    return (template
        .replace("{{NEARBY_CITY_URL}}", city_data["url"])
        .replace("{{NEARBY_CITY_NAME}}", city_data["name"])
        .replace("{{NEARBY_CITY_FLAG}}", city_data["flag"])
        .replace("{{NEARBY_CITY_COUNTRY}}", city_data["country_name"])
        .replace("{{NEARBY_CITY_SERVICE_COUNT}}", str(city_data["service_count"]))
        .replace("{{NEARBY_CITY_PRICE}}", city_data["price_from"])
    )


def build_country_tag(country_data):
    """Генерирует HTML одного тега страны"""
    return f'<a href="{country_data["url"]}" class="tag tag-link">{country_data["flag"]} {country_data["name"]}</a>'