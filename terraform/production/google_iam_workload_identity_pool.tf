# Adopt the existing trust configuration; do not leave the permissive provider behind.
import {
  to = google_iam_workload_identity_pool.github
  id = "projects/682889726379/locations/global/workloadIdentityPools/github-actions"
}

import {
  to = google_iam_workload_identity_pool_provider.github
  id = "projects/682889726379/locations/global/workloadIdentityPools/github-actions/providers/github-actions"
}

import {
  to = google_service_account_iam_binding.github_workload_identity
  id = "projects/srandom/serviceAccounts/github@srandom.iam.gserviceaccount.com roles/iam.workloadIdentityUser"
}

resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-actions"
  display_name              = "GitHub Actions"
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

# Authoritative for this role: REPLACE the old pool/* grant, rather than add another.
resource "google_service_account_iam_binding" "github_workload_identity" {
  service_account_id = google_service_account.github.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository_id/57981173",
  ]
}
