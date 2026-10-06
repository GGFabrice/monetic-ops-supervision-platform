from datetime import datetime

from fraud_detection.risk_scoring import calculate_risk, classify_risk


def test_low_risk():
    result = calculate_risk(
        amount=10000,
        transaction_timestamp=datetime(2026, 6, 15, 14, 30),
        processing_time_ms=300,
        response_code="00",
        is_suspicious=False,
    )

    assert result["risk_score"] == 0
    assert result["risk_level"] == "LOW"


def test_high_risk():
    result = calculate_risk(
        amount=600000,
        transaction_timestamp=datetime(2026, 6, 15, 2, 30),
        processing_time_ms=2500,
        response_code="51",
        is_suspicious=False,
    )

    assert result["risk_score"] == 65
    assert result["risk_level"] == "HIGH"


def test_critical_risk():
    result = calculate_risk(
        amount=600000,
        transaction_timestamp=datetime(2026, 6, 15, 2, 30),
        processing_time_ms=2500,
        response_code="51",
        is_suspicious=True,
    )

    assert result["risk_score"] == 85
    assert result["risk_level"] == "CRITICAL"


def test_risk_score_maximum():
    result = calculate_risk(
        amount=1000000,
        transaction_timestamp=datetime(2026, 6, 15, 3, 30),
        processing_time_ms=5000,
        response_code="96",
        is_suspicious=True,
    )

    assert result["risk_score"] <= 100


def test_classify_risk():
    assert classify_risk(0) == "LOW"
    assert classify_risk(29) == "LOW"
    assert classify_risk(30) == "MEDIUM"
    assert classify_risk(49) == "MEDIUM"
    assert classify_risk(50) == "HIGH"
    assert classify_risk(69) == "HIGH"
    assert classify_risk(70) == "CRITICAL"
    assert classify_risk(100) == "CRITICAL"