output "igw_id" {
  description = "ID del Internet Gateway"
  value       = aws_internet_gateway.igw.id
}

output "vpc_id" {
  description = "ID del VPC"
  value       = aws_vpc.main.id
}