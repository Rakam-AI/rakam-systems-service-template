# dj_ai_api

## General

The API is developped to serve as a base for all RAKAM AI projects using AI.

---

## Endpoints

- #### GET /health

Cet endpoint permet de tester le bon fonctionnement du serveur. Le status code devrait être 200.

```json
{
  "status": "healthy"
}
```

## Docker :

#### Lancer le container docker :

```bash
sudo docker compose -f docker-compose-dev.yml up
sudo docker compose -f docker-compose-prod.yml up
```

#### Stopper un container

```bash
sudo docker compose -f docker-compose-dev.yml down
```

#### Stopper un container et supprimer ses images

```bash
sudo docker compose -f docker--compose-dev.yml down && docker system prune -af && docker volume prune -f docker-compose-dev.yml
```

## Architecture du code

```
|-- DJ-AI-API
    |-- api-auth
    |-- application
    |-- server
```

1. **api-auth** should contains the authentication logic.
2. **application** should contains the main logic (AI engine).
3. **server** should contains the API set up.
