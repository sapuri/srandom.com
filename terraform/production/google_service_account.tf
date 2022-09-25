resource "google_service_account" "cloud_run_app" {
  account_id   = "cloud-run-app"
  display_name = "Cloud Run 'app' service account"
}

resource "google_service_account" "github" {
  account_id   = "github"
  display_name = "github"
}
