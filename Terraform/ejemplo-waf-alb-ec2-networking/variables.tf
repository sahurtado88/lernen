variable "aws_region" {
  default = "us-east-1"
  type    = string

}
variable "environment" {
  default = "dev"
  type    = string

}

variable "ami_id" {
  description = "AMI de la instancia (Amazon Linux 2 recomendado)"
  type        = string
  default     = "ami-0fa3fe0fa7920f68e"
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.small"
}