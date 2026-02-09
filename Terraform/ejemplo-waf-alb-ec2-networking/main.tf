resource "aws_vpc" "main" {
  cidr_block = "12.0.0.0/16"

  tags = {
    Name = "test-vpc-${var.environment}"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "igw-${var.environment}"
  }
}

resource "aws_subnet" "subnet_public_1a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "12.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "test-public-subnet-${var.environment}-1a"
  }
}

resource "aws_subnet" "subnet_public_1b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "12.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "test-public-subnet-${var.environment}-1b"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }


  tags = {
    Name = "test-public-rt-${var.environment}"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet_public_1a.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.subnet_public_1b.id
  route_table_id = aws_route_table.public_rt.id
}


#########################
# IAM Role + Instance Profile
#########################

data "aws_iam_policy_document" "ec2_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2_role" {
  name               = "test-${lower(var.environment)}-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_trust.json
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "test-${lower(var.environment)}-profile"
  role = aws_iam_role.ec2_role.name
}

resource "aws_iam_role_policy_attachment" "ec2_ssm_core" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_security_group" "web_sg" {
  name   = "web-sg-${var.environment}"
  vpc_id = aws_vpc.main.id

  ingress {
    description     = "HTTP"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.lb_sg.id]
  }


  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-sg-${var.environment}"
  }
}

#########################
# EC2 instance
#########################

resource "aws_instance" "ec2_cli" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.subnet_public_1a.id
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              dnf update -y
              sudo dnf install httpd -y
              echo "<h1>Server Details</h1><p><strong>Hostname:</strong> $(hostname)</p><p><strong>IP Address:</strong> $(hostname -I | cut -d' ' -f1)</p>" > /var/www/html/index.html
              sudo systemctl restart httpd
              sudo dnf install -y docker
              sudo systemctl enable docker
              sudo systemctl start docker
              sudo usermod -aG docker ec2-user

              # Asegurar que el SSM Agent está instalado y corriendo
              if ! systemctl status amazon-ssm-agent >/dev/null 2>&1; then
                dnf install -y amazon-ssm-agent
                systemctl enable amazon-ssm-agent
                systemctl start amazon-ssm-agent
              fi

              # Instalar AWS CLI v2 si no viene ya
              if ! command -v aws &> /dev/null
              then
                curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                unzip awscliv2.zip
                ./aws/install
              fi
              EOF
  tags = {
    Name        = "test-ec2-cli-${var.environment}"
    Environment = var.environment
  }
}

## Aplication load blancer
resource "aws_security_group" "lb_sg" {
  name   = "lb-sg-${var.environment}"
  vpc_id = aws_vpc.main.id

  ingress {
    description = "HTTP from internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "alb" {
  name               = "test-alb-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets = [
    aws_subnet.subnet_public_1a.id,
    aws_subnet.subnet_public_1b.id
  ]

  # OJO: si esta en true, luego no podrás borrar fácil el ALB
  enable_deletion_protection = false

  tags = {
    Environment = var.environment
  }
}

resource "aws_lb_target_group" "tg" {
  name     = "alb-tg-test-${var.environment}"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path = "/"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}

resource "aws_lb_target_group_attachment" "ec2" {
  target_group_arn = aws_lb_target_group.tg.arn
  target_id        = aws_instance.ec2_cli.id
  port             = 80
}

##### WAF

resource "aws_wafv2_ip_set" "ip_whitelist" {
  name               = "ip-whitelist-${var.environment}"
  scope              = "REGIONAL"
  ip_address_version = "IPV4"

  addresses = [
    "1.2.3.4/32",
    "5.6.7.0/24",
  ]

  tags = {
    Environment = var.environment
  }
}

resource "aws_wafv2_ip_set" "ip_blacklist" {
  name               = "ip-blacklist-${var.environment}"
  scope              = "REGIONAL"
  ip_address_version = "IPV4"

  addresses = [
    "11.22.33.44/32",
    "99.88.77.0/24",
  ]

  tags = {
    Environment = var.environment
  }
}

resource "aws_wafv2_web_acl" "alb_waf" {
  name  = "alb-waf-${var.environment}"
  scope = "REGIONAL"

  default_action {
    block {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "albWaf"
    sampled_requests_enabled   = true
  }

  # 0) BLOQUEAR IPs en blacklist (primero siempre)
  rule {
    name     = "BlockBlacklistedIPs"
    priority = 0

    action {
      block {}
    }

    statement {
      ip_set_reference_statement {
        arn = aws_wafv2_ip_set.ip_blacklist.arn
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "BlockIPs"
      sampled_requests_enabled   = true
    }
  }

  # 1) PERMITIR IPs en whitelist
  rule {
    name     = "AllowWhitelistedIPs"
    priority = 1

    action {
      allow {}
    }

    statement {
      ip_set_reference_statement {
        arn = aws_wafv2_ip_set.ip_whitelist.arn
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AllowIPs"
      sampled_requests_enabled   = true
    }
  }

  # 2) PERMITIR solo CO y AR
  rule {
    name     = "AllowCOandAR"
    priority = 2

    action {
      allow {}
    }

    statement {
      geo_match_statement {
        country_codes = ["CO", "AR"]
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AllowCOAR"
      sampled_requests_enabled   = true
    }
  }

  # 3) AWS Managed Rules
  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 3

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        vendor_name = "AWS"
        name        = "AWSManagedRulesCommonRuleSet"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "CommonRuleSet"
      sampled_requests_enabled   = true
    }
  }
}

## rules 
#Comportamiento final:
#
#❌ Blacklist → bloquea SIEMPRE (aunque sea CO/AR o whitelist)
#
#✅ Whitelist → permite
#
#✅ CO/AR → permite
#
#🛡️ Managed Rules → inspeccionan lo permitido
#
#❌ Todo lo demás → bloqueado por default_action

# Asociar WAF al ALB

resource "aws_wafv2_web_acl_association" "alb" {
  resource_arn = aws_lb.alb.arn
  web_acl_arn  = aws_wafv2_web_acl.alb_waf.arn
}
