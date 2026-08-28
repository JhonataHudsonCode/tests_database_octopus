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
    connect_timeout: int
    target_schema: str
    target_table: str

    @classmethod
    def from_env(cls, prefix: str = "PG") -> "PostgresSettings":
        return cls(
            host=_env(prefix, "HOST"),
            port=int(_env(prefix, "PORT")),
            database=_env(prefix, "DATABASE"),
            user=_env(prefix, "USER"),
            password=_env(prefix, "PASSWORD"),
            connect_timeout=int(_env(prefix, "CONNECT_TIMEOUT")),
            target_schema=_env(prefix, "TARGET_SCHEMA"),
            target_table=_env(prefix, "TARGET_TABLE"),
        )


@dataclass(frozen=True, slots=True)
class OpenSearchSettings:
    host: str
    port: int
    user: str
    password: str
    use_ssl: bool
    verify_certs: bool

    @classmethod
    def from_env(cls, prefix: str = "OPENSEARCH") -> "OpenSearchSettings":
        return cls(
            host=_env(prefix, "HOST"),
            port=int(_env(prefix, "PORT")),
            user=_env(prefix, "USER"),
            password=_env(prefix, "PASSWORD"),
            use_ssl=_to_bool(_env(prefix, "USE_SSL")),
            verify_certs=_to_bool(_env(prefix, "VERIFY_CERTS")),
        )


@dataclass(frozen=True, slots=True)
class OpenSearchDashboardsSettings:
    host: str
    port: int
    user: str
    password: str
    use_ssl: bool
    verify_certs: bool
    path_prefix: str
    request_timeout: int

    @classmethod
    def from_env(
        cls,
        prefix: str = "OPENSEARCH_DASHBOARDS",
    ) -> "OpenSearchDashboardsSettings":
        return cls(
            host=_env(prefix, "HOST"),
            port=int(_env(prefix, "PORT")),
            user=_env(prefix, "USER"),
            password=_env(prefix, "PASSWORD"),
            use_ssl=_to_bool(_env(prefix, "USE_SSL")),
            verify_certs=_to_bool(_env(prefix, "VERIFY_CERTS")),
            path_prefix=_optional_env(prefix, "PATH_PREFIX").rstrip("/"),
            request_timeout=int(_env(prefix, "REQUEST_TIMEOUT")),
        )
