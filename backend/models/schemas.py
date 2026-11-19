"""
Data models and schemas for Air Quality Context and Recommendations.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass
class AirQualityContext:
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    aqi: int = 150
    pm2_5: float = 65.0
    pm10: float = 120.0
    severity_tier: str = "Poor"  # Moderate, Poor, Very Poor, Severe
    source: str = "preset"       # live, preset, custom
    timestamp: str = ""
    no2: float = 45.0
    so2: float = 18.0
    co: float = 1.2
    o3: float = 28.0
    temperature: float = 19.5
    humidity: int = 76
    wind_speed: float = 4.5
    who_multiplier: float = 4.3
    cigarette_equiv: float = 3.0
    standard_name: str = "CPCB (National AQI - India)"
    operator_source: str = "Central Pollution Control Board (CPCB) / IMD"
    is_indian_standard: bool = True
    hotspots: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class HouseholdProfile:
    commute_mode: str = "public_bus_metro"  # two_wheeler, public_bus_metro, car_alone, carpool_walk
    housing_type: str = "apartment"         # apartment, independent_house, multistory_flat
    cooking_heating: str = "lpg_gas"        # lpg_gas, induction_electric, biomass_kerosene, wood_coal
    budget_tier: str = "low_cost"           # free, low_cost, equipment_ready
    vulnerable_members: List[str] = field(default_factory=list) # children, seniors, asthma, pregnant
    time_of_day: str = "morning"            # morning, afternoon, evening, night

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class RoutineItem:
    time_window: str
    title: str
    description: str
    action_category: str  # ventilation, commute, physical_activity, indoor_habits
    direct_impact: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class IAQHackItem:
    title: str
    cost_tier: str       # Free, Low-Cost (< $15), Equipment-Ready
    materials_needed: str
    implementation_steps: str
    direct_impact: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class SustainableAlternativeItem:
    title: str
    scope: str           # Household, Neighborhood/Community
    replaces_activity: str
    direct_impact: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DirectImpactItem:
    action: str
    physical_mechanism: str
    exposure_reduction: str
    avoided_emissions: str
    community_benefit: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class RiskSummary:
    severity_tier: str
    aqi: int
    pm2_5: float
    health_warning: str
    priority_actions: List[str]
    non_medical_disclaimer: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class RecommendationResponse:
    risk_summary: RiskSummary
    daily_routines: List[RoutineItem]
    iaq_hacks: List[IAQHackItem]
    sustainable_alternatives: List[SustainableAlternativeItem]
    direct_impacts: List[DirectImpactItem]
    generated_by: str = "deterministic_engine"
    cached: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_summary": self.risk_summary.to_dict(),
            "daily_routines": [r.to_dict() for r in self.daily_routines],
            "iaq_hacks": [h.to_dict() for h in self.iaq_hacks],
            "sustainable_alternatives": [s.to_dict() for s in self.sustainable_alternatives],
            "direct_impacts": [d.to_dict() for d in self.direct_impacts],
            "generated_by": self.generated_by,
            "cached": self.cached
        }
