SELECT_CLIENT_BY_ID = """
SELECT
    client_id,
    has_rsa,
    has_alerts,
    octopus_endpoint
FROM {schema_name}.clients
WHERE client_id = %s;
"""

SELECT_ALL_CLIENTS = """
SELECT
    client_id,
    has_rsa,
    has_alerts,
    octopus_endpoint
FROM {schema_name}.clients
ORDER BY client_id;
"""
