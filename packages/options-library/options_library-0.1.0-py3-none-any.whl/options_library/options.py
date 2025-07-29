# options_library.py

class Put:
    """Represents a Put option with a strike price and premium."""
    def __init__(self, strike: float, premium: float):
        self.strike = strike
        self.premium = premium
    
    def breakeven(self):
        return {"breakeven": self.strike - self.premium}
    
    def payoff(self, spot: float):
        if spot <= self.strike:
            return {"payoff_net_of_premium": self.strike - spot - self.premium,
                    "payoff_without_premium": self.strike - spot}
        else:
            return {"payoff_net_of_premium": -self.premium,
                    "payoff_without_premium": 0}

class Call:
    """Represents a Call option with a strike price and premium."""
    def __init__(self, strike: float, premium: float):
        self.strike = strike
        self.premium = premium
    
    def breakeven(self):
        return {"breakeven": self.strike + self.premium}
    
    def payoff(self, spot: float):
        if spot >= self.strike:
            return {"payoff_net_of_premium": spot - self.strike - self.premium,
                    "payoff_without_premium": spot - self.strike}
        else:
            return {"payoff_net_of_premium": -self.premium,
                    "payoff_without_premium": 0}

# Define other classes like Straddle and Bullcall similarly