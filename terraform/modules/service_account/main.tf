resource "google_service_account" "this" {
  account_id   = var.account_id
  display_name = var.display_name
  description  = "Service account for Home Depot retail data processing"
}
