variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "app_ami" {
  type    = string
  default = "ami-0eb1f91977a3fcc1b"
}

variable "app_instance_type" {
  type    = string
  default = "t2.large"
}

variable "app_key_pair_name" {
  type    = string
  default = "ineuron"
}

variable "app_tag_name" {
  type    = string
  default = "Application Server"
}

variable "app_eip_name" {
  type    = string
  default = "app_ip"
}

variable "app_sg_group_name" {
  type    = string
  default = "app_sg_group"
}

variable "app_ingress_from_port" {
  type    = list(number)
  default = [22, 8080]
}

variable "app_cidr_block" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "app_protocol" {
  type    = string
  default = "tcp"
}

variable "app_ingress_to_port" {
  type    = list(number)
  default = [22, 8080]
}

variable "app_egress_from_port" {
  type    = number
  default = 0
}

variable "app_egress_to_port" {
  type    = number
  default = 65535
}

variable "app_volume_size" {
  default = 50
  type    = number
}

variable "app_volume_type" {
  default = "gp2"
  type    = string
}

variable "app_volume_encryption" {
  default = true
  type    = bool
}

variable "app_eip_vpc" {
  default = true
  type    = bool
}

variable "app_connection_type" {
  default = "ssh"
  type    = string
}

variable "app_user" {
  default = "ubuntu"
  type    = string
}

variable "app_timeout" {
  default = "4m"
  type    = string
}
