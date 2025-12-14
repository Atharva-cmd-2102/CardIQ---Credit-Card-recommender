"""Card Evaluator Agent - Calculates financial value of cards"""
import json
from typing import List, Dict
from src.agents.base_agent import BaseAgent
from src.models.agent_outputs import SpendingAnalysis, CardEvaluations, CardEvaluation
from src.prompts import CARD_EVALUATOR_SYSTEM_PROMPT
from src.data.card_loader import CardLoader
from src.utils.calculations import (
    calculate_category_rewards,
    calculate_total_annual_credits,
    calculate_net_value
)

class CardEvaluatorAgent(BaseAgent):
    """Agent that evaluates and ranks credit cards"""
    
    def __init__(self, claude_client=None):
        super().__init__(claude_client)
        self.card_loader = CardLoader()
    
    def get_system_prompt(self) -> str:
        return CARD_EVALUATOR_SYSTEM_PROMPT
    
    def process(self, spending_analysis: SpendingAnalysis, user_profile) -> CardEvaluations:
        """Evaluate all cards and return top ranked cards"""
        
        # Load all cards
        all_cards = self.card_loader.load_cards()
        
        # Filter by user preferences if specified
        eligible_cards = self._filter_cards(all_cards, user_profile)
        
        # Calculate value for each card
        evaluations = []
        for card in eligible_cards:
            eval_result = self._evaluate_single_card(card, spending_analysis, user_profile)
            evaluations.append(eval_result)

        # Sort by blended score that balances short-term and long-term value
        # This prevents high signup bonuses from always dominating recommendations
        # Formula: (Year_1 * 0.3) + (Year_2 * 0.4) + (Year_3 * 0.3)
        # This gives more weight to Year 2 (ongoing value without signup bonus)
        evaluations.sort(key=lambda x: (x.net_value_year_1 * 0.3 +
                                        x.net_value_year_2 * 0.4 +
                                        x.net_value_year_3 * 0.3),
                        reverse=True)

        # Return top 5
        top_cards = evaluations[:5]
        
        return CardEvaluations(
            top_cards=top_cards,
            total_cards_evaluated=len(evaluations)
        )
    
    def _filter_cards(self, cards: List[Dict], user_profile) -> List[Dict]:
        """Filter cards based on user preferences"""
        filtered = cards
        
        # Filter by max annual fee if specified
        if user_profile.max_annual_fee is not None:
            filtered = [c for c in filtered if c['annual_fee'] <= user_profile.max_annual_fee]
        
        # Filter by rewards type if specified
        if user_profile.preferred_rewards_type:
            filtered = [c for c in filtered if c['rewards_type'].lower() == user_profile.preferred_rewards_type.lower()]
        
        return filtered
    
    def _evaluate_single_card(self, card: Dict, spending_analysis: SpendingAnalysis, user_profile) -> CardEvaluation:
        """Calculate value for a single card"""
        
        # Get monthly spending as dict
        spending_dict = user_profile.monthly_spending.model_dump()
        
        # Calculate annual rewards
        annual_rewards = calculate_category_rewards(
            monthly_spending=spending_dict,
            card_rewards=card['rewards'],
            point_value=card['point_value']
        )
        
        # Get signup bonus value
        signup_bonus_value = card['signup_bonus'].get('estimated_value') or 0
        if signup_bonus_value is None:
            signup_bonus_value = 0
        # Convert to float if it's a string
        signup_bonus_value = float(signup_bonus_value)
        
        # Calculate annual credits value
        annual_credits_value = calculate_total_annual_credits(card.get('annual_credits', []))
        
        # Get annual fee
        annual_fee = float(card['annual_fee'])
        
        # Calculate net values
        net_value_year_1 = calculate_net_value(
            annual_rewards=annual_rewards,
            signup_bonus_value=signup_bonus_value,
            annual_fee=annual_fee,
            annual_credits_value=annual_credits_value,
            year=1
        )
        
        net_value_year_2 = calculate_net_value(
            annual_rewards=annual_rewards,
            signup_bonus_value=signup_bonus_value,
            annual_fee=annual_fee,
            annual_credits_value=annual_credits_value,
            year=2
        )
        
        net_value_year_3 = calculate_net_value(
            annual_rewards=annual_rewards,
            signup_bonus_value=signup_bonus_value,
            annual_fee=annual_fee,
            annual_credits_value=annual_credits_value,
            year=3
        )
        
        # Calculate blended ranking score: Year 1 (30%) + Year 2 (40%) + Year 3 (30%)
        # This balances signup bonuses with long-term value
        blended_score = (net_value_year_1 * 0.3) + (net_value_year_2 * 0.4) + (net_value_year_3 * 0.3)

        return CardEvaluation(
            card_id=card['card_id'],
            card_name=card['card_name'],
            annual_rewards=round(annual_rewards, 2),
            signup_bonus_value=round(signup_bonus_value, 2),
            annual_fee=annual_fee,
            annual_credits_value=round(annual_credits_value, 2),
            net_value_year_1=round(net_value_year_1, 2),
            net_value_year_2=round(net_value_year_2, 2),
            net_value_year_3=round(net_value_year_3, 2),
            ranking_score=round(blended_score, 2)  # Use blended score for ranking
        )
