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
