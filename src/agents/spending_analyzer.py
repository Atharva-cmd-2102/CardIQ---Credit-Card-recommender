"""Spending Analyzer Agent - Analyzes user spending patterns"""
import json
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.user_input import UserProfile
from src.models.agent_outputs import SpendingAnalysis
from src.prompts import SPENDING_ANALYZER_SYSTEM_PROMPT
from src.utils.calculations import calculate_spending_percentages

class SpendingAnalyzerAgent(BaseAgent):
    """Agent that analyzes user spending patterns"""
    
    def get_system_prompt(self) -> str:
        return SPENDING_ANALYZER_SYSTEM_PROMPT
    
    def process(self, user_profile: UserProfile) -> SpendingAnalysis:
        """Analyze user spending and return insights"""
        
        # Prepare spending data
        spending_dict = user_profile.monthly_spending.model_dump()
        
        # Create user message
        user_message = self._create_user_message(spending_dict, user_profile.credit_score)
        
        # Call Haiku (fast and cheap for calculations)
        response = self._call_llm(user_message, use_sonnet=False, max_tokens=1500)
        
        # Parse JSON response
        analysis_data = self._parse_response(response)
        
        # Create and return SpendingAnalysis model
        return SpendingAnalysis(**analysis_data)
    
    def _create_user_message(self, spending: Dict[str, float], credit_score: str) -> str:
        """Create user message for LLM"""
        message = f"""Analyze this user's monthly spending pattern:

Monthly Spending:
{json.dumps(spending, indent=2)}

Credit Score: {credit_score}

Please provide a comprehensive analysis in JSON format with:
1. total_monthly_spend (sum of all spending)
2. total_annual_spend (monthly × 12)
3. top_categories (top 2-3 categories by spend)
4. spending_profile (descriptive label like "dining_focused", "travel_enthusiast", etc.)
5. category_percentages (percentage of total for each category)
6. insights (list of 2-3 key observations)

Output ONLY valid JSON, no other text."""
        
        return message
    
    def _parse_response(self, response: str) -> Dict:
        """Parse LLM response into dict"""
        try:
            # Try to parse as JSON directly
            return json.loads(response)
        except json.JSONDecodeError:
            # If wrapped in markdown, extract JSON
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            else:
                raise ValueError(f"Could not parse response as JSON: {response[:200]}")
