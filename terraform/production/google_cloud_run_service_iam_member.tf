resource "google_cloud_run_service_iam_member" "allow_unauthenticated_invocation_app" {
  location = google_cloud_run_service.app.location
  service  = google_cloud_run_service.app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service_iam_member" "github_deployer" {
  project  = local.gcp_project_id
  location = local.region
  service  = google_cloud_run_service.app.name
  role     = "roles/run.developer"
  member   = google_service_account.github.member
}
