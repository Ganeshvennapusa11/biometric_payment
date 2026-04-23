# import json
# import os

# def calculate_risk_score(sender_folder, amount):
#     """
#     Analyzes transaction risk using historical averages.
#     Returns: (is_anomaly, risk_level)
#     """
#     user_file = f"{sender_folder}/user.json"
    
#     if not os.path.exists(user_file):
#         return False, "Low"

#     with open(user_file, 'r') as f:
#         data = json.load(f)

#     # Get transaction history (if any)
#     history = data.get("transactions", [])
    
#     if len(history) < 3:
#         # Not enough data: use a fixed threshold (e.g., ₹5000)
#         if amount > 5000:
#             return True, "Medium (New Account High Value)"
#         return False, "Low"

#     # Calculate Mean of past transactions
#     amounts = [t['amount'] for t in history]
#     avg_spend = sum(amounts) / len(amounts)
    
#     # Logic: If current amount is > 3x the average, it's an anomaly
#     if amount > (avg_spend * 3):
#         return True, "High (Value Deviation)"
    
#     return False, "Low"

import json
import os
from datetime import datetime

# ─── RISK THRESHOLDS ──────────────────────────────────────────────────────────
RISK_THRESHOLD_PIN   = 55   # Score >= this requires PIN verification
RISK_THRESHOLD_BLOCK = 90   # Score >= this blocks the transaction entirely

# ─── WEIGHT TABLE ─────────────────────────────────────────────────────────────
WEIGHTS = {
    "transaction_value":   30,   # max points for a suspiciously large amount
    "failed_attempts":     25,   # max points for prior failed biometric attempts
    "velocity":            20,   # max points for too many txns in short window
    "balance_ratio":       15,   # max points for spending most of the balance
    "time_anomaly":        10,   # max points for odd-hours transactions (11 PM–5 AM)
}


def _score_transaction_value(amount: float, history: list) -> tuple[float, str]:
    """High value relative to personal history → higher risk."""
    if not history:
        # No history: flat threshold
        if amount >= 20000:
            return WEIGHTS["transaction_value"], "New account, high-value transfer"
        if amount >= 5000:
            return WEIGHTS["transaction_value"] * 0.5, "New account, moderate-value transfer"
        return 0, "New account, low-value transfer"

    amounts  = [t["amount"] for t in history]
    avg      = sum(amounts) / len(amounts)
    max_hist = max(amounts)

    if amount > max_hist * 4:
        ratio = 1.0
        reason = f"Amount ₹{amount} is >4x personal maximum (₹{max_hist:.0f})"
    elif amount > avg * 3:
        ratio = 0.75
        reason = f"Amount ₹{amount} is >3x personal average (₹{avg:.0f})"
    elif amount > avg * 1.5:
        ratio = 0.35
        reason = f"Amount ₹{amount} moderately above average (₹{avg:.0f})"
    else:
        ratio = 0.0
        reason = "Amount within normal range"

    return round(WEIGHTS["transaction_value"] * ratio, 1), reason


def _score_failed_attempts(failed: int) -> tuple[float, str]:
    """Recent biometric failures indicate possible unauthorised access."""
    if failed == 0:
        return 0, "No failed attempts"
    if failed == 1:
        score = WEIGHTS["failed_attempts"] * 0.4
        reason = "1 recent failed biometric attempt"
    elif failed == 2:
        score = WEIGHTS["failed_attempts"] * 0.7
        reason = "2 recent failed biometric attempts"
    else:
        score = WEIGHTS["failed_attempts"]
        reason = f"{failed} failed biometric attempts — high suspicion"
    return round(score, 1), reason


def _score_velocity(history: list) -> tuple[float, str]:
    """Too many transactions in a short window → velocity fraud signal."""
    if len(history) < 2:
        return 0, "Insufficient history for velocity check"

    now = datetime.now()
    window_minutes = 30
    recent = []

    for t in history:
        try:
            ts = datetime.fromisoformat(t.get("timestamp", ""))
            delta = (now - ts).total_seconds() / 60
            if delta <= window_minutes:
                recent.append(t)
        except Exception:
            continue

    count = len(recent)
    if count >= 5:
        return WEIGHTS["velocity"], f"{count} transactions in last {window_minutes} min — velocity spike"
    if count >= 3:
        return round(WEIGHTS["velocity"] * 0.6, 1), f"{count} transactions in last {window_minutes} min"
    if count >= 2:
        return round(WEIGHTS["velocity"] * 0.3, 1), f"{count} transactions in last {window_minutes} min"
    return 0, "Normal transaction velocity"


