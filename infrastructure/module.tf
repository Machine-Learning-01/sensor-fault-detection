terraform {
  backend "s3" {
    bucket = "sensor-tf-state"
    key    = "tf_state"
    region = "us-east-1"
  }
}

module "sensor_ec2" {
  source = "./sensor_ec2"
}

module "sensor_io_files_bucket" {
  source = "./sensor_io_files_bucket"
}

module "sensor_ecr" {
  source = "./sensor_ecr"
}
