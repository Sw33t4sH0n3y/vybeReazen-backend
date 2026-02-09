SAFEGUARDS = {
    "frequency_min_hz": 20,
    "frequency_max_hz": 1000,
    "max_master_volume": 0.90,
    "max_session_minutes": 120
}

def validate_volume(volume: float) -> tuple[bool,str]:
    if volume > SAFEGUARDS["max_master_volume"]:
        return False, f"Volume exceeds max of {SAFEGUARDS['max_master_volume']}"
    return True, "Valid"

def validate_frequency(hertz: int) -> tuple[bool, str]:
    if hertz < SAFEGUARDS["frequency_min_hz"]:
        return False, f"Frequency too low (infrasound)"
    if hertz > SAFEGUARDS["frequency_max_hz"]:
        return False, f"Frequency exceeds safe range"
    return True, "Valid"

def get_safeguards():
    return SAFEGUARDS                   