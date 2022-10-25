# Deploy DataHub using AWS managed services and ingest metadata from AWS Glue and Amazon Redshift
Here you can find the AWS Big Data Blog that is part of this code base .

[Part 1](https://aws.amazon.com/blogs/big-data/part-1-deploy-datahub-using-aws-managed-services-and-ingest-metadata-from-aws-glue-and-amazon-redshift/)
[Part 2](https://aws.amazon.com/blogs/big-data/part-2-deploy-datahub-using-aws-managed-services-and-ingest-metadata-from-aws-glue-and-amazon-redshift/)


# Section A :  Prerequisites​

We need kubectl,helm and AWS CLI to complete the setup of DataHub in AWS environment. We can execute all the instructions either from local desktop or using AWS Cloud9. If you are using AWS Cloud9 please follow below instruction to spin up AWS Cloud9 or 
else skip to installation of kubectl,helm and AWS CLI section.


## If you are using Cloud9

<em>**Note** Create a Cloud9 instance with instance type of t3.small and increase the default size from 10GB to 50GB. Follow the instructions on the Cloud9 documentation to resize your EBS volume to at least 50GB.</em> 

https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html#move-environment-resize



## This guide requires the installation of following cli tools, with following version:


* __kubectl__ -  to manage kubernetes resources



    <em>**version** - [Client Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.6"}]
    </em>

  For downloading a specific version
  ```
  sudo curl --silent --location -o /usr/local/bin/kubectl \
   https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.5/2022-01-21/bin/linux/amd64/kubectl

  sudo chmod +x /usr/local/bin/kubectl
    ```


  <em>**Note**
    
    For installing Kubectl in Cloud9 , Please follow the below instructions

    Cloud9 normally manages IAM credentials dynamically. This isn’t currently compatible with the EKS IAM authentication, so we will disable it and rely on the IAM role instead.
  </em>

  https://www.eksworkshop.com/020_prerequisites/k8stools/

  https://www.eksworkshop.com/020_prerequisites/iamrole/

  https://www.eksworkshop.com/020_prerequisites/ec2instance/

  https://www.eksworkshop.com/020_prerequisites/workspaceiam/


* __helm__ -  to deploy the resources based on helm 
charts.

  <em>**version**
  [version.BuildInfo{Version:"v3.9.3"}]
  </em>

  ```
  curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
  chmod 700 get_helm.sh
  DESIRED_VERSION=v3.9.3 ./get_helm.sh
  ```

* __AWS CLI__ -	Install AWS CLI (version 2.X.x) or migrate AWS CLI version 1 to version 2 - 
https://docs.aws.amazon.com/cli/latest/userguide/cliv2-migration.html



  ```
  aws --version
  ```
 this should point to aws cli version 2, if this is still pointing to older version close the terminal and start with a new terminal 



To use the above tools, you need to set up AWS credentials by following this [guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html).



## Service-linked role
Amazon ES uses IAM service-linked roles. A service-linked role is a unique type of IAM role that is linked directly to Amazon ES. Service-linked roles are predefined by Amazon ES and include all the permissions that the service requires to call other AWS services on your behalf. To create a service-linked role for Amazon ES, issue the following command:

```
aws iam create-service-linked-role --aws-service-name opensearchservice.amazonaws.com
```

# Section B : install cdk 2 /upgrade cdk 1 to cdk 2

## Installing and updating CDK

```
npm install -g aws-cdk@latest
```

*** In the case of error try to force it ***
```
npm install -g aws-cdk@latest --force
```

# Welcome to your CDK Python project!

clone the repo  - 
```
git clone https://github.com/aws-samples/deploy-datahub-using-aws-managed-services-ingest-metadata.git
cd deploy-datahub-using-aws-managed-services-ingest-metadata
```
### Important : Change cdk.json config values (ACCOUNT_ID, REGION) , cdk.json is present in the root directory of the code repo
And change the value of ACCOUNT_ID and REGION in cdk.json

```
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
python3 -m pip install -r requirements.txt
```

This is needed one time per account. If you have never executed this before, then run this

```
cdk bootstrap aws://<account-id>/<aws-region>

```

At this point you can now synthesize the CloudFormation template for this code.

```
cdk synth
```

Deploy

```
cdk deploy --all --require-approval never
```


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!




# Section C : Check Cfn output and service console to get the following credentials and URL

### EKS Details
pointing kubectl to newly created cluster

get the kubectl updateconfig command from EKS stack CfnOutput

 ```
  aws eks update-kubeconfig --region region-code --name cluster-name --role-arn
```

### Navigate to "Secrets Manager" and find the secret with name "MySqlInstancedatahubSecret****" and click "Retrieve secret value" button from "Secret value" section to get following
    password <pwd>
	dbname db1
	engine mysql
	port 3306
	dbInstanceIdentifier <identifier-name>
	host <host>
	username admin

### Navigate to "ES/OpenSearch" CFN Stack and get the following details from its output
		MasterPW <pwd>	
		MasterUser opensearch


### Navigate to OpenSearch service and get the Domain endpoint, which is in below format:
		vpc-opensearch-domain-datahub-<id>.<region>.es.amazonaws.com

### Navigate to MSK Service in AWS console and click your cluster i.e. "MSK-datahub"
     Copy the Zookeeper "Plaintext" connection Url
     Copy the broker "Plaintext" Connection Url 
      

# Section D:  installing datahub containers to provisioned EKS cluster
   
    1- create K8S secrets
    2- Change two config files to add the service information
    3- Helm deploy
    4- Expose endpoints using a load balancer​ [Optional]


## 1 - create K8S secrets

### Assuming kubectl context points to the correct kubernetes cluster, first create kubernetes secrets that contain MySQL and Elasticsearch passwords.

```
kubectl create secret generic mysql-secrets --from-literal=mysql-root-password=<replace here>
```
```
kubectl create secret generic elasticsearch-secrets --from-literal=elasticsearch-password=<replace here>
```

### Add datahub helm repo by running the following
```
helm repo add datahub https://helm.datahubproject.io/
```

```
helm repo update datahub
```

## 2- Change two config files to add the service information 
 
### Modify "kafka:" -> "bootstrapServers:" value in "./charts/prerequisites/values.yaml" with MSK broker URL copied from Section B

### Modify MySQL host, ES Domain and Kafka detail in "./charts/datahub/values.yaml" file copied from Section B


## 3- Helm deploy

 ```
 helm install prerequisites datahub/datahub-prerequisites --values ./charts/prerequisites/values.yaml --version 0.0.10
 ```

```
 helm install datahub datahub/datahub --values ./charts/datahub/values.yaml --version 0.2.108
```

Note: If you want to use newer [helm chart](https://github.com/acryldata/datahub-helm/blob/master/charts/datahub/values.yaml,), replace the following chart values from your existing values.yaml
•	elasticsearchSetupJob
•	global : graph_service_impl
•	global : elasticsearch
•	global :kafka
•	global :sql


### If installation failed, the debug with below commands to check the status of EKS cluster pods
### Confirm kubectl points to the EKS cluster: 
```			
kubectl config current-context
```
### Get Status of Pods
```
kubectl get pods
``` 
### If any service has error from above command, then execute below command for the error service
```
kubectl logs -f <error-pod-name>
``` 

### After identifying issue from above log and fixing manually, try to setup DataHub with following Upgrade command
### For updating the helm chart
  ```
  helm upgrade --install prerequisites datahub/datahub-prerequisites --values ./charts/prerequisites/values.yaml --version 0.0.10
  helm upgrade --install datahub datahub/datahub --values ./charts/datahub/values.yaml --version 0.2.108 
```  


### After the DataHub setup is successful, execute below in Cloud9 CLI to get DataHub frontend URL that uses 9002 port 
```
    kubectl get svc
``` 

### Access the DataHub URL in browser with HTTP. (Disconnect from VPN that might block this port) 
```	
    http://<id>.<region>.elb.amazonaws.com:9002/
```	
Note: This is not recommended for production deployment, we recommend to change the default user name and password or configure SSO via OpenID Connect - https://datahubproject.io/docs/authentication/guides/add-users/. And also use the following link to expose end point by setting up ingress controller with custom domain name. https://datahubproject.io/docs/deploy/aws/ in order to meet your networking requirement.

### Other useful commands​
Command	Description
```
## datahub	Remove DataHub	
helm uninstall 
## List of Helm charts
helm ls	
## Fetch a release history
helm history	
```	

## 4- Expose endpoints using a load balancer [Optional]​

### IRSA - IAM role for service account 
https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html


### Download the IAM policy document for allowing the controller to make calls to AWS APIs on your behalf.

```
curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.2.0/docs/install/iam_policy.json

```

###Create an IAM policy based on the policy document by running the following.
```
aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json
```


### Use eksctl to create a service account that allows us to attach the above policy to kubernetes pods.

```
eksctl create iamserviceaccount \
  --cluster={cluster_name} \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn={cluster_name} \
  --override-existing-serviceaccounts \
  --approve      
```

### Install the TargetGroupBinding custom resource definition by running the following.
```
kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"  
```



### Add the helm chart repository containing the latest version of the ALB controller.

```
helm repo add eks https://aws.github.io/eks-charts
helm repo update
```


### Install the controller into the kubernetes cluster by running the following.

```
helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
  --set clusterName={cluster Name} \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  -n kube-system
```

We can enable ingress by updating the values.yaml
https://datahubproject.io/docs/deploy/aws

###  Update default password for Superadmin user "datahub"[optional]
Create a file /tmp/user.props
Add a single line with user:password E.g:  datahub:<password>

```
kubectl create secret generic datahub-users --from-file=user.props=/tmp/user.props 
```

```
extraVolumes:
    - name: user-props
      secret:
        secretName: datahub-pass-secret
  extraVolumeMounts:
    - name: user-props
      mountPath: /datahub-frontend/conf/user.props
      subPath: token
      readOnly: true
```      