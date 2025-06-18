import requests


def standardize_country(name, username, fuzzy_level):
    url = "https://secure.geonames.org/searchJSON"
    params = {
        'username': username,
        'q': name,
        'maxRows': 5,
        'fuzzy': round(fuzzy_level, 2),
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as ex:
        print(f"API error: {ex}")
        return None

    for countryName in data.get("geonames", []):
        if countryName.get("fcode") == "PCLI":  # Confirm it's a country
            return countryName.get("name")

    return name  # Fallback if no country match found


def find_country_with_fuzzy(name, username):
    for i in range(0, 11):  # 0 to 10 inclusive
        fuzzy_val = i / 10
        match = standardize_country(name, username, fuzzy_val)
        print(f"Fuzzy={fuzzy_val:.1f} → {match}")
        if match:
            return match

    return name  # fallback if no match found


# API version test
if __name__ == "__main__":
    username = "rishnaik" # Geonames username
    name = "Brzil"  # Try a misspelled country
    result = find_country_with_fuzzy(name, username)
    print(f"Final Match: {name} -> {result}")