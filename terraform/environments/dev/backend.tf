terraform {
  required_version = ">= 1.5.0"

  backend "gcs" {
    bucket = "hd-retail-intelligence-2026-tfstate"
    prefix = "home-depot/dev"
  }
}
