from fraud_detection.fraud_rules import evaluate_transaction


def classify_risk(score: int) -> str:
    if score >= 70:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 30:
        return "MEDIUM"
    return "LOW"


def calculate_risk(
    amount: float,
    transaction_timestamp,
    processing_time_ms,
    response_code: str,
    is_suspicious: bool,
) -> dict:

    rules = evaluate_transaction(
        amount=amount,
        transaction_timestamp=transaction_timestamp,
        processing_time_ms=processing_time_ms,
        response_code=response_code,
        is_suspicious=is_suspicious,
    )

    score = rules.total_score

    return {
        "risk_score": score,
        "risk_level": classify_risk(score),
        "amount_score": rules.amount_score,
        "unusual_hour_score": rules.unusual_hour_score,
        "processing_time_score": rules.processing_time_score,
        "response_code_score": rules.response_code_score,
        "suspicious_flag_score": rules.suspicious_flag_score,
    }