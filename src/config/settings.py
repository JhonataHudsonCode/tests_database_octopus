from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _env(prefix: str, name: str) -> str:
    normalized_prefix = prefix.strip("_").upper()
    key = f"{normalized_prefix}_{name}" if normalized_prefix else name

    value = os.getenv(key)
    if value is None or value == "":
        raise ValueError(f"Variável de ambiente obrigatória não configurada: {key}")

    return value


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True, slots=True)
class PostgresSettings:
    host: str
    port: int
    database: str
    user: str
    password: str
    connect_timeout: int

    @classmethod
    def from_env(cls, prefix: str = "PG") -> "PostgresSettings":
        return cls(
            host=_env(prefix, "HOST"),
            port=int(_env(prefix, "PORT")),
            database=_env(prefix, "DATABASE"),
            user=_env(prefix, "USER"),
            password=_env(prefix, "PASSWORD"),
            connect_timeout=int(_env(prefix, "CONNECT_TIMEOUT")),
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
