"""Pydantic models for user input"""
from pydantic import BaseModel, Field
from typing import Optional

class MonthlySpending(BaseModel):
    """User's monthly spending by category"""
    dining: float = Field(ge=0, description="Monthly dining spend")
    groceries: float = Field(ge=0, description="Monthly grocery spend")
    travel: float = Field(ge=0, description="Monthly travel spend")
    gas: float = Field(ge=0, description="Monthly gas spend")
    streaming: float = Field(ge=0, description="Monthly streaming spend")
    other: float = Field(ge=0, description="Monthly other spend")
    
    # Optional detailed categories
    flights: Optional[float] = Field(default=0, ge=0)
    hotels: Optional[float] = Field(default=0, ge=0)
    transit: Optional[float] = Field(default=0, ge=0)

class UserProfile(BaseModel):
    """Complete user profile for recommendations"""
    monthly_spending: MonthlySpending
    credit_score: str = Field(
        pattern="^(excellent|good|fair)$",
        description="User's credit score tier"
    )
    max_annual_fee: Optional[int] = Field(
        default=None, 
        ge=0,
        description="Maximum acceptable annual fee"
    )
    preferred_rewards_type: Optional[str] = Field(
        default=None,
        description="Preferred type of rewards (cash_back, travel, flexible_points)"
    )
    planning_to_travel: Optional[bool] = Field(
        default=False,
        description="Whether user plans to travel internationally"
    )
