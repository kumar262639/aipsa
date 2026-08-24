# Architecture Overview

```text
React + TypeScript
       |
       | REST
       v
FastAPI
  |    |
  |    +--> Guardrails
  |
  +--> LLM / fallback router
          |
          v
     Allow-listed tools
       |       |
       v       v
  Product DB  Order DB
       |
       v
    Audit log
```

The browser has no database access.

The LLM handles language understanding and structured routing. The backend remains authoritative for business operations.

Production evolution: SQLite -> PostgreSQL/MySQL; structured filtering -> OpenSearch; demo identity -> OAuth2/OIDC + RBAC; logs -> OpenTelemetry.
