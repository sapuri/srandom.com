resource "google_storage_bucket" "tfstate" {
  name     = "${local.gcp_project_id}-tfstate"
  location = local.region

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      num_newer_versions = 5
    }
  }
}

resource "google_storage_bucket" "internal" {
  name     = "${local.gcp_project_id}-internal"
  location = local.region

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      num_newer_versions = 5
    }
  }
}
