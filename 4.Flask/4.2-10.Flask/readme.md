

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

## 2 Dockers

```bash
docker network create my_network
```

```bash
docker run --network my_network --name some-postgres -e POSTGRES_PASSWORD=ramze_akbar_agha -e POSTGRES_USER=akbar_agha -e POSTGRES_DB=database_akbar_agha -d postgres
```

```bash
docker run --rm --network my_network --name ai_web_app -p 8080:5000 -v $(pwd):/myapp ai_web_app
```

## Docker compose

```bash
docker compose up -d
```

```bash
docker compose ps
```

Stop your services once you've finished with them:

```bash
docker compose stop
```

You can bring everything down, removing the containers entirely, with the following command:

```bash
docker compose down
```

https://devhints.io/docker-compose
