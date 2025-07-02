import requests
from tabulate import tabulate

def standardize_name(name, username, fuzzy_level, fcode_filter="PCLI", fallback_key="name"):
    url = "https://secure.geonames.org/searchJSON"
    params = {
        'username': username,
        'q': name,
        'maxRows': 5,
        'fuzzy': round(fuzzy_level, 2),
        'style': 'FULL'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as ex:
        print(f"API error: {ex}")
        return None, []

    geonames = data.get("geonames", [])
    pcli_match = None
    alt_names = []

    for result in geonames:
        if result.get("fcode") == fcode_filter:
            alt_names = extract_alt_names(result)
            pcli_match = result.get(fallback_key)
            return pcli_match, alt_names[:5]

    # Fallback: Return top result if there are no PCLI matches
    if geonames:
        result = geonames[0]
        fallback_match = result.get(fallback_key)
        alt_names = extract_alt_names(result)
        return fallback_match, alt_names[:5]

    return None, []


def extract_alt_names(result):
    alt_list = result.get("alternateNames", [])
    return [
        alt.get("name") for alt in alt_list
        if alt.get("name") and len(alt.get("name")) > 2 and alt.get("name").isascii()
    ]


def find_match_with_fuzzy(names, username, fcode_filter="PCLI", fallback_key="name", min_fuzzy=0.30, max_fuzzy=1, step=0.10):
    results = []

    for name in names:
        fuzzy = max_fuzzy
        matched = None # Fallback value
        alternates = []
        final_fuzzy = fuzzy

        while fuzzy >= min_fuzzy:
            match, alt_names = standardize_name(name, username, fuzzy, fcode_filter, fallback_key)
            print(f"{name}: Fuzzy={fuzzy:.1f} → {match}")

            if match and match.lower() != name.lower():
                matched = match
                alternates = alt_names
                final_fuzzy = fuzzy
                break
            fuzzy = round(fuzzy - step, 2)

        # If no country matched, attempt fallback
        if not matched:
            fallback_match, fallback_alts = standardize_name(name, username, max_fuzzy, None, fallback_key)
            matched = fallback_match if fallback_match else name
            alternates = fallback_alts

        results.append((f"{name}", f"(fuzzy={final_fuzzy:.1f})", ", ".join(alternates), matched))

    return results


# API version test
if __name__ == "__main__":
    username = "rishnaik" # Geonames username
    test_names = ["Grate Britan", "Indes", "Japn", "Deutchlnd", "Curacao", "Sudahn", "Koria", "Ivorie Cost"]
    corrected_rows = find_match_with_fuzzy(test_names, username)

    print(tabulate(corrected_rows, headers=["Misspelled Name", "Fuzzy", "Alternate Spellings", "Final Match"]))