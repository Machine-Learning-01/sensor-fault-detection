terraform {
  backend "s3" {
    bucket = "Sensor-truck-tf-state"
    key    = "tf_state"
    region = "us-east-1"
  }
}

module "Sensor_truck_ec2" {
  source = "./Sensor_truck_ec2"
}