# create zip file from requirements.txt. Triggers only when the file is updated
# resource "random_string" "random_suffix" {
#   length  = 8
#   special = false
#   upper   = false
#   keepers = {
#     requirements = filesha1("${var.app_path}/requirements.txt")
#   }
# }

resource "null_resource" "lambda_layer" {

  triggers = {
    requirements = filesha1("${var.app_path}/requirements.txt")
  }
  # the command to install python and dependencies to the machine and zips
  provisioner "local-exec" {
    command = <<EOT
        echo "creating layers with requirements.txt packages..."

        cd ${var.app_path}/.tftemp
        rm -rf layers
        mkdir layers
        cd layers
        cp ${var.app_path}/requirements.txt .

        ${var.runtime} -m venv python
        . python/bin/activate

        # Installing python dependencies...
        if [ -f requirements.txt ]; then
            echo "From: requirement.txt file exists..."  

            pip install -r requirements.txt
            zip -r PythonRequirements-${var.common.service_name}-${var.common.environment}.zip python/
         else
            echo "Error: requirement.txt does not exist!"
        fi

        # Deactivate virtual environment...
        deactivate

        #deleting the python dist package modules
        rm -rf python
        
    EOT
  }
}

# upload zip file to s3
resource "aws_s3_object" "lambda_layer_zip" {

  bucket     = aws_s3_bucket.lambda_s3.bucket
  key        = "layers/PythonRequirements-${var.common.service_name}-${var.common.environment}.zip"
  source     = "${var.app_path}/.tftemp/layers/PythonRequirements-${var.common.service_name}-${var.common.environment}.zip"
  source_hash = filemd5("${var.app_path}/requirements.txt")
  depends_on = [null_resource.lambda_layer] # triggered only if the zip file is created

  tags       = var.common.default_tags
}

# create lambda layer from s3 object
resource "aws_lambda_layer_version" "this" {
  
  s3_bucket           = aws_s3_bucket.lambda_s3.bucket
  s3_key              = aws_s3_object.lambda_layer_zip.key
  layer_name          = "${var.common.project_code}-PythonRequirements-${var.common.service_name}-${var.common.environment}-lambda-layer-01" # Change this if increment
  compatible_runtimes = ["${var.runtime}"]
  skip_destroy        = true
  source_code_hash    = filebase64sha256("${var.app_path}/requirements.txt")
  depends_on          = [aws_s3_object.lambda_layer_zip] # triggered only if the zip file is uploaded to the bucket
}

# resource "null_resource" "cleanup_lambda_layer_zip" {

#   provisioner "local-exec" {
#     command = <<EOT
#       echo "Cleaning up the created zip file..."
#       rm -f ${var.app_path}/.tftemp/layers/PythonRequirements-${var.common.service_name}-${var.common.environment}.zip
#     EOT
#   }

#   depends_on = [aws_lambda_layer_version.this]
# }
