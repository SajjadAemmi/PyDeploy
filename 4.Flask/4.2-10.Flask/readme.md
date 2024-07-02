

## Run

```

```

## Docker

Use PostgreSQL database docker

```bash
docker pull postgres
docker run -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=ramze_akbar_agha -e POSTGRES_USER=akbar_agha -e POSTGRES_DB=database_akbar_agha -d postgres
```

```bash
docker build -t ai_web_app .
```

```bash
docker run --rm -p 5432:5432 -p 8080:5000 -v $(pwd):/myapp ai_web_app
```

## Docker compose
