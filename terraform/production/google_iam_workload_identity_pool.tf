import {
  to = google_iam_workload_identity_pool.github
  id = "projects/682889726379/locations/global/workloadIdentityPools/github-actions"
}

resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-actions"
  display_name              = "GitHub Actions"
}
