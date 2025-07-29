# resource "aws_security_group" "redshift_sg" {
#   name   = "redshift-sg"
#   vpc_id = var.vpc_id

#   ingress {
#     from_port       = 5439
#     to_port         = 5439
#     protocol        = "tcp"
#     security_groups = [aws_security_group.lambda_sg.id]
#     description     = "Allow Lambda to access Redshift"
#   }

#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }
