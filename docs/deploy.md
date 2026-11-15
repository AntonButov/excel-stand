# Deploy excel-stand

> Проверено: 2026-11-15

| | |
|--|--|
| Host | **80.87.196.33** only |
| Path | `/opt/excel-stand` |
| Port | **8130** → container `8080` |
| Health | `http://80.87.196.33:8130/health` |

**Not on** `206.223.250.251` (landing only).

Secrets: `DEPLOY_SSH_PRIVATE_KEY`, `DEPLOY_USER` (`root`).

Push to `main` → workflow `deploy`.
