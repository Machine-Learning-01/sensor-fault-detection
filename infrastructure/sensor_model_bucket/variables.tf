variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "model_bucket_name" {
  type    = string
  default = "sensor-model"
}

variable "aws_account_id" {
  type    = string
  default = "566373416292"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}

