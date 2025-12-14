"""Load and parse credit card data"""
import json
from typing import List, Dict, Optional
from pathlib import Path
from src.models.card import CreditCard
from src.config import CARDS_JSON_PATH

class CardLoader:
    """Loads credit card data from JSON"""
    
    def __init__(self, json_path: Optional[Path] = None):
        self.json_path = json_path or CARDS_JSON_PATH
        self._cards_cache = None
    
    def load_cards(self) -> List[Dict]:
        """Load cards from JSON file as dictionaries"""
        if self._cards_cache is None:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self._cards_cache = json.load(f)
        return self._cards_cache
    
    def load_cards_as_models(self) -> List[CreditCard]:
        """Load cards as Pydantic models"""
        cards_data = self.load_cards()
        return [CreditCard(**card) for card in cards_data]
    
    def get_card_by_id(self, card_id: str) -> Optional[Dict]:
        """Get specific card by ID"""
        cards = self.load_cards()
        return next((c for c in cards if c['card_id'] == card_id), None)
    
    def get_cards_by_issuer(self, issuer: str) -> List[Dict]:
        """Get all cards from a specific issuer"""
        cards = self.load_cards()
        return [c for c in cards if c['issuer'].lower() == issuer.lower()]
    
    def get_cards_by_rewards_type(self, rewards_type: str) -> List[Dict]:
        """Get all cards of a specific rewards type"""
        cards = self.load_cards()
        return [c for c in cards if c['rewards_type'].lower() == rewards_type.lower()]
    
    def filter_by_annual_fee(self, max_fee: float) -> List[Dict]:
        """Filter cards by maximum annual fee"""
        cards = self.load_cards()
        return [c for c in cards if c['annual_fee'] <= max_fee]
    
    def filter_by_credit_score(self, credit_tier: str) -> List[Dict]:
        """Filter cards by credit score requirement"""
        cards = self.load_cards()
        # For now, all cards accept good-excellent, so return all
        # In future, could add more sophisticated filtering
        return cards
