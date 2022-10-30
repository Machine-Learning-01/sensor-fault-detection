provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "app_instance" {
  ami                    = var.app_ami
  instance_type          = var.app_instance_type
  key_name               = var.app_key_pair_name
  vpc_security_group_ids = [aws_security_group.security_group.id]

  tags = {
    Name = var.app_tag_name
  }

  root_block_device {
    volume_size = var.app_volume_size
    volume_type = var.app_volume_type
    encrypted   = var.app_volume_encryption
  }

  connection {
    type    = var.app_connection_type
    host    = self.public_ip
    user    = var.app_user
    timeout = var.app_timeout
  }
}