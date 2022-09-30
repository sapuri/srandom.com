resource "google_dns_managed_zone" "srandom_com" {
  name        = "srandom-com"
  dns_name    = "srandom.com."
  description = "srandom.com. DNS zone"
}
