# QA Integration Tests

Repositório-base de testes de integração em Python + Pytest.

## Objetivo

Este projeto foi estruturado para servir como um repositório de testes de integração reutilizável, com:

- PostgreSQL
- OpenSearch
- suporte a múltiplas instâncias/conexões
- Pytest
- pytest-html
- execução local
- execução via Docker
- execução em pipeline
- separação entre conexão, queries, repositories e testes

Os testes **não executam SQL diretamente**. Eles apenas validam o retorno dos métodos da camada de repository.

## Arquitetura

```text
qa-integration-tests/
├── .github/
│   └── workflows/
│       └── integration-tests.yml
├── .vscode/
│   ├── extensions.json
│   ├── settings.json
│   └── tasks.json
├── src/
│   ├── config/
│   │   └── settings.py
│   ├── connections/
│   │   ├── base.py
│   │   ├── factory.py
│   │   ├── opensearch.py
│   │   └── postgres.py
│   ├── models/
│   │   └── table_metadata.py
│   ├── queries/
│   │   └── postgres_queries.py
│   └── repositories/
│       └── postgres_catalog_repository.py
├── tests/
│   ├── conftest.py
│   └── integration/
│       └── postgres/
│           ├── test_postgres_connection.py
│           └── test_postgres_pg_tables.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── pytest.ini
└── requirements.txt
```

## Responsabilidades

### `src/config`

Centraliza configurações vindas de variáveis de ambiente.

### `src/connections`

Responsável apenas por criar, manter e fechar clientes/conexões.

### `src/queries`

Centraliza SQLs. Os testes não conhecem SQL.

### `src/repositories`

Executa queries e transforma os resultados em objetos de domínio.

### `tests`

Valida somente o comportamento público dos repositories/connections expostos pelas fixtures.

---

# Requisitos

- Python 3.10+
- Docker opcional

## 1. Criar ambiente virtual

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. Instalar dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Criar configuração local

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

## 4. Subir PostgreSQL local

```bash
docker compose up -d postgres
```

O projeto usa por padrão:

```text
host: localhost
port: 5432
database: qa_db
user: qa_user
password: qa_password
```

## 5. Rodar os testes

```bash
pytest
```

Somente integração:

```bash
pytest -m integration
```

PostgreSQL:

```bash
pytest -m postgres
```

## 6. Relatório HTML

O `pytest-html` gera automaticamente um relatório único em:

```text
reports/test-report.html
```

Para executar os testes e gerar o relatório:

```bash
make report
```

Para abrir o arquivo no navegador local:

```bash
make open-report
```

Em um servidor Linux sem interface gráfica, disponibilize o relatório por HTTP:

```bash
make serve-report
```

Em seguida, acesse `http://localhost:8000/test-report.html` usando o encaminhamento da porta 8000 do VS Code.

---

# Testes incluídos

## Conectividade PostgreSQL

Valida o retorno de:

```python
repository.check_connection()
```

Internamente o repository executa:

```sql
SELECT 1 AS health;
```

O teste não conhece esse SQL.

## Validação de `pg_catalog.pg_tables`

O repository executa um `SELECT` na view:

```text
pg_catalog.pg_tables
```

Por padrão o teste procura:

```text
pg_catalog.pg_type
```

`pg_type` é uma tabela interna do PostgreSQL e torna o teste independente de dados de negócio.

O teste recebe um `TableMetadata` e valida somente o contrato retornado.

---

# Múltiplos bancos PostgreSQL

A configuração suporta prefixos.

Exemplo:

```env
SOURCE_PG_HOST=source-db
SOURCE_PG_PORT=5432
SOURCE_PG_DATABASE=source
SOURCE_PG_USER=user
SOURCE_PG_PASSWORD=password

TARGET_PG_HOST=target-db
TARGET_PG_PORT=5432
TARGET_PG_DATABASE=target
TARGET_PG_USER=user
TARGET_PG_PASSWORD=password
```

No Python:

```python
from src.config.settings import PostgresSettings
from src.connections.postgres import PostgresConnection

source_settings = PostgresSettings.from_env("SOURCE_PG")
target_settings = PostgresSettings.from_env("TARGET_PG")

source = PostgresConnection(source_settings)
target = PostgresConnection(target_settings)
```

Isso permite usar o mesmo padrão em cenários ETL, por exemplo:

```text
Source DB -> Transformação -> Target DB
```

---

# OpenSearch

A base de conexão já está incluída.

Variáveis:

```env
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_USER=admin
OPENSEARCH_PASSWORD=admin
OPENSEARCH_USE_SSL=false
OPENSEARCH_VERIFY_CERTS=false
```

Exemplo:

```python
from src.config.settings import OpenSearchSettings
from src.connections.opensearch import OpenSearchConnection

settings = OpenSearchSettings.from_env()
connection = OpenSearchConnection(settings)

client = connection.client
```

Para criar testes de OpenSearch, mantenha o mesmo padrão:

```text
connection -> repository -> test
```

Não coloque chamadas ao OpenSearch diretamente no teste.

---

# Pipeline

Um exemplo de GitHub Actions está em:

```text
.github/workflows/integration-tests.yml
```

A pipeline:

1. inicia PostgreSQL;
2. instala Python;
3. instala dependências;
4. executa Pytest;
5. gera o relatório HTML;
6. publica os resultados como artifact.

A mesma estrutura pode ser transportada para:

- GitLab CI
- Azure DevOps
- Jenkins
- Bitbucket Pipelines

---

# Boas práticas adotadas

## SOLID

- **SRP:** conexão, SQL, repository, configuração e teste possuem responsabilidades separadas.
- **OCP:** novos tipos de conexão podem ser adicionados sem alterar os testes existentes.
- **LSP:** conexões seguem o contrato `BaseConnection`.
- **ISP:** o contrato de conexão é pequeno.
- **DIP:** repositories recebem a conexão por injeção de dependência.

## DRY

- conexão é criada em fixture;
- SQL centralizado;
- configuração centralizada;
- execução de query reutilizada dentro do repository.

## KISS

Não há framework interno complexo. O fluxo é:

```text
Settings
   ↓
Connection
   ↓
Repository
   ↓
Pytest
   ↓
pytest-html
```

---

# Regra para evolução do repositório

Para cada nova tecnologia:

```text
src/connections/<tecnologia>.py
src/queries/<tecnologia>_queries.py
src/repositories/<tecnologia>_repository.py
tests/integration/<tecnologia>/
```

Exemplo futuro:

```text
src/connections/mysql.py
src/connections/sqlserver.py
src/connections/s3.py

src/repositories/mysql_repository.py
src/repositories/sqlserver_repository.py
src/repositories/opensearch_repository.py

tests/integration/mysql/
tests/integration/sqlserver/
tests/integration/opensearch/
```

Esse padrão mantém o repositório escalável sem transformar os arquivos de teste em scripts de infraestrutura.
