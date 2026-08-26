CHECK_CONNECTION = """
SELECT 1 AS health;
"""

SELECT_TABLE_FROM_PG_TABLES = """
SELECT
    schemaname,
    tablename,
    tableowner,
    tablespace,
    hasindexes,
    hasrules,
    hastriggers,
    rowsecurity
FROM pg_catalog.pg_tables
WHERE schemaname = %s
  AND tablename = %s;
"""
