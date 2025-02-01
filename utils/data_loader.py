import json
import os

# Paths to data files
LIMITS_DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/mil_std_461G_RE102.json')
FREQ_DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/mil_std_frequencies.json')
ANTENNA_DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/antennas.json')

def load_json(file_path):
    """Generic function to load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ====== Load Frequencies ======
def load_frequencies():
    """Loads control frequencies from JSON file."""
    return load_json(FREQ_DATA_PATH)

def get_frequencies_by_version(standard_version):
    """Returns control frequencies for the given MIL-STD-461 version."""
    data = load_frequencies()
    return data.get(standard_version, [])

# ====== ЛИМИТЫ (LIMITS) ======
def load_limits():
    """Loads emission limits from JSON file."""
    return load_json(LIMITS_DATA_PATH)

def get_limits_by_frequency(frequency_mhz):
    """Gets the closest emission limits for a given frequency."""
    data = load_limits()
    results = []

    for category in data["categories"]:
        category_name = category["name"]
        for limit in category["limits"]:
            sub_category_name = limit["sub_category"]
            closest_limit = min(limit["data"], key=lambda x: abs(x["frequency_mhz"] - frequency_mhz))
            results.append({
                "category": category_name,
                "sub_category": sub_category_name,
                "frequency_mhz": closest_limit["frequency_mhz"],
                "limit_dbuv_m": closest_limit["limit_dbuv_m"]
            })
    
    return results

# ====== Antenna Factors ======
def load_antennas():
    """Loads antenna data from JSON file."""
    return load_json(ANTENNA_DATA_PATH)

def get_antenna_factor(antenna_type, frequency_mhz):
    """Returns the closest antenna factor for a given frequency."""
    antennas = load_antennas()
    
    if antenna_type not in antennas:
        return None
    
    antenna = antennas[antenna_type]
    factors = antenna["factors"]
    
    # Преобразуем ключи (частоты) в float, если они строковые
    factor_frequencies = {float(freq): value for freq, value in factors.items()}
    
    # Ищем ближайшую частоту
    closest_freq = min(factor_frequencies.keys(), key=lambda f: abs(f - frequency_mhz))
    
    return {
        "antenna": antenna["name"],
        "frequency_mhz": closest_freq,
        "factor_db_m": factor_frequencies[closest_freq]
    }

