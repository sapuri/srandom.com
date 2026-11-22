resource "google_cloud_run_service" "app" {
  name     = "app"
  location = local.region

  autogenerate_revision_name = true
  depends_on                 = [google_secret_manager_secret_iam_member.runtime_env_reader]

  template {
    spec {
      containers {
        image = "asia-northeast1-docker.pkg.dev/srandom/app/app"

        env {
          name  = "APP_ENV_FILE"
          value = "/etc/srandom/production.env"
        }

        volume_mounts {
          name       = "production-env"
          mount_path = "/etc/srandom"
        }

        resources {
          limits = { "memory" : "256Mi", "cpu" : "1000m" }
        }
      }

      volumes {
        name = "production-env"
        secret {
          secret_name = google_secret_manager_secret.production_env.secret_id
          items {
            key  = var.production_env_secret_version
            path = "production.env"
          }
        }
      }

      service_account_name = google_service_account.cloud_run_app.email
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "3"
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
