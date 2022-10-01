resource "google_monitoring_alert_policy" "cloud_run_app_warning_count" {
  display_name = "[srandom] Warning log count is high"
  combiner     = "OR"
  conditions {
    display_name = "logging/user/cloud-run-app-warning [COUNT]"
    condition_threshold {
      threshold_value = 10
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      trigger {
        count = 1
      }
      aggregations {
        alignment_period   = "600s"
        per_series_aligner = "ALIGN_COUNT"
      }
      filter = "metric.type=\"logging.googleapis.com/user/cloud-run-app-warning\" resource.type=\"cloud_run_revision\""
    }
  }
  notification_channels = [
    "projects/srandom/notificationChannels/2775302667456552373"
  ]
  alert_strategy {
    auto_close = "259200s"
  }
}


resource "google_monitoring_alert_policy" "cloud_run_app_error_count" {
  display_name = "[srandom] An error log is detected"
  combiner     = "OR"
  conditions {
    display_name = "logging/user/cloud-run-app-error [COUNT]"
    condition_threshold {
      threshold_value = 1
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      trigger {
        count = 1
      }
      aggregations {
        alignment_period   = "600s"
        per_series_aligner = "ALIGN_COUNT"
      }
      filter = "metric.type=\"logging.googleapis.com/user/cloud-run-app-error\" resource.type=\"cloud_run_revision\""
    }
  }
  notification_channels = [
    "projects/srandom/notificationChannels/2775302667456552373"
  ]
  alert_strategy {
    auto_close = "259200s"
  }
}

resource "google_monitoring_alert_policy" "cloud_run_job_export2csv_error_count" {
  display_name = "[export2csv] An error log is detected"
  combiner     = "OR"
  conditions {
    display_name = "logging/user/cloud-run-job-export2csv-error [COUNT]"
    condition_threshold {
      threshold_value = 1
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      trigger {
        count = 1
      }
      aggregations {
        alignment_period   = "600s"
        per_series_aligner = "ALIGN_COUNT"
      }
      filter = "metric.type=\"logging.googleapis.com/user/cloud-run-job-export2csv-error\" resource.type=\"cloud_run_job\""
    }
  }
  notification_channels = [
    "projects/srandom/notificationChannels/2775302667456552373"
  ]
  alert_strategy {
    auto_close = "259200s"
  }
}

resource "google_monitoring_alert_policy" "cloud_run_job_update_music_error_count" {
  display_name = "[update-music] An error log is detected"
  combiner     = "OR"
  conditions {
    display_name = "logging/user/cloud-run-job-update-music-error [COUNT]"
    condition_threshold {
      threshold_value = 1
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      trigger {
        count = 1
      }
      aggregations {
        alignment_period   = "600s"
        per_series_aligner = "ALIGN_COUNT"
      }
      filter = "metric.type=\"logging.googleapis.com/user/cloud-run-job-update-music-error\" resource.type=\"cloud_run_job\""
    }
  }
  notification_channels = [
    "projects/srandom/notificationChannels/2775302667456552373"
  ]
  alert_strategy {
    auto_close = "259200s"
  }
}
