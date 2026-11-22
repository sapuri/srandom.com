variable "production_env_secret_version" {
  description = "Numeric app-env version mounted at runtime; also update ENV_SECRET_VERSION in app.yml."
  type        = string
  default     = "1"
  validation {
    condition     = can(regex("^[1-9][0-9]*$", var.production_env_secret_version))
    error_message = "Use an explicit, positive secret version; do not use latest."
  }
}
