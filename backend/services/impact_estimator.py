"""
Impact Estimator: Transparent, assumption-documented scientific calculations
for personal exposure reduction and avoided household/community emissions.
"""
from typing import Dict, Any, List
from backend.models.schemas import DirectImpactItem

class ImpactEstimator:
    """
    Computes transparent physical impacts based on published aerosol physics
    and urban emission factors (EPA, WHO, Central Pollution Control Board).
    """

    @staticmethod
    def calculate_commute_impact(commute_mode: str, round_trip_km: float = 18.0) -> Dict[str, Any]:
        """
        Calculates avoided CO2e and tailpipe particulate emissions when shifting
        from solitary personal car/two-wheeler to public transit or carpooling.
        """
        # Emission factors (approx grams per passenger-km)
        # Solo Car: ~160g CO2e/km, ~0.08g PM2.5/km
        # Two Wheeler: ~70g CO2e/km, ~0.12g PM2.5/km
        # Metro / Electric Bus: ~25g CO2e/km, ~0.005g PM2.5/km
        # Carpool (3 riders): ~55g CO2e/km, ~0.027g PM2.5/km

        if commute_mode == "car_alone":
            avoided_co2e_kg = round((160 - 25) * round_trip_km / 1000.0, 2)
            avoided_pm_g = round((0.08 - 0.005) * round_trip_km, 2)
            return {
                "action": "Shift from Solo Car to Metro / Public Bus",
                "physical_mechanism": "Eliminates single-occupancy internal combustion tailpipe emissions in congested surface traffic where idling multiplies particulate output by 3x.",
                "exposure_reduction": "25% lower in-cabin PM2.5 exposure by avoiding surface exhaust inhalation plumes.",
                "avoided_emissions": f"{avoided_co2e_kg} kg CO2e and {avoided_pm_g}g tailpipe PM2.5 avoided per round trip.",
                "community_benefit": f"Prevents {avoided_co2e_kg} kg of greenhouse gas and local street-level toxic soot deposition in your neighborhood airshed."
            }
        elif commute_mode == "two_wheeler":
            avoided_co2e_kg = round((70 - 25) * round_trip_km / 1000.0, 2)
            avoided_pm_g = round((0.12 - 0.005) * round_trip_km, 2)
            return {
                "action": "Shift from Two-Wheeler to Enclosed Public Transit on High Smog Days",
                "physical_mechanism": "Two-wheelers directly inhale roadway micro-environments where PM2.5 and black carbon concentrations are 400% higher than ambient background.",
                "exposure_reduction": "60%–75% personal particulate inhalation reduction compared to riding in open traffic.",
                "avoided_emissions": f"{avoided_co2e_kg} kg CO2e and {avoided_pm_g}g tailpipe PM2.5 avoided per round trip.",
                "community_benefit": "Reduces high-emitting 2-stroke/small-engine cold-start emissions during winter morning temperature inversions."
            }
        else:
            return {
                "action": "Maintain Low-Emission Commute & Carpool Optimization",
                "physical_mechanism": "High passenger-density transit minimizes per-capita primary combustion products.",
                "exposure_reduction": "Avoids high-density traffic exhaust pockets.",
                "avoided_emissions": "1.5–2.0 kg CO2e saved daily relative to individual private vehicle usage.",
                "community_benefit": "Reduces urban road congestion and localized brake-wear particulate resuspension."
            }

    @staticmethod
    def calculate_iaq_hacks_impact(budget_tier: str, base_pm25: float) -> List[DirectImpactItem]:
        """
        Quantifies the particulate reduction mechanism of indoor air interventions.
        """
        items: List[DirectImpactItem] = []

        # 1. Wet Mopping vs Dry Sweeping (Free)
        items.append(DirectImpactItem(
            action="Wet Mopping & Damp Microfiber Dusting (vs. Dry Sweeping)",
            physical_mechanism="Dry broom bristles impart aerodynamic shear forces that aerosolize coarse dust and settled PM2.5 back into breathing zones for 2–4 hours. Damp wiping traps particles via liquid surface tension.",
            exposure_reduction="Reduces indoor airborne dust re-suspension by 65%–80% within 15 minutes.",
            avoided_emissions="Zero secondary chemical VOCs when using clean warm water without synthetic aerosol sprays.",
            community_benefit="Zero electrical power consumption; completely accessible to all housing tiers."
        ))

        # 2. Door & Window Draft Sealing (Low-Cost)
        infiltration_drop = 60
        new_indoor_estimate = round(base_pm25 * (1 - (infiltration_drop / 100.0)), 1)
        items.append(DirectImpactItem(
            action="Door Draft Sweeps & Rolled-Towel Sash Sealing",
            physical_mechanism="Reduces building envelope Air Changes per Hour (ACH) from leaky infiltration (~0.8 ACH) down to sealed state (~0.25 ACH), halting fine particle pressure infiltration.",
            exposure_reduction=f"Cuts outdoor-to-indoor particle penetration by ~{infiltration_drop}%, preventing indoor PM2.5 from tracking outdoor spikes (estimated drop from {base_pm25} to ~{new_indoor_estimate} ug/m3).",
            avoided_emissions="Preserves indoor thermal energy, lowering room heating electricity or gas fuel burn by 12%–18%.",
            community_benefit="Inexpensive, non-destructive retrofit ideal for renters and low-income families."
        ))

        # 3. DIY Corsi-Rosenthal Box / HEPA Purifier (Low-Cost / Equipment)
        if budget_tier in ["low_cost", "equipment_ready"]:
            items.append(DirectImpactItem(
                action="DIY Corsi-Rosenthal Box Air Cleaner (Box Fan + MERV-13 Filters)",
                physical_mechanism="High-volume mechanical filtration uses impaction, interception, and Brownian diffusion across pleated electrostatic fibers, achieving Clean Air Delivery Rate (CADR) of 200–250 CFM at 1/5th the cost of commercial units.",
                exposure_reduction="Clears 85%–90% of indoor PM2.5 within 40 minutes in a standard 300 sq.ft living or bedroom area.",
                avoided_emissions="Energy-efficient 55W fan draws less electricity than a standard incandescent light bulb.",
                community_benefit="Open-source, DIY design empowering schools, neighborhood centers, and households with affordable clean air."
            ))

        # 4. Combustion Cessation (Incense, Coils, Biomass)
        items.append(DirectImpactItem(
            action="Eliminating Indoor Incense, Mosquito Coils & Unvented Solid Fuels",
            physical_mechanism="Incense and mosquito coils undergo smoldering incomplete combustion, releasing ultrafine carbon soot and benzene-ring compounds directly into unventilated rooms.",
            exposure_reduction="Prevents extreme indoor PM2.5 surges of 200–450 ug/m3 (equivalent to passive exposure from 75–100 cigarettes per coil burned).",
            avoided_emissions="Averts toxic polycyclic aromatic hydrocarbons (PAHs) and carbon monoxide indoors.",
            community_benefit="Protects vulnerable infants and elderly respiratory tracts from deep alveolar inflammation."
        ))

        return items

    @staticmethod
    def calculate_routine_inversion_impact(time_of_day: str) -> Dict[str, Any]:
        """
        Explains diurnal atmospheric boundary layer inversion impact.
        """
        return {
            "action": "Diurnal Inversion Timing: Reschedule Outdoor Exposure to 12:00–16:00",
            "physical_mechanism": "Radiative nocturnal cooling traps heavy cold air and surface emissions under a thermal lid near ground level (05:00–09:30). Solar heating between noon and 16:00 expands the atmospheric boundary layer by 300%–500%, diluting ambient pollutant concentrations.",
            "exposure_reduction": "Reduces personal active inhalation exposure by 40%–60% compared to early morning outdoor exertion.",
            "avoided_emissions": "Reduces cold-start idling pollution spikes during early morning commute rush hours.",
            "community_benefit": "Shifts community errands and deliveries to windows of natural atmospheric dispersion."
        }
