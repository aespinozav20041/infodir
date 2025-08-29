# Vector Store Evaluation

This repository evaluates **Milvus**, **Weaviate** and **PostgreSQL + pgvector** as
vector database options. A small abstraction layer in `vector_store/` exposes a
common API which is served through FastAPI for indexing and querying
embeddings.

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the service (defaults to Weaviate backend):

```bash
uvicorn api:app --reload
```

Select the backend by setting the `VECTOR_STORE` environment variable to one of
`milvus`, `weaviate` or `pgvector`.

## Terraform

The `terraform/` directory contains a sample configuration for provisioning a
managed Weaviate cluster with configurable replication and shard counts.

## Evaluation

- **Milvus** – high performance, standalone vector database with IVF indexes.
- **Weaviate** – cloud service with built-in semantic search capabilities.
- **Postgres + pgvector** – leverages existing Postgres deployments and SQL.
