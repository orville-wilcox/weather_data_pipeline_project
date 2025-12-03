# src/validation/validator.py

def validate_weather_payload(payload: dict) -> tuple[bool, list[str]]:
    """
    Validate required fields of the OpenWeather payload.
    Returns:
        (is_valid, errors)
    """

    errors = []

    # --- Required paths ---
    required_paths = {
        "dt": int,
        "id": int,
        "name": str,
        "sys.country": str,
        "timezone": int,
        "coord.lat": (int, float),
        "coord.lon": (int, float),
        "main.temp": (int, float),
        "main.feels_like": (int, float),
        "main.humidity": int,
        "main.pressure": int,
        "wind.speed": (int, float),
        "wind.deg": int,
        "clouds.all": int,
        "visibility": int,
        "weather[0].main": str,
        "weather[0].description": str,
    }

    # --- Helper to extract nested fields ---
    def get_nested(data, path):
        keys = path.replace("]", "").split(".")
        for key in keys:
            if "[" in key:  # handle list index
                key, idx = key.split("[")
                idx = int(idx)
                data = data.get(key, [])
                if len(data) <= idx:
                    return None
                data = data[idx]
            else:
                data = data.get(key)
            if data is None:
                return None
        return data

    # --- Validation ---
    for field_path, expected_type in required_paths.items():
        value = get_nested(payload, field_path)
        if value is None:
            errors.append(f"Missing field: {field_path}")
        elif not isinstance(value, expected_type):
            errors.append(
                f"Invalid type for {field_path}: got {type(value)}, expected {expected_type}"
            )

    # --- Business rules ---
    if get_nested(payload, "main.humidity") is not None:
        humidity = get_nested(payload, "main.humidity")
        if not (0 <= humidity <= 100):
            errors.append("Humidity out of range (0–100)")

    if get_nested(payload, "wind.speed") is not None:
        ws = get_nested(payload, "wind.speed")
        if ws < 0:
            errors.append("Wind speed cannot be negative")

    if get_nested(payload, "clouds.all") is not None:
        cc = get_nested(payload, "clouds.all")
        if not (0 <= cc <= 100):
            errors.append("Cloud cover out of range (0–100)")

    return (len(errors) == 0, errors)
