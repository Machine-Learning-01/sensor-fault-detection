# Sensor Assignment
​
## Task 1
You have to pick one project from the internship portal [link](https://internship.ineuron.ai/). The Sensor is a classification project, thus you must choose one of the classification projects from the portal.  You have to complete and submit the chosen project with the same architecture as the sensor project.
​
## Task 2
The project which you have built, you need to modify the architecture of the project. 
For example -
Please use the dask library for model training. 
- Refer to [this](https://ml.dask.org/install.html) official document for installation of dask library. 
- Refer to [this](https://examples.dask.org/machine-learning.html) document for model training.
In the sensor project data drift has been used, you have to implement data drift and model drift in your project. Create a proper document with explanation on the changes proposed.
​
## Task 3
You need to think of some different approaches to solve the same project and  implement those approaches to the project. Try to use a Deep learning approach for getting better model performance. 
​
Libraries to be used - 1. Tensorflow
                        2. PyTorch
​
Create a proper document with explanation.
​
## Task 4
Change the data pipeline destination from MongoDB to S3 bucket and change the data ingestion component accordingly.  Try to optimise all components based on time complexity. 
For example - Let's say, the data ingestion component takes 1 minute to complete. You need to optimise in such a way that the process can be completed in less than 1 minute,  like in 45 seconds or 30 seconds. 
​
## Task 5
AWS services were used in the sensor project to deploy the app in the cloud and GitHub Actions were used for CICD. 
You need to deploy your project on Azure cloud services and to save the model artifacts you have to use Azure blob storage. 
	For CICD you have to use CircleCI. 