"""Main entry point for CardIQ system"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.agents.orchestrator import Orchestrator
from src.models.user_input import UserProfile, MonthlySpending

def main():
    """Run CardIQ recommendation system"""
    
    print("\n" + "=" * 60)
    print("Welcome to CardIQ!")
    print("AI-Powered Credit Card Recommendation System")
    print("=" * 60 + "\n")
    
    # Example user profile - CUSTOMIZE THIS
    user_profile = UserProfile(
        monthly_spending=MonthlySpending(
            dining=1200,
            groceries=200,
            travel=200,
            gas=150,
            streaming=50,
            other=300
        ),
        credit_score="excellent",
        max_annual_fee=500,  # Optional: set max fee
        preferred_rewards_type=None  # Optional: "cash_back", "travel", "flexible_points"
    )
    
    print("📊 Your Spending Profile:")
    print(f"  • Dining: ${user_profile.monthly_spending.dining}")
    print(f"  • Groceries: ${user_profile.monthly_spending.groceries}")
    print(f"  • Travel: ${user_profile.monthly_spending.travel}")
    print(f"  • Gas: ${user_profile.monthly_spending.gas}")
    print(f"  • Streaming: ${user_profile.monthly_spending.streaming}")
    print(f"  • Other: ${user_profile.monthly_spending.other}")
    print(f"  • Credit Score: {user_profile.credit_score}")
    
    # Initialize orchestrator
    orchestrator = Orchestrator()
    
    # Get recommendations
    try:
        result = orchestrator.get_quick_recommendation(user_profile)
        print(result)
        
        # Optionally save to file
        output_path = Path("outputs/recommendations/recommendation.txt")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"\n💾 Recommendation saved to: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
