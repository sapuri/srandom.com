#
# srandom.com
#
resource "google_dns_record_set" "srandom_com_a" {
  name         = google_dns_managed_zone.srandom_com.dns_name
  managed_zone = google_dns_managed_zone.srandom_com.name
  type         = "A"
  rrdatas      = ["216.239.32.21", "216.239.34.21", "216.239.36.21", "216.239.38.21"] # Cloud Run
  ttl          = 3600
}

resource "google_dns_record_set" "srandom_com_aaaa" {
  name         = google_dns_managed_zone.srandom_com.dns_name
  managed_zone = google_dns_managed_zone.srandom_com.name
  type         = "AAAA"
  rrdatas      = ["2001:4860:4802:32::15", "2001:4860:4802:34::15", "2001:4860:4802:36::15", "2001:4860:4802:38::15"] # Cloud Run
  ttl          = 3600
}

#
# static.srandom.com
#
resource "google_dns_record_set" "static_srandom_com_cname" {
  name         = "static.${google_dns_managed_zone.srandom_com.dns_name}"
  managed_zone = google_dns_managed_zone.srandom_com.name
  type         = "CNAME"
  rrdatas      = ["c.storage.googleapis.com."] # Cloud Storage
  ttl          = 3600
}
