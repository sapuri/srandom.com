resource "google_logging_metric" "cloud_run_app_warning" {
  name        = "cloud-run-app-warning"
  description = "Warning log count of Cloud Run 'app'"
  filter      = "resource.type = \"cloud_run_revision\" AND resource.labels.service_name = \"app\" AND severity = \"WARNING\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
  }
}

resource "google_logging_metric" "cloud_run_app_error" {
  name        = "cloud-run-app-error"
  description = "Error log count of Cloud Run 'app'"
  filter      = "resource.type = \"cloud_run_revision\" AND resource.labels.service_name = \"app\" AND severity >= \"ERROR\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
  }
}

resource "google_logging_metric" "cloud_run_job_export2csv_error" {
  name        = "cloud-run-job-export2csv-error"
  description = "Error log count of Cloud Run Job 'export2csv'"
  filter      = "resource.type = \"cloud_run_job\" AND resource.labels.job_name = \"export2csv\" AND severity >= \"ERROR\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
  }
}

resource "google_logging_metric" "cloud_run_job_update_music_error" {
  name        = "cloud-run-job-update-music-error"
  description = "Error log count of Cloud Run Job 'update-music'"
  filter      = "resource.type = \"cloud_run_job\" AND resource.labels.job_name = \"update-music\" AND severity >= \"ERROR\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
  }
}
