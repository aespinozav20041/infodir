terraform {
  required_providers {
    weaviate = {
      source  = "semi-technologies/weaviate"
      version = "~> 0.8"
    }
  }
}

provider "weaviate" {
  # Authentication via WEAVIATE_API_KEY environment variable
}

resource "weaviate_cluster" "this" {
  name     = var.name
  tier     = var.tier
  replicas = var.replicas
  shards   = var.shards
}
