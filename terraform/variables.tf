variable "name" {
  description = "Cluster name"
  type        = string
  default     = "vector-store"
}

variable "tier" {
  description = "Service tier"
  type        = string
  default     = "sandbox"
}

variable "replicas" {
  description = "Number of replicas"
  type        = number
  default     = 1
}

variable "shards" {
  description = "Number of shards per class"
  type        = number
  default     = 1
}
