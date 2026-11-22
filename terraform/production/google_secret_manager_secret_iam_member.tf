resource "google_secret_manager_secret_iam_member" "runtime_env_reader" {
  secret_id = google_secret_manager_secret.production_env.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_app.email}"
}
