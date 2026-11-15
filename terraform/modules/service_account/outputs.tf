output "email" {
  description = "Service account email address"
  value       = google_service_account.this.email
}

output "member" {
  description = "IAM principal identifier for the service account"
  value       = google_service_account.this.member
}
