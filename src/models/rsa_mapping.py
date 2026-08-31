from __future__ import annotations

from typing import Any


EXPECTED_RSA_MAPPING: dict[str, str | dict[str, Any]] = {
    "@timestamp": "date",
    "@version": "text",
    "first_scan": "date",
    "ip": "text",
    "key": "text",
    "last_time_vulnerable": "date",
    "locations": "object",
    "main_domain": "text",
    "os": {
        "cpes": "text",
        "name": "text",
    },
    "port": "long",
    "port_severity": "text",
    "port_severity_level": "long",
    "port_severity_reason": "text",
    "ports": {
        "cpes": "text",
        "port": "long",
        "product": "text",
        "protocol": "text",
        "reason": "text",
        "service": "text",
        "severity": "text",
        "severity_level": "long",
        "ssl": "boolean",
        "version": "text",
    },
    "scan_date": "date",
    "status": "text",
    "status_code": "text",
    "subdomain": "text",
    "subdomain_takeover_vulnerable": "boolean",
    "subdomain_tools": "text",
    "tags": "text",
    "times_vulnerable": "long",
    "title": "text",
    "vulnerable": "boolean",
    "vulns": "text",
}
