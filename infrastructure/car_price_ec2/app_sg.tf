resource "aws_security_group" "security_group" {
  name        = var.app_sg_group_name
  description = "Security Group for EKS Master Server"

  ingress {
    from_port   = var.app_ingress_from_port[0]
    to_port     = var.app_ingress_to_port[0]
    protocol    = var.app_protocol
    cidr_blocks = var.app_cidr_block
  }

  ingress {
    from_port   = var.app_ingress_from_port[1]
    to_port     = var.app_ingress_to_port[1]
    protocol    = var.app_protocol
    cidr_blocks = var.app_cidr_block
  }

  egress {
    from_port   = var.app_egress_from_port
    to_port     = var.app_egress_to_port
    protocol    = var.app_protocol
    cidr_blocks = var.app_cidr_block
  }

  tags = {
    Name = var.app_sg_group_name
  }
}