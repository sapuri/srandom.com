resource "google_storage_bucket_iam_member" "all_users_are_legacy_object_reader_of_static" {
  bucket = google_storage_bucket.static.name
  role   = "roles/storage.legacyObjectReader"
  member = "allUsers"
}