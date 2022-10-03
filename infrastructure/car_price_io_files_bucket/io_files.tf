resource "aws_s3_bucket" "io_files" {
  bucket        = var.io_files
  force_destroy = var.force_destroy_bucket
}