resource "google_artifact_registry_repository_iam_member" "github_writer" {
  project    = local.gcp_project_id
  location   = local.region
  repository = google_artifact_registry_repository.app.repository_id
  role       = "roles/artifactregistry.writer"
  member     = google_service_account.github.member
}
