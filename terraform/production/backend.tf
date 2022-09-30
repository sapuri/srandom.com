terraform {
  backend "gcs" {
    bucket = "srandom-tfstate"
  }
}
