resource "google_project_iam_member" "cloud_run_app_is_storage_object_admin" {
  project = local.gcp_project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.cloud_run_app.email}"
}

resource "google_project_iam_member" "github_is_storage_admin" {
  project = local.gcp_project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.github.email}"
}

resource "google_project_iam_member" "github_is_cloudkms_crypto_key_decrypter" {
  project = local.gcp_project_id
  role    = "roles/cloudkms.cryptoKeyDecrypter"
  member  = "serviceAccount:${google_service_account.github.email}"
}

resource "google_project_iam_member" "github_is_cloudbuild_builds_editor" {
  project = local.gcp_project_id
  role    = "roles/cloudbuild.builds.editor"
  member  = "serviceAccount:${google_service_account.github.email}"
}

resource "google_project_iam_member" "github_is_artifactregistry_writer" {
  project = local.gcp_project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.github.email}"
}

resource "google_project_iam_member" "github_is_run_admin" {
  project = local.gcp_project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.github.email}"
}

resource "google_project_iam_member" "github_is_service_account_user" {
  project = local.gcp_project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.github.email}"
}
