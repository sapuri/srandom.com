import {
  to = google_service_account_iam_binding.github_workload_identity
  id = "projects/srandom/serviceAccounts/github@srandom.iam.gserviceaccount.com roles/iam.workloadIdentityUser"
}

# Authoritative for this role: REPLACE the old pool/* grant, rather than add another.
resource "google_service_account_iam_binding" "github_workload_identity" {
  service_account_id = google_service_account.github.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository_id/57981173",
  ]
}
