terraform {
  backend "s3" {
    bucket = "scania-truck-tf-state"
    key    = "tf_state"
    region = "us-east-1"
  }
}

module "scania_truck_ec2" {
  source = "./scania_truck_ec2"
}