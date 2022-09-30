resource "google_kms_crypto_key" "app_env" {
  name     = "env"
  key_ring = google_kms_key_ring.app.id

  lifecycle {
    prevent_destroy = true
  }
}
