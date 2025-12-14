"""Create text chunks from credit card data for embedding"""
from typing import List, Dict

class CardTextChunker:
    """Creates rich text representations of cards for embedding"""
    
    def create_chunk_for_card(self, card: Dict) -> str:
        """Create a single text chunk for a card"""
        
        # Start with basic info
        chunk = f"{card['card_name']} by {card['issuer']}. "
        
        # Add description
        chunk += f"{card['description']} "
        
        # Add rewards information in natural language
        rewards = card['rewards']
        high_rewards = {cat: rate for cat, rate in rewards.items() if rate > 2.0}
        if high_rewards:
            chunk += "This card offers enhanced rewards: "
            for category, rate in high_rewards.items():
                chunk += f"{rate}x points on {category}, "
            chunk = chunk.rstrip(", ") + ". "
        
        # Add annual fee info
        if card['annual_fee'] == 0:
            chunk += "No annual fee. "
        else:
            chunk += f"${card['annual_fee']} annual fee. "
        
        # Add special features
        if card['special_features']:
            chunk += "Special features include: " + ", ".join(card['special_features']) + ". "
        
        # Add annual credits
        if card['annual_credits']:
            credits_text = ", ".join([c['name'] for c in card['annual_credits']])
            chunk += f"Annual credits: {credits_text}. "
        
        # Add foreign transaction fee info
        if card['foreign_transaction_fee'] == 0:
            chunk += "No foreign transaction fees. "
        
        # Add best for categories
        if card['best_for']:
            chunk += f"Best for: {', '.join(card['best_for'])}. "
        
        # Add rewards type
        chunk += f"Rewards type: {card['rewards_type']}."
        
        return chunk
    
    def create_chunks(self, cards: List[Dict]) -> List[Dict]:
        """Create text chunks for all cards with metadata"""
        chunks = []
        for card in cards:
            chunks.append({
                'card_id': card['card_id'],
                'card_name': card['card_name'],
                'text': self.create_chunk_for_card(card),
                'metadata': {
                    'issuer': card['issuer'],
                    'rewards_type': card['rewards_type'],
                    'annual_fee': card['annual_fee']
                }
            })
        return chunks
