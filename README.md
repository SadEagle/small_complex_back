# About

Current project is the realization of a small backend application with monolithic architecture.

The project contain current points:
- [x] FastAPI
- [x] JWT auth
- [x] SQLAlchemy ORM + Pydantic
- [x] Alembic migrations
- [x] Docker/Compose
- [x] Async
- [ ] RabbitMQ

Note, `flake.nix` and `flake.lock` are NixOS specific package manager files

# Run

1. Program run
```
docker compose up
``` 
2. DB initialization with alembic script:
```
docker exec small_complex_back-backend-1 uv run alembic upgrade head 
```
3. Test swagger documentation on `http://localhost:8000/#docs`
