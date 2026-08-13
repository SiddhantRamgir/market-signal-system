locals {
  image_name = "ghcr.io/${lower(var.github_username)}/market-signal-system:${var.image_tag}"
}