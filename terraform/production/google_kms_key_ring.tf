resource "google_kms_key_ring" "app" {
  name     = "app"
  location = "asia-northeast1"
}
