# Create a Docker file, push it to ECR and run it on Kubernetes

Detailed instructions can be found in the Kindle book
[ECR, EKS and Python Docker images: A step by step guide to deploying to Kubernetes in AWS](https://www.amazon.com/ECR-EKS-Python-Docker-images-ebook/dp/B089JDPB86/ref=sr_1_5?dchild=1&keywords=matthew+casperson&qid=1591219209&sr=8-5).

# Commands and notes

* install flask python library:<br>
pip3 install flask
* test Python web app locally:<br>
python3 app.py
* build docker image:<br>
docker build . -t pythonhelloworld
* test Python web app running in local Docker:<br>
docker run -p 8080:8080 pythonhelloworld
* create IAM user "KubernetesAdmin" with admin permissions
* use access and secret key of KubernetesAdmin:<br>
aws configure<br>
and check that you are "KubernetesAdmin"<br>
aws sts get-caller-identity
* create ECR repository:<br>
aws ecr create-repository --repository-name pythonhelloworld
* log into AWS ECR<br>
(aws ecr get-login is deprecated, use aws ecr get-login-password instead):<br>
aws ecr get-login-password \
| docker login \
    --username AWS \
    --password-stdin 094033154904.dkr.ecr.eu-west-1.amazonaws.com
* tag Docker image:<br>
docker tag pythonhelloworld 094033154904.dkr.ecr.eu-west-1.amazonaws.com/pythonhelloworld
* push Docker image to ECR:<br>
docker push 094033154904.dkr.ecr.eu-west-1.amazonaws.com/pythonhelloworld
* create EKS cluster role "EKSRole" with AmazonEKSServiceRolePolicy and AmazonEKSClusterPolicy (Trust Relationships set to eks.amazonaws.com)
* create EC2 role "EKSNodeRole" with AmazonEKSWorkerNodePolicy, AmazonEKS_CNI_Policy and AmazonEC2ContainerRegistryReadOnly policy  (Trust Relationships set to ec2.amazonaws.com)
* create a VPC "EKSVPC" with a single public subnet in AZ a using the AWS console wizard
* add another subnet to this VPC with CIDR 10.0.1.0/24 in AZ b
* for second subnet, add route to Internet Gateway: 0.0.0.0/0 => igw
* for both subnets, auto-assign public ip4 address
* add a security group for this VPC with port 443 open for all traffic (0.0.0.0/0) in the new VPC
* create key pair and download it
* create EKS cluster "CloudGuidesEKS" linked to the VPC, subnets, "EKSRole" and security group:<br>
aws eks create-cluster \
   --region eu-west-1 \
   --name CloudGuidesEKS2 \
   --kubernetes-version 1.16 \
   --role-arn arn:aws:iam::094033154904:role/EKSRole \
   --resources-vpc-config subnetIds=subnet-0efb86813f8213218,subnet-0b75bcf7ea0d4c711,securityGroupIds=sg-0daaf335839a8c338
check with
aws eks describe-cluster CloudGuidesEKS
* add EKS worker nodes: set name to "EKSNodeGroup", set role to EKSNodeRole, set ssh key and leave the rest to its defaults
* configure kubectl (download kubectl and create ~/.kub/config):<br>
curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.14.6/2019-08-22/bin/darwin/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin
aws eks --region eu-west-1 update-kubeconfig --name CloudGuidesEKS
kubectl get svc
kubectl get nodes
* deploy Kubernetes pod:<br>
kubectl apply -f deployment.yaml
kubectl get deployment cloudguide-deployment -o yaml
kubectl get pods
* deploy Kubernetes service (adds an ELB so that we can reach the pod from outside):<br>
kubectl apply -f service.yaml
kubectl get service cloudguide-service
* test the app running on Docker in a Kubernetes cluster in the browser (use the output from the last command):<br>
a83db63935a0e4de0ad8460e1971db19-1300743338.eu-west-1.elb.amazonaws.com
should return "Hello world!"

With this we have successfully written, compiled and packaged a custom application (simple web server) as a Docker image, and deployed a complete Kubernetes stack hosted in AWS with an ECR instance hosting our Docker image and EKS hosting our Kubernetes cluster.
