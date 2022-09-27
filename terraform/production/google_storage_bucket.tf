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

resource "google_storage_bucket" "static" {
  name     = "${local.gcp_project_id}-static"
  location = local.region

  cors {
    max_age_seconds = 3600
    method          = ["GET"]
    origin = [
      "http://127.0.0.1:8000",
      "https://app-4ibqittu2a-an.a.run.app",
      "https://srandom.com",
    ]
    response_header = [
      "Content-Type",
      "Access-Control-Allow-Origin",
    ]
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
