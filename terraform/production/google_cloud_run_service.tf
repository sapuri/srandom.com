resource "google_cloud_run_service" "app" {
  name     = "app"
  location = local.region

  autogenerate_revision_name = true

  template {
    spec {
      containers {
        image = "asia-northeast1-docker.pkg.dev/srandom/app/app"

        resources {
          limits = { "memory" : "1G", "cpu" : "2000m" }
        }
      }

      service_account_name = google_service_account.cloud_run_app.email
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "2"
      }
    }
  }

  lifecycle {
    ignore_changes = [
      metadata,
      template.0.spec.0.containers.0.image,
      template.0.metadata.0.annotations["client.knative.dev/user-image"],
      template.0.metadata.0.annotations["run.googleapis.com/client-name"],
      template.0.metadata.0.annotations["run.googleapis.com/client-version"],
      traffic,
    ]
  }
}
