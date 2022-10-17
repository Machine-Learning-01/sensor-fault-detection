resource "aws_s3_bucket" "model" {
  bucket        = var.model
  force_destroy = var.force_destroy_bucket
}