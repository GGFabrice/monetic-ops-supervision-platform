from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FraudRuleResult:
    amount_score: int = 0
    unusual_hour_score: int = 0
    processing_time_score: int = 0
    response_code_score: int = 0
    suspicious_flag_score: int = 0

    @property
    def total_score(self) -> int:
        return min(
            100,
            self.amount_score
            + self.unusual_hour_score
            + self.processing_time_score
            + self.response_code_score
            + self.suspicious_flag_score
        )


def check_amount(amount: float) -> int:
    if amount >= 500000:
        return 25
    return 0


def check_unusual_hour(transaction_timestamp: datetime) -> int:
    hour = transaction_timestamp.hour

    if 0 <= hour < 6:
        return 15

    return 0


def check_processing_time(processing_time_ms: Optional[int]) -> int:
    if processing_time_ms is not None and processing_time_ms > 2000:
        return 15

    return 0


def check_response_code(response_code: str) -> int:
    risky_codes = {
        "05",
        "14",
        "51",
        "54",
        "55",
        "57",
        "91",
        "96",
    }

    if response_code in risky_codes:
        return 10

    return 0


def check_suspicious_flag(is_suspicious: bool) -> int:
    if is_suspicious:
        return 20

    return 0


def evaluate_transaction(
    amount: float,
    transaction_timestamp: datetime,
    processing_time_ms: Optional[int],
    response_code: str,
    is_suspicious: bool,
) -> FraudRuleResult:

    return FraudRuleResult(
        amount_score=check_amount(amount),
        unusual_hour_score=check_unusual_hour(transaction_timestamp),
        processing_time_score=check_processing_time(processing_time_ms),
        response_code_score=check_response_code(response_code),
        suspicious_flag_score=check_suspicious_flag(is_suspicious),
    )