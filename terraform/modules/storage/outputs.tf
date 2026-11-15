output "bucket_name" {
  description = "Name of the provisioned bucket"
  value       = google_storage_bucket.this.name
}

output "bucket_url" {
  description = "GCS URL of the bucket"
  value       = google_storage_bucket.this.url
}
