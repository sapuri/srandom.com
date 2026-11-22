resource "google_service_account_iam_member" "github_runtime_user" {
  service_account_id = google_service_account.cloud_run_app.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.github.email}"
}
