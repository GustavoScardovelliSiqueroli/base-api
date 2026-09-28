# base-api

![CI](https://github.com/GustavoScardovelliSiqueroli/base-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

API base em **FastAPI** com arquitetura modular, autenticação **JWT** e suíte de testes.
Serve como ponto de partida para novos serviços back-end.

## ✨ Recursos

- **FastAPI** + **SQLAlchemy 2.0**
- **Autenticação OAuth2/JWT** (`PyJWT`) com hash de senha em **bcrypt**
- Configuração via **Pydantic Settings** (variáveis de ambiente / `.env`)
- **Arquitetura modular** por domínio (`modules/`), com separação de router, service, repositório e schemas
- **Tratamento centralizado de erros** (exceções de domínio → handler)
- **Testes** com `pytest`, `pytest-asyncio` e `httpx`, com relatório de **coverage**
- Qualidade de código com **Ruff** (lint + format) e automação de tarefas com **Taskipy**
- Gerenciamento de dependências com **Poetry** (Python 3.12+)

## 🧱 Arquitetura

```
base_api/
├── api/v1/router.py         # agrega as rotas da API v1
├── core/
│   ├── configs.py           # Settings (Pydantic)
│   ├── database.py          # Base do SQLAlchemy / sessão
│   ├── exceptions.py        # exceções de domínio
│   └── errors_handlers.py   # handlers centralizados
├── infra/db/repositories/   # implementação de repositórios
├── modules/
│   ├── auth/                # router, service, schemas, dependencies
│   └── user/                # router, model, repository, service, schemas
├── shared/response_schemas.py  # envelope padrão de resposta (ApiResponse)
└── main.py                  # create_app()
tests/                       # testes unitários e de integração
```

> No estado atual, o `UserRepository` usado é um **repositório em memória**
> (`infra/db/repositories/inmemory_user_repository.py`), demonstrando a troca de
> implementação sem tocar no serviço. O modelo `User` (tabela `users`) já existe via SQLAlchemy.

## 🔌 Endpoints

| Método | Rota | Descrição | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Cadastra um usuário | — |
| `POST` | `/api/v1/auth/login` | Autentica e retorna o token JWT | — |
| `GET`  | `/api/v1/users/` | Lista usuários | Bearer |

A documentação interativa fica em `/docs` (Swagger) e `/redoc`.

## 🚀 Como rodar

Requer **Python 3.12+** e [Poetry](https://python-poetry.org/).

```bash
git clone https://github.com/GustavoScardovelliSiqueroli/base-api.git
cd base-api
poetry install

# crie o .env
echo "API_KEY=sua-chave-secreta" > .env

poetry run uvicorn base_api.main:app --reload
```

## ⚙️ Configuração (`.env`)

| Variável | Padrão | Descrição |
| :--- | :--- | :--- |
| `API_KEY` | *(obrigatória)* | Segredo usado para assinar o JWT |
| `ACCESS_TOKEN_EXPIRE_HOURS` | `24` | Validade do token |
| `JWT_ALGORITHM` | `HS256` | Algoritmo de assinatura |

## 🧪 Testes

```bash
poetry run task test      # pytest -s -x --cov=base_api -vv + coverage html
```

## 🧹 Qualidade

```bash
poetry run task lint      # ruff check
poetry run task format    # ruff check --fix + ruff format
```

## 📄 Licença

MIT — veja `LICENSE`.
