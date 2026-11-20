"""
Input validation, bounds-checking, and sanitization utilities.
"""
import html
import re
from typing import Dict, Any, List

def sanitize_string(value: str, max_length: int = 150) -> str:
    """Strip dangerous characters, cap length, and escape HTML entities."""
    if not isinstance(value, str):
        return ""
    # Strip null bytes and control chars
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    cleaned = cleaned.strip()[:max_length]
    return html.escape(cleaned)

def validate_aqi(value: Any, default: int = 150) -> int:
    """Ensure AQI is an integer bounded between 0 and 1000."""
    try:
        val = int(value)
        return max(0, min(1000, val))
    except (ValueError, TypeError):
        return default

def validate_pm25(value: Any, default: float = 60.0) -> float:
    """Ensure PM2.5 is a float bounded between 0.0 and 1500.0."""
    try:
        val = float(value)
        return max(0.0, min(1500.0, round(val, 2)))
    except (ValueError, TypeError):
        return default

def validate_choice(value: str, allowed: List[str], default: str) -> str:
    """Validate string against allowed choices."""
    if isinstance(value, str) and value.strip().lower() in [a.lower() for a in allowed]:
        return value.strip().lower()
    return default

def sanitize_household_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize full incoming recommendation request payload."""
    location = sanitize_string(payload.get("location", "Delhi"), max_length=80)
    if not location:
        location = "Delhi"
        
    aqi_input_type = validate_choice(
        payload.get("aqi_input_type", "preset"),
        ["live", "preset", "custom"],
        "preset"
    )
    
    preset_severity = validate_choice(
        payload.get("preset_severity", "Severe"),
        ["moderate", "poor", "very poor", "severe"],
        "severe"
    ).title()
    
    custom_aqi = validate_aqi(payload.get("custom_aqi", 150))
    time_of_day = validate_choice(
        payload.get("time_of_day", "morning"),
        ["morning", "afternoon", "evening", "night"],
        "morning"
    )
    
    commute_mode = validate_choice(
        payload.get("commute_mode", "public_bus_metro"),
        ["two_wheeler", "public_bus_metro", "car_alone", "carpool_walk"],
        "public_bus_metro"
    )
    
    housing_type = validate_choice(
        payload.get("housing_type", "apartment"),
        ["apartment", "independent_house", "multistory_flat"],
        "apartment"
    )
    
    cooking_heating = validate_choice(
        payload.get("cooking_heating", "lpg_gas"),
        ["lpg_gas", "induction_electric", "biomass_kerosene", "wood_coal"],
        "lpg_gas"
    )
    
    budget_tier = validate_choice(
        payload.get("budget_tier", "low_cost"),
        ["free", "low_cost", "equipment_ready"],
        "low_cost"
    )
    
    raw_vulnerable = payload.get("vulnerable_members", [])
    valid_vulnerable = []
    allowed_vulnerable = {"children", "seniors", "asthma", "pregnant"}
    if isinstance(raw_vulnerable, list):
        for v in raw_vulnerable:
            if isinstance(v, str) and v.lower() in allowed_vulnerable:
                valid_vulnerable.append(v.lower())
                
    user_question = sanitize_string(payload.get("user_question", ""), max_length=300)

    return {
        "location": location,
        "aqi_input_type": aqi_input_type,
        "preset_severity": preset_severity,
        "custom_aqi": custom_aqi,
        "time_of_day": time_of_day,
        "commute_mode": commute_mode,
        "housing_type": housing_type,
        "cooking_heating": cooking_heating,
        "budget_tier": budget_tier,
        "vulnerable_members": valid_vulnerable,
        "user_question": user_question
    }

def sanitize_activity_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize activity evaluation request payload."""
    activity = sanitize_string(payload.get("activity", ""), max_length=200)
    if not activity:
        activity = "Outdoor Morning Jog"

    location = sanitize_string(payload.get("location", "Delhi"), max_length=80)
    if not location:
        location = "Delhi"

    aqi_input_type = validate_choice(
        payload.get("aqi_input_type", "preset"),
        ["live", "preset", "custom"],
        "preset"
    )

    preset_severity = validate_choice(
        payload.get("preset_severity", "Severe"),
        ["moderate", "poor", "very poor", "severe"],
        "severe"
    ).title()

    custom_aqi = validate_aqi(payload.get("custom_aqi", 150))
    time_of_day = validate_choice(
        payload.get("time_of_day", "morning"),
        ["morning", "afternoon", "evening", "night"],
        "morning"
    )

    housing_type = validate_choice(
        payload.get("housing_type", "apartment"),
        ["apartment", "independent_house", "multistory_flat"],
        "apartment"
    )

    raw_vulnerable = payload.get("vulnerable_members", [])
    valid_vulnerable = []
    allowed_vulnerable = {"children", "seniors", "asthma", "pregnant"}
    if isinstance(raw_vulnerable, list):
        for v in raw_vulnerable:
            if isinstance(v, str) and v.lower() in allowed_vulnerable:
                valid_vulnerable.append(v.lower())

    return {
        "activity": activity,
        "location": location,
        "aqi_input_type": aqi_input_type,
        "preset_severity": preset_severity,
        "custom_aqi": custom_aqi,
        "time_of_day": time_of_day,
        "housing_type": housing_type,
        "vulnerable_members": valid_vulnerable
    }

