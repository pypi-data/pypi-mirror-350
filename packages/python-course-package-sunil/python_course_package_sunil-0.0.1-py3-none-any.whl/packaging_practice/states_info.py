import json
from pathlib import Path
from typing import List

THIS_DIR = Path(__file__).parent
CITIES_JSON_FPATH = THIS_DIR / "cities.json"


def is_city_capitol_of_state(city_name: str, state: str) -> bool:
    """Return True if `city_name` is the capitol of `state`."""
    cities_json_contents = CITIES_JSON_FPATH.read_text()
    cities: List[dict] = json.loads(cities_json_contents)
    matching_cities: List[dict] = [city for city in cities if city["city"] == city_name]
    if len(matching_cities) == 0:
        return False
    matched_city = matching_cities[0]
    return matched_city["state"] == state


if __name__ == "__main__":
    print(is_city_capitol_of_state(city_name="Montgomery", state="Alabama"))