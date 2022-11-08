terraform {
  backend "s3" {
    bucket = "sensor-tf-state"
    key    = "tf_state"
    region = "ap-south-1"
  }
}

module "sensor_ec2" {
  source = "./sensor_ec2"
}

module "sensor_model" {
  source = "./sensor_model_bucket"
}

module "sensor_ecr" {
  source = "./sensor_ecr"
}

module "sensor_pred_data" {
  source = "./sensor_pred_data_bucket"
}