![alt text](https://ineuron.ai/images/ineuron-logo.png)

# Infrastructure Setup 

## AWS Cloud Setup 

First we need to have a AWS account with credit card attached to it, else we will not be able to access AWS cloud resources. Once that is that, login to AWS account, with your credentials. Once that is done, near to the services section there is a serach tab, there type IAM and click enter. You will be redirected to IAM console, in the access management, click on users and then click on add user, give the username of your choice, example "sensorproject" and select the AWS access type as programmatic access, then click on next permissions, and click on attach existing policies directly and select "AmazonEC2FullAccess" policy and "AmazonS3FullAccess" policy. Click on next tags, you can skip the creation of tags, and next review, here you shall see that the user with username as "sensorproject" has been created with AmazonEC2FullAccess and AmazonS3FullAccess policy, once the review is done, click on create user. Once that is done, the user will be created with given permissions and neccessary AWS keys are created. Note that these keys have to be kept secret and not shared with anyone, and there is no way to retrive these secrets once lost, so be carefull not to expose or lose these credentials. With that said, download the .csv file which contains the credentials for connecting to AWS via CLI. You can now close and you will redirected to iam console, where you can "sensorproject" user has been created.

## AWS CLI Installation

### Install AWS CLI in Linux System

To install awscli in linux system, execute the following commands

```bash
sudo apt update
```

```bash
sudo apt upgrade
```

```bash
sudo apt install awscli
```

### Install AWS CLI in Windows System

To install awscli in windows system, follow the process, 

Install the msi package of awscli

```bash
https://awscli.amazonaws.com/AWSCLIV2.msi
```

Once the download and double click on the installer, and click on next and agree to the terms and conditions, and click on next and click on install button. Once the installation is done, click on finish and proceed to the futher steps

### Install AWS CLI in MacOS System

To install awscli on MacOS system, execute the following commands

```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
```

```bash
sudo installer -pkg AWSCLIV2.pkg -target /
```

### Check AWS CLI installation

To check aws cli is working fine or not, execute the following commands

```bash
aws --version
```

### Manual deployment of the application to instance

First step is to login to the console, you can open aws console in your browser and login with your credentials


Once you are logged into you aws account, go to services and select the EC2 service. Go the network and security column and click on key pairs, on doing so you will be redirected to key pairs page.


Click on create key pair and give any key pair name and private key file format and then click on create key pair and select the location of key pair.


Once that is done, go to instances columns and click on instances, by default there will be no instances present.To launch an EC2 instance, click on launch instance and you will be redirected to launch a instance page


Next, write the name of the instance and then click on browser more amis, and in the search bar, write deep learning and select the first ami. 


Once that is done select the instance type to be t2.large and key pair which was previously created.



Coming to the network settings, click on edit and then in the inbound security groups rule click on add security group role and in port range write 8080, in the source select 0.0.0.0/0. Once that is done, click on launch instance and then after some time EC2 instance will reach running state.



Once the instance is running, click on the instance id and then click on connect and copy the ssh command. Open any SSH client like Putty,Mobaxterm or powershell terminal and change directory to the place where the pem file is present, and paste the command and then click on enter. Type yes on prompted.



After the you will be successfully connected to EC2 instance via SSH.