resource "google_storage_bucket" "this" {
  name          = var.bucket_name
  location      = var.location
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  labels = {
    project     = "retail-intelligence"
    environment = "dev"
    managed_by  = "terraform"
  }
}
