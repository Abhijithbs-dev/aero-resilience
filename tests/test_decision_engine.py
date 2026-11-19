"""
Unit tests for Deterministic Decision Engine, personas, and impact calculations.
"""
import unittest
from backend.models.schemas import AirQualityContext, HouseholdProfile
from backend.services.decision_engine import DecisionEngine

class TestDecisionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DecisionEngine()

    def test_persona_parent_with_children_in_severe_smog(self):
        """P1: Parent with young children navigating severe winter smog."""
        aqi_ctx = AirQualityContext(
            location="Delhi",
            aqi=420,
            pm2_5=285.0,
            severity_tier="Severe"
        )
        profile = HouseholdProfile(
            commute_mode="carpool_walk",
            housing_type="apartment",
            cooking_heating="lpg_gas",
            budget_tier="low_cost",
            vulnerable_members=["children"],
            time_of_day="morning"
        )

        res = self.engine.generate_recommendations(aqi_ctx, profile)
        
        # Verify Risk Summary
        self.assertEqual(res.risk_summary.severity_tier, "Severe")
        self.assertIn("Children", res.risk_summary.health_warning)
        self.assertIn("non-medical", res.risk_summary.non_medical_disclaimer.lower())

        # Verify Routines
        self.assertTrue(len(res.daily_routines) >= 3)
        morning_routine = res.daily_routines[0]
        self.assertIn("Inversion", morning_routine.title)

        # Verify IAQ Hacks include low-cost / free
        self.assertTrue(len(res.iaq_hacks) >= 3)
        titles = [h.title for h in res.iaq_hacks]
        self.assertTrue(any("Corsi-Rosenthal" in t for t in titles))
        self.assertTrue(any("Mopping" in t for t in titles))

        # Verify Direct Impacts
        self.assertTrue(len(res.direct_impacts) >= 3)
        for impact in res.direct_impacts:
            self.assertTrue(len(impact.physical_mechanism) > 10)
            self.assertTrue(len(impact.exposure_reduction) > 5)

    def test_persona_budget_renter_commuter(self):
        """P3: Budget-conscious commuter using two-wheeler with free budget."""
        aqi_ctx = AirQualityContext(
            location="Lahore",
            aqi=280,
            pm2_5=160.0,
            severity_tier="Very Poor"
        )
        profile = HouseholdProfile(
            commute_mode="two_wheeler",
            housing_type="apartment",
            cooking_heating="lpg_gas",
            budget_tier="free",
            vulnerable_members=[],
            time_of_day="morning"
        )

        res = self.engine.generate_recommendations(aqi_ctx, profile)
        
        # Verify commute advice addresses two-wheeler and N95
        commute_routine = [r for r in res.daily_routines if r.action_category == "commute"]
        self.assertTrue(len(commute_routine) > 0)
        self.assertIn("N95", commute_routine[0].description)

        # Direct impact contains commute savings
        commute_impacts = [d for d in res.direct_impacts if "Two-Wheeler" in d.action or "Commute" in d.action]
        self.assertTrue(len(commute_impacts) > 0)
        self.assertIn("inhalation", commute_impacts[0].exposure_reduction.lower())

    def test_persona_multigenerational_asthma(self):
        """P2: Senior / asthma vulnerable resident in high smog."""
        aqi_ctx = AirQualityContext(
            location="Kathmandu",
            aqi=190,
            pm2_5=95.0,
            severity_tier="Poor"
        )
        profile = HouseholdProfile(
            commute_mode="public_bus_metro",
            housing_type="independent_house",
            cooking_heating="biomass_kerosene",
            budget_tier="equipment_ready",
            vulnerable_members=["seniors", "asthma"]
        )

        res = self.engine.generate_recommendations(aqi_ctx, profile)
        self.assertIn("Asthma", res.risk_summary.health_warning)

        # Sustainable alternatives should address biomass heating
        alts = [s.title for s in res.sustainable_alternatives]
        self.assertTrue(any("Biomass" in a or "Clean Electric" in a for a in alts))

if __name__ == "__main__":
    unittest.main()
