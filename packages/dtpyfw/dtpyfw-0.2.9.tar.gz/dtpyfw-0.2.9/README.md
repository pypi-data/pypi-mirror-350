# DealerTower Python Framework (dtpyfw)

**DealerTower Framework** provides reusable, production‑ready building blocks for DealerTower microservices. It’s organized into modular sub‑packages, each focusing on a specific domain:

---

- **Core** – Fundamental utilities  
- **API** – FastAPI helpers  
- **Database** – SQLAlchemy orchestration  
- **Bucket** – S3-compatible storage  
- **FTP** – FTP/SFTP file operations  
- **Redis** – Caching & Streams  
- **Worker** – Celery task management  
- **Encryption** – Hashing & JWT  

---

## 🚀 Installation

### Base package & Core
```bash
pip install dtpyfw
```
### Optional Extras
Install just the features you need:

| Sub‑Package   | Description                          | Install Command                 | Docs                                |
|---------------|--------------------------------------|---------------------------------|-------------------------------------|
| **core**      | Env, errors, async bridge, utils     | included in base                | [Core Docs](docs/core.md)           |
| **api**       | FastAPI middleware & routing helpers | `pip install dtpyfw[api]`       | [API Docs](docs/api.md)             |
| **db**        | SQLAlchemy sync/async & search tools | `pip install dtpyfw[db]`        | [DB Docs](docs/db.md)               |
| **bucket**    | S3‑compatible file management        | `pip install dtpyfw[bucket]`    | [Bucket Docs](docs/bucket.md)       |
| **ftp**       | FTP and SFTP convenience wrappers    | `pip install dtpyfw[ftp]`       | [FTP Docs](docs/ftp.md)             |
| **redis**     | Redis clients & Streams consumer     | `pip install dtpyfw[redis]`     | [Redis Docs](docs/redis.md)         |
| **worker**    | Celery task & scheduler setup        | `pip install dtpyfw[worker]`    | [Worker Docs](docs/worker.md)       |
| **encrypt**   | Password hashing & JWT utilities     | `pip install dtpyfw[encrypt]`   | [Encryption Docs]( docs/encrypt.md) |
| **slim-task** | DB, Redis, Worker                    | `pip install dtpyfw[slim-task]` | —                                   |
| **slim-api**  | API, DB                              | `pip install dtpyfw[slim-api]`  | —                                   |
| **normal**    | API, DB, Redis, Worker               | `pip install dtpyfw[normal]`    | —                                   |
| **all**       | Everything above                     | `pip install dtpyfw[all]`       | —                                   |

---

## 📦 Sub‑Package Summaries

### Core  
Fundamental utilities and patterns shared across services:
- **Env Management**: `.env` loading + whitelist.  
- **Error Handling**: `RequestException` + `exception_to_dict`.  
- **Async Bridge**: `async_to_sync` helper.  
- **Data Utilities**: list chunking, slug/URL helpers, safe accessors.  
- **Request Wrapper**: HTTP calls with telemetry.  
- **Retry Decorators**: sync/async retries with backoff.  

More details → [Core Docs](docs/core.md)

---

### API  
Turnkey FastAPI setup:
- **MainApp** & **SubApp**: compose multi‑app services with CORS, docs, and lifecycle hooks.  
- **Middleware**: structured error, validation, and runtime logging.  
- **Routing**: `Route` & `Router` classes for declarative endpoint definitions.  
- **Auth Helpers**: API key header/query validation.  
- **Response Utils**: consistent JSON envelopes with cache headers.  

More details → [API Docs](docs/api.md)

---

### Database (DB)  
SQLAlchemy orchestration for sync/async workflows:
- **DatabaseConfig**: fluent connection settings.  
- **DatabaseInstance**: engine creation, session context managers, health checks.  
- **ModelBase**: UUID PKs, timestamps, `.to_dict()`, diffing.  
- **Search Helpers**: dynamic filter UI values, min/max aggregations.  

More details → [DB Docs](docs/db.md)

---

### Bucket  
Simplified S3-compatible storage:
- **Initialization**: custom endpoints or AWS S3 mode.  
- **URL Generation**: public object URLs.  
- **File Ops**: upload (bytes/path), download, duplicate, safe‑duplicate, delete.  
- **Existence Check**: head_object wrapper.  

More details → [Bucket Docs](docs/bucket.md)

---

### FTP/SFTP  
Unified FTP & SFTP client:
- **Connection**: auto‑choose ftplib vs Paramiko.  
- **Directory Ops**: list, create, remove.  
- **File Transfers**: upload/download to path or file‑like object.  
- **Metadata**: fetch last‑modified timestamps.  

More details → [FTP Docs](docs/ftp.md)

---

### Redis & Streams  
Robust caching and message streaming:
- **RedisConfig** + **RedisInstance**: sync/async clients with SSL support.  
- **Cache Decorator**: `cache_function` with namespace, TTL, conditional caching.  
- **Consumer**: Redis Streams consumer with retry logic, handler registration, and cleanup.  
- **Health Check**: simple ping utility.  

More details → [Redis Docs](docs/redis.md)

---

### Worker  
Celery setup helper for tasks and periodic jobs:
- **Task**: register task routes and RedBeat schedules.  
- **Worker**: fluent Celery app builder—broker/backend config, serializers, timezone, and SSL.  
- **Auto Discovery**: plug in task list and beat schedule automatically.  

More details → [Worker Docs](docs/worker.md)

---

### Encryption  
Out‑of‑the‑box password & token security:
- **Hash**: bcrypt via Passlib.  
- **JWT**: `jwt_encrypt` & `jwt_decrypt` with subject validation and exp check.  

More details → [Encryption Docs](docs/encrypt.md)

---

## 📄 License  
DealerTower Python Framework is proprietary. See [LICENSE](LICENSE) for terms.  
