from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _env(prefix: str, name: str, default: str | None = None) -> str:
    normalized_prefix = prefix.strip("_").upper()
    key = f"{normalized_prefix}_{name}" if normalized_prefix else name

    value = os.getenv(key, default)
    if value is None or value == "":
        raise ValueError(f"Variável de ambiente obrigatória não configurada: {key}")

    return value


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _optional_env(prefix: str, name: str, default: str = "") -> str:
    normalized_prefix = prefix.strip("_").upper()
    key = f"{normalized_prefix}_{name}" if normalized_prefix else name
    return os.getenv(key, default).strip()


@dataclass(frozen=True, slots=True)
class PostgresSettings:
    host: str
    port: int
    database: str
    user: str
    password: str
    connect_timeout: int = 5
    target_schema: str = "pg_catalog"
    target_table: str = "pg_type"

    @classmethod
    def from_env(cls, prefix: str = "PG") -> "PostgresSettings":
        return cls(
            host=_env(prefix, "HOST", "localhost"),
            port=int(_env(prefix, "PORT", "5432")),
            database=_env(prefix, "DATABASE", "qa_db"),
            user=_env(prefix, "USER", "qa_user"),
            password=_env(prefix, "PASSWORD", "qa_password"),
            connect_timeout=int(_env(prefix, "CONNECT_TIMEOUT", "5")),
            target_schema=_env(prefix, "TARGET_SCHEMA", "pg_catalog"),
            target_table=_env(prefix, "TARGET_TABLE", "pg_type"),
        )


@dataclass(frozen=True, slots=True)
class OpenSearchSettings:
    host: str
    port: int
    user: str
    password: str
    use_ssl: bool = False
    verify_certs: bool = False

    @classmethod
    def from_env(cls, prefix: str = "OPENSEARCH") -> "OpenSearchSettings":
        return cls(
            host=_env(prefix, "HOST", "localhost"),
            port=int(_env(prefix, "PORT", "9200")),
            user=_env(prefix, "USER", "admin"),
            password=_env(prefix, "PASSWORD", "admin"),
            use_ssl=_to_bool(_env(prefix, "USE_SSL", "false")),
            verify_certs=_to_bool(_env(prefix, "VERIFY_CERTS", "false")),
        )


@dataclass(frozen=True, slots=True)
class OpenSearchDashboardsSettings:
    host: str
    port: int
    user: str
    password: str
    use_ssl: bool = False
    verify_certs: bool = False
    path_prefix: str = ""
    request_timeout: int = 10

    @classmethod
    def from_env(
        cls,
        prefix: str = "OPENSEARCH_DASHBOARDS",
    ) -> "OpenSearchDashboardsSettings":
        return cls(
            host=_env(prefix, "HOST"),
            port=int(_env(prefix, "PORT", "5601")),
            user=_env(prefix, "USER", "admin"),
            password=_env(prefix, "PASSWORD", "admin"),
            use_ssl=_to_bool(_env(prefix, "USE_SSL", "false")),
            verify_certs=_to_bool(_env(prefix, "VERIFY_CERTS", "false")),
            path_prefix=_optional_env(prefix, "PATH_PREFIX").rstrip("/"),
            request_timeout=int(_env(prefix, "REQUEST_TIMEOUT", "10")),
        )
