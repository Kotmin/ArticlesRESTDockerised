# ArticlesRESTDockerised

## Overview

The Article Management API is a FastAPI-based application for managing articles with details such as name, tags, dates, category, and more. The application is designed to demonstrate various database isolation levels using PostgreSQL in a microservices architecture.


[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Kotmin/ArticlesRESTDockerised/article-management-api)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Kotmin/ArticlesRESTDockerised/article-management-api/blob/main/LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Quickstart](#quickstart)
  - [Docker Compose](#docker-compose)
  - [DB User Addition](#manual-user-addition)
- [API Endpoints](#api-endpoints)


## Quickstart
### Docker Compose

To get started with the Article Management API using Docker Compose, follow these steps:

  Clone the repository:

  ```bash

    git clone https://github.com/yourusername/article-management-api.git
    cd article-management-api
```
Build and start the services:

```bash

    docker-compose up --build
```
  This will start the PostgreSQL database and the FastAPI application.

## To turn down service

```bash
  docker-compose down
```

### Turn service down (and db whipe)

```bash
  docker-compose down -v
```

## Manual User Addition

After starting the services, add the necessary users to the PostgreSQL database:

### Access the PostgreSQL container:

    
```bash

docker-compose exec db psql -U user1 -d isolation_demo
```

#### Alt

```bash
  docker exec -it <db_container_id> psql -U user1 -d isolation_demo
```

Add the second user:

```sql

    CREATE USER user2 WITH PASSWORD 'password2';
    GRANT ALL PRIVILEGES ON DATABASE isolation_demo TO user2;
```
## API Endpoints

Full documentation aviable also at "/docs" endpoint
Create Article

    Endpoint: /articles/
    Method: POST
  Request Body:

  ```json

{
  "name": "Article 1",
  "tags": ["tag1", "tag2"],
  "creation_date": "2023-05-27T12:00:00",
  "modification_date": null,
  "publication_date": null,
  "category": "Category 1",
  "content_path": "/path/to/content1",
  "thumbnail": "/path/to/thumbnail1",
  "subtitle": "Subtitle 1"
}
```
Response:

```json

    {
      "id": "generated-uuid",
      "name": "Article 1",
      "tags": ["tag1", "tag2"],
      "creation_date": "2023-05-27T12:00:00",
      "modification_date": null,
      "publication_date": null,
      "category": "Category 1",
      "content_path": "/path/to/content1",
      "thumbnail": "/path/to/thumbnail1",
      "subtitle": "Subtitle 1"
    }
```
Get All Articles

    Endpoint: /articles/
    Method: GET
  Response:

  ```json

    [
      {
        "id": "generated-uuid",
        "name": "Article 1",
        "tags": ["tag1", "tag2"],
        "creation_date": "2023-05-27T12:00:00",
        "modification_date": null,
        "publication_date": null,
        "category": "Category 1",
        "content_path": "/path/to/content1",
        "thumbnail": "/path/to/thumbnail1",
        "subtitle": "Subtitle 1"
      }
    ]
```

Get Article by ID

    Endpoint: /articles/{article_id}
    Method: GET
  Response:

  ```json

    {
      "id": "generated-uuid",
      "name": "Article 1",
      "tags": ["tag1", "tag2"],
      "creation_date": "2023-05-27T12:00:00",
      "modification_date": null,
      "publication_date": null,
      "category": "Category 1",
      "content_path": "/path/to/content1",
      "thumbnail": "/path/to/thumbnail1",
      "subtitle": "Subtitle 1"
    }
```

Update Article

    Endpoint: /articles/{article_id}
    Method: PUT
  Request Body:

  ```json

{
  "name": "Updated Article",
  "tags": ["tag1", "tag2"],
  "creation_date": "2023-05-27T12:00:00",
  "modification_date": "2023-05-28T12:00:00",
  "publication_date": null,
  "category": "Category 1",
  "content_path": "/path/to/updated_content",
  "thumbnail": "/path/to/updated_thumbnail",
  "subtitle": "Updated Subtitle"
}
```

Response:

```json

    {
      "id": "generated-uuid",
      "name": "Updated Article",
      "tags": ["tag1", "tag2"],
      "creation_date": "2023-05-27T12:00:00",
      "modification_date": "2023-05-28T12:00:00",
      "publication_date": null,
      "category": "Category 1",
      "content_path": "/path/to/updated_content",
      "thumbnail": "/path/to/updated_thumbnail",
      "subtitle": "Updated Subtitle"
    }
```
Delete Article

    Endpoint: /articles/{article_id}
    Method: DELETE
  Response:

  ```json

{
  "message": "Article deleted successfully"
}

```
