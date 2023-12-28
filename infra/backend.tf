terraform {
    backend "s3" {
      bucket = "wiliot-locations-tfstate"
      key = "state/terraform.tfstate"
      region = "eu-west-1"
      encrypt = true
      dynamodb_table = "wiliot-locations-tf-lock"
    }
}