module "raw_storage" {
  source = "../../modules/storage"

  bucket_name = "hd-retail-intelligence-2026-raw"
  location    = "US-CENTRAL1"
}

module "curated_storage" {
  source = "../../modules/storage"

  bucket_name = "hd-retail-intelligence-2026-curated"
  location    = "US-CENTRAL1"
}

module "data_processor" {
  source = "../../modules/service_account"

  account_id   = "retail-data-processor"
  display_name = "Retail Data Processor"
}

resource "google_storage_bucket_iam_member" "raw_reader" {
  bucket = module.raw_storage.bucket_name
  role   = "roles/storage.objectViewer"
  member = module.data_processor.member
}

resource "google_storage_bucket_iam_member" "curated_writer" {
  bucket = module.curated_storage.bucket_name
  role   = "roles/storage.objectCreator"
  member = module.data_processor.member
}

resource "google_bigquery_dataset" "retail" {
  dataset_id  = "retail_intelligence"
  description = "Home Depot retail search intelligence analytics"
  location    = "US"

  labels = {
    environment = "dev"
    managed_by  = "terraform"
  }
}