def _score_balance_ratio(amount: float, balance: float) -> tuple[float, str]:
    """Spending a large fraction of remaining balance is risky."""
    if balance <= 0:
        return WEIGHTS["balance_ratio"], "Zero or negative balance"

    ratio = amount / balance
    if ratio >= 0.9:
        return WEIGHTS["balance_ratio"], f"Transfer is {ratio*100:.0f}% of total balance"
    if ratio >= 0.7:
        return round(WEIGHTS["balance_ratio"] * 0.7, 1), f"Transfer is {ratio*100:.0f}% of balance"
    if ratio >= 0.5:
        return round(WEIGHTS["balance_ratio"] * 0.4, 1), f"Transfer is {ratio*100:.0f}% of balance"
    return 0, "Balance ratio within safe range"


def _score_time_anomaly() -> tuple[float, str]:
    """Transactions at unusual hours (11 PM – 5 AM IST) are higher risk."""
    hour = datetime.now().hour
    if 23 <= hour or hour < 5:
        return WEIGHTS["time_anomaly"], f"Transaction at unusual hour ({hour:02d}:xx)"
    if 5 <= hour < 7:
        return round(WEIGHTS["time_anomaly"] * 0.4, 1), "Early morning transaction"
    return 0, "Transaction during normal hours"


# ─── PUBLIC API ───────────────────────────────────────────────────────────────

def calculate_risk_score(sender_folder: str, amount: float) -> dict:
    """
    Compute a composite risk score (0–100) for a proposed transaction.

    Returns a dict:
    {
        "score":         int,          # 0-100
        "level":         str,          # "Low" | "Medium" | "High" | "Critical"
        "requires_pin":  bool,
        "blocked":       bool,
        "breakdown":     list[dict],   # per-factor detail
        "recommendation": str
    }
    """
    # ── load user data ─────────────────────────────────────────────────────
    user_file = f"dataset/{sender_folder}/user.json"
    if not os.path.exists(user_file):
        return _build_result(0, [], "Unknown user — defaulting to Low risk")

    with open(user_file, "r") as f:
        data = json.load(f)

    history  = data.get("transactions", [])
    balance  = data.get("balance", 0)
    failed   = data.get("failed_attempts", 0)

    # ── score each factor ──────────────────────────────────────────────────
    factors = []

    s, r = _score_transaction_value(amount, history)
    factors.append({"factor": "Transaction Value",   "score": s, "max": WEIGHTS["transaction_value"],  "reason": r})

    s, r = _score_failed_attempts(failed)
    factors.append({"factor": "Failed Attempts",     "score": s, "max": WEIGHTS["failed_attempts"],    "reason": r})

    s, r = _score_velocity(history)
    factors.append({"factor": "Transaction Velocity","score": s, "max": WEIGHTS["velocity"],           "reason": r})

    s, r = _score_balance_ratio(amount, balance)
    factors.append({"factor": "Balance Ratio",       "score": s, "max": WEIGHTS["balance_ratio"],      "reason": r})

    s, r = _score_time_anomaly()
    factors.append({"factor": "Time Anomaly",        "score": s, "max": WEIGHTS["time_anomaly"],       "reason": r})

    total = min(round(sum(f["score"] for f in factors), 1), 100)
    return _build_result(total, factors)


def _build_result(score: float, factors: list, override_reason: str = "") -> dict:
    if score < 30:
        level = "Low"
        recommendation = "Transaction cleared — no additional checks required."
    elif score < RISK_THRESHOLD_PIN:
        level = "Medium"
        recommendation = "Elevated risk detected — proceed with standard biometric confirmation."
    elif score < RISK_THRESHOLD_BLOCK:
        level = "High"
        recommendation = "⚠️ High risk — PIN verification required before proceeding."
    else:
        level = "Critical"
        recommendation = "🚫 Transaction blocked — risk score exceeds safe threshold."

    if override_reason:
        recommendation = override_reason

    return {
        "score":          int(score),
        "level":          level,
        "requires_pin":   score >= RISK_THRESHOLD_PIN,
        "blocked":        score >= RISK_THRESHOLD_BLOCK,
        "breakdown":      factors,
        "recommendation": recommendation,
    }


def get_risk_thresholds() -> dict:
    """Expose thresholds so UI can reference them."""
    return {
        "pin_required": RISK_THRESHOLD_PIN,
        "blocked":      RISK_THRESHOLD_BLOCK,
    }