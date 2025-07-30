provider "digitalocean" {
  token = var.do_api_key
  spaces_access_id = var.do_spaces_access_id
  spaces_secret_key = var.do_spaces_secret_key
}
