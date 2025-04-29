# test_alert_parser.py

import pytest
from alert_parser import parse_alert, analyze_alert, AlertModel

# Тестовые алерты
TEST_ALERTS = [
    {
        "text": "[ALERT][HIGH] ssh | IP: 192.168.1.100 had 5 ssh failures and 3 credential stuffing attempts",
        "expected": {
            "severity": "alert",
            "priority": "high",
            "event_type": "ssh",
            "ip": "192.168.1.100",
            "failures": 5,
            "event_category": "credential_stuffing",
            "valid": True
        }
    },
    {
        "text": "[ALERT][HIGH] web_login_failed | Multiple IPs targeting a single server with low failure rate",
        "expected": {
            "severity": "alert",
            "priority": "high",
            "event_type": "web_login_failed",
            "event_category": None,
            "failures": None,
            "valid": True
        }
    },
    {
        "text": "[ALERT][HIGH] ssh | IP: 172.16.0.50 trying to login with unusual usernames",
        "expected": {
            "severity": "alert",
            "priority": "high",
            "event_type": "ssh",
            "ip": "172.16.0.50",
            "failures": None,
            "event_category": "account_probe",
            "valid": True
        }
    },
    {
        "text": "Invalid alert format without brackets",
        "expected": {
            "valid": False
        }
    }
]

@pytest.mark.parametrize("alert_case", TEST_ALERTS)
def test_alert_parsing(alert_case):
    alert_text = alert_case["text"]
    expected = alert_case["expected"]

    alert = parse_alert(alert_text)
    alert = analyze_alert(alert_text, alert)
    result = alert.dict()

    for key, value in expected.items():
        assert result.get(key) == value, f"Mismatch in {key}: expected {value}, got {result.get(key)}"
