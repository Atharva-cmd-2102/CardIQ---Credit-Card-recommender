"""Recommendation Synthesizer Agent - Creates personalized recommendations"""
import json
from typing import List
from src.agents.base_agent import BaseAgent
from src.models.agent_outputs import (
    SpendingAnalysis,
    CardEvaluations,
    RecommendationOutput,
    Recommendation
)
from src.prompts import RECOMMENDATION_SYNTHESIZER_SYSTEM_PROMPT
from src.data.card_loader import CardLoader
from src.rag.retriever import CardRetriever

class RecommendationSynthesizerAgent(BaseAgent):
    """Agent that creates personalized card recommendations"""
    
    def __init__(self, claude_client=None):
        super().__init__(claude_client)
        self.card_loader = CardLoader()
        # RAG retriever for getting card details
        try:
            self.retriever = CardRetriever()
        except:
            # If vector DB not built yet, just use card loader
            self.retriever = None
    
    def get_system_prompt(self) -> str:
        return RECOMMENDATION_SYNTHESIZER_SYSTEM_PROMPT
    
    def process(
        self,
        spending_analysis: SpendingAnalysis,
        card_evaluations: CardEvaluations,
        user_profile
    ) -> RecommendationOutput:
        """Create personalized recommendations for top 3 cards"""
        
        # Get top 3 cards
        top_3_evaluations = card_evaluations.top_cards[:3]
        
        recommendations = []
        
        for rank, evaluation in enumerate(top_3_evaluations, 1):
            # Get full card details
            card = self.card_loader.get_card_by_id(evaluation.card_id)
            
            # Get additional context via RAG if available
            rag_context = self._get_rag_context(card) if self.retriever else ""
            
            # Create user message
            user_message = self._create_user_message(
                rank=rank,
                spending_analysis=spending_analysis,
                evaluation=evaluation,
                card=card,
                rag_context=rag_context
            )
            
            # Call Sonnet for high-quality explanations
            response = self._call_llm(user_message, use_sonnet=True, max_tokens=3000)
            
            # Parse response
            recommendation_data = self._parse_response(response)
            
            # Add rank and card info
            recommendation_data['rank'] = rank
            recommendation_data['card_id'] = card['card_id']
            recommendation_data['card_name'] = card['card_name']
            
            # Add financial summary
            recommendation_data['financial_summary'] = {
                'year_1_value': evaluation.net_value_year_1,
                'year_2_value': evaluation.net_value_year_2,
                'year_3_value': evaluation.net_value_year_3,
                'annual_rewards': evaluation.annual_rewards,
                'annual_fee': evaluation.annual_fee,
                'signup_bonus': evaluation.signup_bonus_value
            }
            
            recommendations.append(Recommendation(**recommendation_data))
        
        # Create portfolio strategy
        portfolio_strategy = self._create_portfolio_strategy(recommendations, spending_analysis)
        
        return RecommendationOutput(
            recommendations=recommendations,
            portfolio_strategy=portfolio_strategy
        )
    
    def _get_rag_context(self, card: dict) -> str:
        """Get additional context via RAG"""
        if not self.retriever:
            return ""
        
        try:
            # Search for cards with similar features
            query = f"{card['card_name']} benefits features"
            results = self.retriever.search(query, k=1)
            if results:
                return f"Additional context: {results[0].get('description', '')}"
        except:
            pass
        
        return ""
    
    def _create_user_message(
        self,
        rank: int,
        spending_analysis: SpendingAnalysis,
        evaluation,
        card: dict,
        rag_context: str
    ) -> str:
        """Create user message for LLM"""
        
        message = f"""Create a personalized recommendation for this credit card:

CARD: {card['card_name']}
RANK: #{rank}

USER SPENDING PROFILE:
- Total Monthly Spend: ${spending_analysis.total_monthly_spend:,.2f}
- Top Categories: {', '.join(spending_analysis.top_categories)}
- Spending Profile: {spending_analysis.spending_profile}
- Key Insights: {'; '.join(spending_analysis.insights)}

CARD DETAILS:
- Issuer: {card['issuer']}
- Annual Fee: ${card['annual_fee']}
- Rewards Type: {card['rewards_type']}
- Description: {card['description']}

REWARDS STRUCTURE:
{json.dumps(card['rewards'], indent=2)}

SPECIAL FEATURES:
{json.dumps(card['special_features'], indent=2)}

ANNUAL CREDITS:
{json.dumps(card.get('annual_credits', []), indent=2)}

FINANCIAL VALUE:
- Annual Rewards: ${evaluation.annual_rewards:,.2f}
- Signup Bonus: ${evaluation.signup_bonus_value:,.2f}
- Year 1 Net Value: ${evaluation.net_value_year_1:,.2f}
- Year 2 Net Value: ${evaluation.net_value_year_2:,.2f}
- Year 3 Net Value: ${evaluation.net_value_year_3:,.2f}

{rag_context}

Create a JSON response with:
1. why_this_card: Personalized explanation (2-3 sentences) connecting their spending to card benefits
2. how_to_maximize: List of 3-5 specific strategies
3. watch_out_for: List of 2-3 warnings about fees/restrictions
4. optimization_strategy: Dict with:
   - use_this_card_for: list of categories
   - pair_with: suggestion for complementary card
   - avoid_using_for: list of categories
5. long_term_projection: Dict with:
   - one_year: string description
   - two_years: string description
   - three_years: string description

Output ONLY valid JSON."""
        
        return message
    
    def _create_portfolio_strategy(self, recommendations: List[Recommendation], spending_analysis: SpendingAnalysis) -> str:
        """Create overall portfolio strategy"""
        
        if len(recommendations) < 2:
            return f"Use {recommendations[0].card_name} as your primary card for all spending."
        
        top_card = recommendations[0].card_name
        second_card = recommendations[1].card_name if len(recommendations) > 1 else None
        
        strategy = f"Recommended strategy: Use {top_card} as your primary card"
        
        if second_card:
            strategy += f", paired with {second_card} for categories where it offers better rewards. "
            strategy += f"This combination optimizes your {spending_analysis.spending_profile} spending pattern."
        
        return strategy
    
    def _parse_response(self, response: str) -> dict:
        """Parse LLM response into dict"""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Handle markdown-wrapped JSON
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            else:
                raise ValueError(f"Could not parse response as JSON: {response[:200]}")
