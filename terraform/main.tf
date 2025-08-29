terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket" {
  description = "S3 bucket for data lake storage"
  type        = string
  default     = "example-bucket"
}

resource "aws_glue_catalog_database" "curated" {
  name = "curated"
}

resource "aws_glue_catalog_database" "features" {
  name = "features"
}

resource "aws_glue_catalog_table" "curated" {
  name          = "curated"
  database_name = aws_glue_catalog_database.curated.name
  table_type    = "EXTERNAL_TABLE"
  parameters = {
    classification = "delta"
  }
  storage_descriptor {
    location      = "s3://${var.s3_bucket}/curated"
    input_format  = "io.delta.sql.DeltaInputFormat"
    output_format = "io.delta.sql.DeltaOutputFormat"
    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }
  }
  partition_keys {
    name = "period"
    type = "string"
  }
}

resource "aws_glue_catalog_table" "features" {
  name          = "features"
  database_name = aws_glue_catalog_database.features.name
  table_type    = "EXTERNAL_TABLE"
  parameters = {
    classification = "delta"
  }
  storage_descriptor {
    location      = "s3://${var.s3_bucket}/features"
    input_format  = "io.delta.sql.DeltaInputFormat"
    output_format = "io.delta.sql.DeltaOutputFormat"
    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }
  }
  partition_keys {
    name = "period"
    type = "string"
  }
}

resource "aws_iam_role" "glue" {
  name = "glue-minimal-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "glue.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "glue" {
  name = "glue-minimal-policy"
  role = aws_iam_role.glue.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = "arn:aws:s3:::${var.s3_bucket}"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = "arn:aws:s3:::${var.s3_bucket}/*"
      },
      {
        Effect   = "Allow"
        Action   = ["glue:*"]
        Resource = "*"
      }
    ]
  })
}
