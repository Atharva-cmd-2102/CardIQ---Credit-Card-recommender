"""Interactive CardIQ - User enters spending via prompts"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.agents.orchestrator import Orchestrator
from src.models.user_input import UserProfile, MonthlySpending

def get_float_input(prompt, default=0):
    """Get float input with default value"""
    while True:
        try:
            value = input(f"{prompt} (default: ${default}): ").strip()
            if value == "":
                return float(default)
            return float(value)
        except ValueError:
            print("Please enter a valid number.")

def get_choice_input(prompt, choices):
    """Get choice from list"""
    while True:
        print(f"\n{prompt}")
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")
        try:
            selection = int(input("Enter number: ").strip())
            if 1 <= selection <= len(choices):
                return choices[selection - 1]
            print(f"Please enter a number between 1 and {len(choices)}")
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("\n" + "=" * 60)
    print("Welcome to CardIQ!")
    print("AI-Powered Credit Card Recommendation System")
    print("=" * 60 + "\n")
    
    print("Let's understand your monthly spending habits.\n")
    
    # Get spending inputs
    dining = get_float_input("Monthly spending on DINING (restaurants, food delivery)", 300)
    groceries = get_float_input("Monthly spending on GROCERIES", 300)
    travel = get_float_input("Monthly spending on TRAVEL (general)", 200)
    gas = get_float_input("Monthly spending on GAS", 150)
    streaming = get_float_input("Monthly spending on STREAMING services", 50)
    other = get_float_input("Monthly spending on OTHER/EVERYTHING ELSE", 500)
    
    # Optional detailed travel
    flights = get_float_input("  └─ Of travel, how much on FLIGHTS specifically?", 0)
    hotels = get_float_input("  └─ Of travel, how much on HOTELS specifically?", 0)
    transit = get_float_input("  └─ Of travel, how much on TRANSIT/rideshare?", 0)
    
    # Get credit score
    credit_score = get_choice_input(
        "What is your credit score tier?",
        ["excellent", "good", "fair"]
    )
    
    # Optional preferences
    print("\n" + "=" * 60)
    print("Optional Preferences (press Enter to skip)")
    print("=" * 60 + "\n")

    max_fee_input = input("Maximum annual fee you're willing to pay (e.g., 100, 500): ").strip()
    max_annual_fee = int(max_fee_input) if max_fee_input else None

    # Get available rewards types from the card database
    from src.data.card_loader import CardLoader
    loader = CardLoader()
    all_cards = loader.load_cards()
    available_types = sorted(set(card['rewards_type'] for card in all_cards))

    print(f"Preferred rewards type (options: {', '.join(available_types)})")
    rewards_type_input = input("  Enter your choice (or press Enter to skip): ").strip()

    # Validate the input
    if rewards_type_input:
        if rewards_type_input.lower() in [rt.lower() for rt in available_types]:
            preferred_rewards_type = rewards_type_input.lower()
        else:
            print(f"  ⚠️  Warning: '{rewards_type_input}' is not a valid rewards type. Ignoring filter.")
            preferred_rewards_type = None
    else:
        preferred_rewards_type = None
    
    # Create user profile
    user_profile = UserProfile(
        monthly_spending=MonthlySpending(
            dining=dining,
            groceries=groceries,
            travel=travel,
            gas=gas,
            streaming=streaming,
            other=other,
            flights=flights,
            hotels=hotels,
            transit=transit
        ),
        credit_score=credit_score,
        max_annual_fee=max_annual_fee,
        preferred_rewards_type=preferred_rewards_type
    )
    
    # Show summary
    total = dining + groceries + travel + gas + streaming + other
    print("\n" + "=" * 60)
    print("Your Spending Summary")
    print("=" * 60)
    print(f"  • Dining: ${dining:,.2f}")
    print(f"  • Groceries: ${groceries:,.2f}")
    print(f"  • Travel: ${travel:,.2f}")
    print(f"  • Gas: ${gas:,.2f}")
    print(f"  • Streaming: ${streaming:,.2f}")
    print(f"  • Other: ${other:,.2f}")
    print(f"  • TOTAL: ${total:,.2f}/month (${total*12:,.2f}/year)")
    print(f"  • Credit Score: {credit_score}")
    if max_annual_fee is not None:
        print(f"  • Max Annual Fee Filter: ${max_annual_fee}")
    if preferred_rewards_type:
        print(f"  • Rewards Type Filter: {preferred_rewards_type}")
    print("=" * 60 + "\n")
    
    proceed = input("Proceed with recommendation? (yes/no): ").strip().lower()
    if proceed not in ['yes', 'y']:
        print("Recommendation cancelled.")
        return
    
    # Get recommendations
    print("\nGenerating personalized recommendations...\n")
    orchestrator = Orchestrator()
    
    try:
        result = orchestrator.get_quick_recommendation(user_profile)
        print(result)
        
        # Save to file
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