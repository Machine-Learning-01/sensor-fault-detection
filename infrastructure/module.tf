terraform {
  backend "s3" {
    bucket = "Sensor-truck-tf-state"
    key    = "tf_state"
    region = "us-east-1"
  }
}

module "sensor_ec2" {
  source = "./sensor_ec2"
}