variable "bucket_name" {
  description = "Globally unique name of the GCS bucket"
  type        = string
}

variable "location" {
  description = "GCP bucket location"
  type        = string
  default     = "US-CENTRAL1"
}
