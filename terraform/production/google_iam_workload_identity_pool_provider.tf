import {
  to = google_iam_workload_identity_pool_provider.github
  id = "projects/682889726379/locations/global/workloadIdentityPools/github-actions/providers/github-actions"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-actions"
  display_name                       = "GitHub Actions"

  attribute_mapping = {
    "google.subject"                = "assertion.sub"
    "attribute.repository"          = "assertion.repository"
    "attribute.repository_id"       = "assertion.repository_id"
    "attribute.repository_owner_id" = "assertion.repository_owner_id"
  }
  attribute_condition = file("${path.module}/github-actions-condition.cel")

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}
