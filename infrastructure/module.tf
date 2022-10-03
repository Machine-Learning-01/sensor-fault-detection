terraform {
  backend "s3" {
    bucket = "car-price-tf-state"
    key    = "tf_state"
    region = "us-east-1"
  }
}

# module "io_files_bucket" {
#   source = "./car_price_io_files_bucket"
# }

# module "car_price_ecr" {
#   source = "./car_price_ecr"
# }

module "car_price_ec2" {
  source = "./car_price_ec2"
}