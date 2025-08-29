# Data Lake Integration

This repository demonstrates how to manage **curated** and **features** datasets
using [Delta Lake](https://delta.io/). The tables are partitioned by
`period=YYYY-MM` and optimized with Z-Ordering on the `term` column.

## Components

- `scripts/delta_setup.py` – creates Delta tables for curated and features data.
- `scripts/register_schema.py` – registers Avro schemas in Confluent Schema Registry.
- `terraform/` – Terraform configuration for Glue databases, tables and minimal IAM role.
- `schemas/` – Avro schema contracts for each dataset.

## Fuentes regulatorias

Para incorporar reportes oficiales, usa las APIs de **EDGAR**, **ESMA**, **CNMV**, **SMV**, **CVM**, etc. para descargar los documentos y normalizarlos antes de cargarlos en las tablas Delta.

## Usage

### Delta tables

```bash
python scripts/delta_setup.py
```

### Schema Registry

```bash
python scripts/register_schema.py
```

### Terraform

```bash
cd terraform
terraform init -backend=false
terraform apply
```

These examples use placeholder paths and URLs; adapt them to your environment.
