resource "google_storage_bucket_iam_member" "all_users_are_legacy_object_reader_of_static" {
  bucket = google_storage_bucket.static.name
  role   = "roles/storage.legacyObjectReader"
  member = "allUsers"
}

resource "google_storage_bucket_iam_member" "cloud_run_app_is_storage_admin_of_internal" {
  bucket = google_storage_bucket.internal.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.cloud_run_app.email}"
}
