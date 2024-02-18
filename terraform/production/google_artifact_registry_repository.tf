resource "google_artifact_registry_repository" "app" {
  location      = local.region
  repository_id = "app"
  format        = "DOCKER"
  cleanup_policies {
    id     = "delete"
    action = "DELETE"
    condition {
      older_than = "86400s" # 1 day
    }
  }
  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count = 1
    }
  }
}

resource "google_artifact_registry_repository" "cmd" {
  location      = local.region
  repository_id = "cmd"
  format        = "DOCKER"
  cleanup_policies {
    id     = "delete"
    action = "DELETE"
    condition {
      older_than = "86400s" # 1 day
    }
  }
  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count = 1
    }
  }
}
