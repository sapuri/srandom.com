resource "google_cloud_scheduler_job" "update-music" {
  name             = "update-music"
  description      = "Cloud Run Job: update-music"
  schedule         = "5 0 * * *" # At 0:05
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "1200s" # 20m

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = "https://asia-northeast1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/srandom/jobs/update-music:run"

    oauth_token {
      service_account_email = "682889726379-compute@developer.gserviceaccount.com" # Default compute service account
    }
  }
}

resource "google_cloud_scheduler_job" "export2csv" {
  name             = "export2csv"
  description      = "Cloud Run Job: export2csv"
  schedule         = "20 0 * * *" # At 0:20
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "1800s" # 30m

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = "https://asia-northeast1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/srandom/jobs/export2csv:run"

    oauth_token {
      service_account_email = "682889726379-compute@developer.gserviceaccount.com" # Default compute service account
    }
  }
}
