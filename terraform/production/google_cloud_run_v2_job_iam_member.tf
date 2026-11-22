resource "google_cloud_run_v2_job_iam_member" "github_deployer" {
  for_each = toset(["update-music", "export2csv"])
  project  = local.gcp_project_id
  location = local.region
  name     = each.value
  role     = "roles/run.developer"
  member   = "serviceAccount:${google_service_account.github.email}"
}
