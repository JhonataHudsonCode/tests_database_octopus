SELECT_CLIENT_BY_ID = """
SELECT
    client_id,
    has_rsa,
    octopus_endpoint
FROM public.clients
WHERE client_id = %s;
"""

SELECT_ALL_CLIENTS = """
SELECT
    client_id,
    has_rsa,
    octopus_endpoint
FROM public.clients
ORDER BY client_id;
"""
