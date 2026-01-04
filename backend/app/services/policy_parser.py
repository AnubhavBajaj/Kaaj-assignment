import re
from typing import Dict, Any, List, Optional
from app.models.lender import CriteriaType

class PolicyParser:
    """
    Parses extracted text from PDF into structured lender policy data.
    """

    def parse_policy(self, lender_name: str, text: str) -> Dict[str, Any]:
        """
        Routes parsing to the specific lender's parser method.
        """
        # Try to match by name hint first
        name_lower = lender_name.lower()
        if "stearns" in name_lower:
            return self._parse_stearns_bank(text)
        elif "apex" in name_lower:
            return self._parse_apex_commercial(text)
        elif "advantage" in name_lower:
            return self._parse_advantage_plus(text)
        elif "citizens" in name_lower:
            return self._parse_citizens_bank(text)
        elif "falcon" in name_lower:
            return self._parse_falcon_equipment(text)
        
        # Fallback: check text content
        text_lower = text.lower()
        if "stearns bank" in text_lower:
            return self._parse_stearns_bank(text)
        elif "apex commercial" in text_lower:
             return self._parse_apex_commercial(text)
             
        return {"error": f"No parser available for lender: {lender_name}"}

    def _extract_value(self, pattern: str, text: str, type_cast: type = str) -> Optional[Any]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val = match.group(1).strip()
            if type_cast == float:
                return float(re.sub(r'[^0-9.]', '', val))
            elif type_cast == int:
                return int(re.sub(r'[^0-9]', '', val))
            return val
        return None

    def _parse_stearns_bank(self, text: str) -> Dict[str, Any]:
        programs = []
        
        # Parse Tier 1
        programs.append({
            "program_name": "Standard Program",
            "tier_name": "Tier 1",
            "criteria": [
                {"type": CriteriaType.FICO_MIN, "value_numeric": 700},
                {"type": CriteriaType.PAYNET_MIN, "value_numeric": 650},
                {"type": CriteriaType.TIB_MIN, "value_numeric": 2.0}, # Years
            ]
        })

        # Parse Excluded Industries
        excluded_industries = []
        if "Excluded Industries" in text:
            # Simplified logic - in reality would extract list
            excluded_industries = ["Adult Entertainment", "Gambling", "Cannabis"]

        return {
            "lender_name": "Stearns Bank",
            "programs": programs,
            "excluded_industries": excluded_industries,
            "excluded_states": []
        }

    def _parse_apex_commercial(self, text: str) -> Dict[str, Any]:
        programs = []
        # Logic for A/B/C rates would go here based on text analysis
        programs.append({
            "program_name": "Commercial Program",
            "tier_name": "A Credit",
            "criteria": [
                 {"type": CriteriaType.FICO_MIN, "value_numeric": 650},
                 {"type": CriteriaType.TIB_MIN, "value_numeric": 2.0}
            ]
        })
        
        excluded_states = []
        if re.search(r"CA.*NV.*ND.*VT", text):
             excluded_states = ["CA", "NV", "ND", "VT"]

        return {
            "lender_name": "Apex Commercial Capital",
            "programs": programs,
            "excluded_industries": ["Trucking", "Restaurants"], # Placeholder
            "excluded_states": excluded_states
        }

    def _parse_advantage_plus(self, text: str) -> Dict[str, Any]:
        programs = []
        programs.append({
            "program_name": "General Financing",
            "tier_name": "Standard",
            "criteria": [
                 {"type": CriteriaType.FICO_MIN, "value_numeric": 680},
                 {"type": CriteriaType.COMPARABLE_CREDIT_PERCENT, "value_numeric": 80},
            ]
        })
        
        return {
            "lender_name": "Advantage+ Financing",
            "programs": programs,
            "excluded_industries": [],
            "excluded_states": []
        }

    def _parse_citizens_bank(self, text: str) -> Dict[str, Any]:
         # Validating Citizens logic
        programs = []
        programs.append({
            "program_name": "Equipment Finance",
            "tier_name": "Tier A",
            "criteria": [
                 {"type": CriteriaType.FICO_MIN, "value_numeric": 720},
            ]
        })
        return {
            "lender_name": "Citizens Bank",
            "programs": programs,
            "excluded_industries": [],
            "excluded_states": []
        }

    def _parse_falcon_equipment(self, text: str) -> Dict[str, Any]:
        programs = []
        programs.append({
            "program_name": "Falcon Standard",
            "tier_name": "A",
            "criteria": [
                 {"type": CriteriaType.TIB_MIN, "value_numeric": 3.0},
            ]
        })
        return {
            "lender_name": "Falcon Equipment Finance",
            "programs": programs,
            "excluded_industries": [],
            "excluded_states": []
        }

# Standalone helpers for direct usage
def parse_stearns_bank(text: str) -> Dict[str, Any]:
    return PolicyParser()._parse_stearns_bank(text)

def parse_apex_commercial(text: str) -> Dict[str, Any]:
    return PolicyParser()._parse_apex_commercial(text)


