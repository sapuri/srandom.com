# CI only publishes this application. It must not administer project IAM, state,
# KMS keys, Cloud Build, unrelated buckets or other runtime service accounts.
resource "google_artifact_registry_repository_iam_member" "github_writer" {
  project    = local.gcp_project_id
  location   = local.region
  repository = google_artifact_registry_repository.app.repository_id
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.github.email}"
}

resource "google_storage_bucket_iam_member" "github_static_publisher" {
  bucket = google_storage_bucket.static_srandom_com.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.github.email}"
}

resource "google_cloud_run_service_iam_member" "github_deployer" {
  project  = local.gcp_project_id
  location = local.region
  service  = google_cloud_run_service.app.name
  role     = "roles/run.developer"
  member   = "serviceAccount:${google_service_account.github.email}"
}

resource "google_cloud_run_v2_job_iam_member" "github_deployer" {
  for_each = toset(["update-music", "export2csv"])
  project  = local.gcp_project_id
  location = local.region
  name     = each.value
  role     = "roles/run.developer"
  member   = "serviceAccount:${google_service_account.github.email}"
}

resource "google_service_account_iam_member" "github_runtime_user" {
  service_account_id = google_service_account.cloud_run_app.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.github.email}"
}
