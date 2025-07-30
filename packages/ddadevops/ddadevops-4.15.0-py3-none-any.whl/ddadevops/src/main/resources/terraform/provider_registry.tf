terraform {
  required_providers {
     
    hcloud = {
      source = "hetznercloud/hcloud"
      version = ">= 1.41"
    }

    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.6"
    }

    hetznerdns = {
      source = "timohirt/hetznerdns"
      version = ">= 2.2"
    }

    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.28"
    }
  }
}