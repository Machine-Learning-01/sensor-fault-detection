resource "aws_eip" "elastic_ip" {
  vpc      = var.app_eip_vpc
  instance = aws_instance.app_instance.id
  tags = {
    Name = var.app_eip_name
  }
}