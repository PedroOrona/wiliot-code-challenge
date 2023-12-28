# wiliot-code-challenge

This repository presents a Python application that server HTTP requests at the routes `8080:/` and `8080:/health`.

The first one returns local time in specified locations (the default ones are New York, Berlin and Tokyo) in HTML format, and the second one return status code 200 in JSON format. 

We also provide the following:

1. Dockerfile that defines the container that will run the Python application;
2. Terraform templates to define and build the necessary infrastructure to run this app at an AWS EKS Cluster;
3. Helm chart that defines the required Kubernetes objects to run this app at the Kubernetes cluster.

## Requirements

- Python 3.9 (Download [here](https://www.python.org/downloads/))
- Docker (Installation guide [here](https://docs.docker.com/get-docker/))
- AWS CLI configured (Installation guide [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- Terraform 
- Kubectl
- Helm

## Development

1. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. Install the python requirements:

    ```bash
    pip install -r app/requirements.txt
    ```

3. Run the application:
    ```bash
    python app/app.py
    ```
    and you can check in your browser the HTTP server in action by accessing `localhost:8080`.

## Infrastructure

First, make sure that you have configured the AWS CLI profile that will be used to create the infrastructure. If you're not using the default one, specify int the `infra/main.tf` file your profile name on the aws provider definition.

Then, to build the necessary infrastructure, do the following:

1. Initialize the Terraform working directory:
    ```bash
    cd infra
    terraform init
    ```

2. Validate the templates:
    ```bash
    terraform validate
    ```

3. Check which resources terraform will create, change or destroy by running:
    ```bash
    terraform plan
    ```

4. Create (or update) the infrastructure by running:
    ```bash
    terraform apply
    ```

## Deploy

1. Build the docker image by running the following:
    ```bash
    docker build . -t wiliot
    ```

2. Push the docker image to ECR. To do it, follow the instructions [here](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html), and please, name the `tag` image as `latest`.

3. if you are accessing the cluster for the first time, run the following:
    ```bash
    aws eks update-kubeconfig — region <region> — name <eks-cluster-name> — profile <aws-profile>
    ```

    then confirm thatt you have access to the Kubernetes cluster by running:
    ```bash
    kubectl config current-context
    ```

4. Create the kubernetes objects by running the following:
    ```bash
    helm install wiliot-chart helm --values helm/values.yaml -n location
    ```

    or if you have changes at the helm chart that you want do deploy, run the following:

    ```bash
    helm upgrade wiliot-chart helm --values helm/values.yaml -n location
    ```

5. Get the URL to access the app externally by running the following:

    ```bash
    kubectl get services wiliot-chart \
        --namespace location \
        --output jsonpath='{.status.loadBalancer.ingress[0].ip}'
    ```

## Clean

1. Delete all the Kubernetes resources by running:
    ```bash
    helm uninstall wiliot-chart
    ```

2. Destroy the infrastructure by running:
    ```bash
    terraform destroy
    ```
