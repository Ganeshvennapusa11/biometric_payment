import json
import os

def calculate_risk_score(sender_folder, amount):
    """
    Analyzes transaction risk using historical averages.
    Returns: (is_anomaly, risk_level)
    """
    user_file = f"{sender_folder}/user.json"
    
    if not os.path.exists(user_file):
        return False, "Low"

    with open(user_file, 'r') as f:
        data = json.load(f)

    # Get transaction history (if any)
    history = data.get("transactions", [])
    
    if len(history) < 3:
        # Not enough data: use a fixed threshold (e.g., ₹5000)
        if amount > 5000:
            return True, "Medium (New Account High Value)"
        return False, "Low"

    # Calculate Mean of past transactions
    amounts = [t['amount'] for t in history]
    avg_spend = sum(amounts) / len(amounts)
    
    # Logic: If current amount is > 3x the average, it's an anomaly
    if amount > (avg_spend * 3):
        return True, "High (Value Deviation)"
    
    return False, "Low"