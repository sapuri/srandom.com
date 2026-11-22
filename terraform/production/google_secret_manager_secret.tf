variable "production_env_secret_version" {
  description = "Numeric app-env version mounted at runtime; also update ENV_SECRET_VERSION in app.yml."
  type        = string
  default     = "1"
  validation {
    condition     = can(regex("^[1-9][0-9]*$", var.production_env_secret_version))
    error_message = "Use an explicit, positive secret version; do not use latest."
  }
}

# Only metadata is managed here. Upload the payload separately so Terraform state
# and plans never contain the production environment or credentials.
resource "google_secret_manager_secret" "production_env" {
  secret_id = "app-env"
  replication {
    user_managed {
      replicas {
        location = local.region
      }
    }
  }

  depends_on = [google_project_service.secretmanager]
  lifecycle {
    prevent_destroy = true
  }
}

resource "google_secret_manager_secret_iam_member" "runtime_env_reader" {
  secret_id = google_secret_manager_secret.production_env.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_app.email}"
}
