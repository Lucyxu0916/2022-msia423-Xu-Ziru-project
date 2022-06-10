# Body Fat Prediction
Author: Ziru Xu

# Table of Contents
* [Project Charter](#Project-charter)
* [Directory structure ](#Directory-structure)
* [Environment set up](#Environment-setup)
  * [AWS Credential](#AWS-Credential)
  * [RDS Credential](#RDS-Credential)
* [Docker](#Docker)
  * [Docker Image](#Docker-Image)
  * [Build Image](#Build-Image)
* [Model pipeline](#Model-pipeline)
  * [Download Raw Data from S3](#Download-Raw-Data-from-S3)
  * [Preprocess Data](#Preprocess-Data)
  * [Generate Features](#Generate-Features)
  * [Train Model](#Train-Model)
  * [Score Model](#Score-Model)
  * [Evaluate Model](#Evaluate-Model)
  * [Run Entire Pipeline](#Run-Entire-Pipeline)
* [Run the app](#Run-the-app)
  * [1.Initialize database](#1-Initialize-database)
  * [2.Configure Flask app ](#2-Configure-Flask-app)
  * [3.Run the Flask app ](#3-Run-the-Flask-app)
  * [4.Kill the container ](#4-Kill-the-container)
* [Testing](#Testing)


## Project Charter
### Vision
Human body needs fat to function; however, excess fat introduces a higher risk of developing heart diseases, kidney problems, and even cancer. Since the COVID-19 pandemic, the CDC has suggested that obesity increases the risk of severe illness and hospitalization due to COVID-19 infection. Consequently, it is crucial for individuals to keep track of their body fat to evaluate their health.

According to the American College of Sports Medicine, the gold standard for calculating body fat is hydrostatic (or underwater) weighing. During the test, the person is submerged in water while sitting on a scale, and the body fat percentage is calculated by comparing the land weight with the underwater weight. Apparently, measuring body fat percentage in this way is time-consuming and requires special equipment that is not easily accessible. Thus, this app aims to help users easily obtain their body fat percentage information.


### Mission
To better help users understand their health condition, this app will help the users to predict their body fat percentage based on their input of gender, age, weight, height, and circumference of different body parts. This app will also show the users the standard body fat percentage range based on their age and height group so that the users know if they have excess fat or not. If the users' body fat percentage is suboptimal, they could 
make fitness plans accordingly and monitor their fitness progress. 

The dataset(https://www.kaggle.com/datasets/fedesoriano/body-fat-prediction-dataset) contains the body fat percentage, age, weight, height, and ten circumference measurements (e.g., neck, chest waist, etc..) for 252 men. The body fat percentage in the dataset was accurately determined by an underwater weighing technique.

### Success Criteria
#### Machine learning performance metric
The following metrics will be used to assess the model’s performance prior to deployment:

1) Mean Absolute Error(MAE): MAE calculates the average absolute difference between actual and predicted values.

2) Mean Squared Error(MSE): MSE calculates the average squared difference between actual and predicted values.

3) R Squared: R Squared measures the proportion of the variance for the dependent variable that's explained by the independent variables in the model.

4) Adjusted R Squared: Adjusted R Squared is a modified version of R-squared that has been adjusted for the number of predictors in the model.

#### Business metric
1) User Activation: Number of new users every month

2) User Engagement: Number of daily/monthly active user

3) User Retention: Percentage of users who return to the app after the current month

4) User Satisfaction: Surveys completed by the users to rate the app and provide feedback


## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│       ├── basic.css                 <- CSS file to set the style for html pages
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│       ├── error.html		      <- Error page template
│	├── index.html		      <- Index page template
│
├── config                            <- Directory for confiration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│    	├── local.conf		      <- Confiuration file for python loggers
│   ├── config.yaml                   <- Configurations for model pipeline
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── artifacts/                    <- Artifact data sources, used to store artifacts generated from each pipeline step
│   ├── raw/                          <- Raw data sources, used to upload to S3 to mimic the data acquisition process
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│   ├── AVC Project Presentation.pdf/ <- Presentation slides for body fat prediction
│
├── dockerfiles/                      <- Directory for all project-related Dockerfiles 
│   ├── Dockerfile.app                <- Dockerfile for building image to run web app
│   ├── Dockerfile.run                <- Dockerfile for building image to execute run.py  
│   ├── Dockerfile.test               <- Dockerfile for building image to run unit tests
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project.
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project. No executable Python files should live in this folder.  
│   ├── add_bodymeasurement.py        <- Python script that defines the data model for my table in RDS
│   ├── evaluate_model.py             <- Python script that evaluates a model
│   ├── generate_features.py          <- Python script that generate new features from data
│   ├── preprocess_data.py            <- Python script that preprocesses data 
│   ├── s3.py                         <- Python script that connects to S3
│   ├── score_model.py                <- Python script that scores model
│   ├── train_model.py                <- Python script that trains model
│
├── tests/                            <- Files necessary for running model tests (see documentation below) 
│   ├──test_generate_features.py      <- Python script that tests the functions in generate_features.py 
│   ├──test_preprocess_data.py        <- Python script that tests the functions in preprocess_data.py 
│ 
├── app.py                            <- Flask wrapper for running the web app 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── run_rds.py                        <- Create relevant tables in the database
├── run_s3.py                         <- Upload or download raw data to or from s3 bucket
├── requirements.txt                  <- Python package dependencies 
├── Makefile			      <- Make commands to execute and dependencies among the generated files
```
NOTE: Please be sure to be connected to the Northwestern VPN and go to the root directory of the repository before you move forward with the following steps.

## Environment Set up

### AWS Credential
In order to connect to S3, you would first need to configure your AWS Credentials. To configure AWS credentials, run the following commands in terminal to load your credentials as environment variables.
```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
```
Note: Please remember to change  "YOUR_ACCESS_KEY_ID" and "YOUR_SECRET_ACCESS_KEY" above to your own AWS credentials, and you can run the following command to check if the credential is set up correctly.
```bash
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
```

### RDS Credential
In order to connect to database in RDS, you would first need to configure your RDS credential. A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html).

To configure RDS credential, run the following command in terminal to load your credentials as environment variables.
```bash
export SQLALCHEMY_DATABASE_URI = "YOUR_DATABASE_URI"
```
Note: Please remember to change  "YOUR_DATABASE_URI"  above to your own ```SQLALCHEMY_DATABASE_URI```, and you can run the following command to check if the credential is set up correctly.
```bash
echo $SQLALCHEMY_DATABASE_URI
```

## Docker
### Docker Image
This project requires three docker images to execute the python files
1. Dockerfile: to run model pipeline
2. Dockerfile.app: to run the web app
3. Dockerfile.test: to run tests for eligible functions used in the project

### Build Image
Run following commands to build the above images
```bash
make pipeline_image
```
It produces a docker image called final-project which are used to get the raw data, run the model pipeline, and interact with database.
```bash
make app_image
```
It produces a docker image called final-project-app, which are used to launch the flask app.
```bash
make test_image
```
It produces a docker image called final-project-tests, which are used to run the test.

## Model Pipeline

### Download Raw Data from S3
You can download the data from s3 to the repository by running ```make download_from_s3```. The default ```s3_path``` is ```s3://2022-msia-423-xu-ziru/raw/bodyfat.csv```. This step will store the data as ```data/raw/bodyfat.csv```. 

### Preprocess Data
You can preprocess the raw data by running ```make process```. This step will save the preprocessed data as ```data/artifacts/cleaned_data.csv```. 

### Generate Features
You can generate scaler and scale features by running ```make features```. This step will save the scaler as ```models/scaler.sav``` and save features and target as ```data/artifacts/features.csv``` and ```data/artifacts/target.csv```.

### Train Model
You can train the Lasso regression model by running ```make train```. This step will save the train and test data in ```data/artifacts/``` and save the model as ```models/Lasso.sav``` 

### Score Model
You can generate the model predictions on test data by running ```make predict```. This step will save the prediction result as ``data/artifacts/predictions.txt```.

### Evaluate Model
You can evaluate the model performance by running ```make evaluate```. This step will save the evaluation result in ```data/artifacts/evaluation_result.txt```.

### Run Entire Pipeline

You can run the entire model pipeline by using ```make model-pipeline```
This command will run the entire model pipeline mentioned above, from downloading the raw data from s3, preprocessing data, generating features, training the model, scoring the model, all the way to evaluating model performance.


## Run the App
Before running the app, make sure you have completed the following:

1. Set environment variables properly according to the above guidelines.

2. Build docker image final-project-app by running make image-app.

3. Run the entire model pipeline either by make model-pipeline or executing each step sequentially with the corresponding make command.

4. Create the relevant tables in the database connected via your ```SQLALCHEMY_DATABASE_URI``` environment variable . This can be done by running ```make database```.

### 1. Initialize Database
The web app needs a SQL database to run. To create the relevant tables in your database, run following command.
```make database```

You can also create a local SQLite database to test the app by passing a SQLite engine string to the environment variable ```SQLALCHEMY_DATABASE_URI```. It does not require a username or password and replaces the host and port with the path to the database file, and it takes the following form:
```sqlite:///data/bodyfat.db'```

If no ```SQLALCHEMY_DATABASE_URI``` environment variable is found, a default SQLite engine string ```sqlite:///data/bodyfat.db``` is used to create a local database.
'
### 2. Configure Flask app

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5001 # What port to expose app on. Must be the same as the port exposed in dockerfiles/Dockerfile.app 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/bodyfat.db'  # URI (engine string) for database that contains tracks
APP_NAME = "BodyFatCalculator"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```
### 3. Run the Flask app 

To run the Flask app, run: 

```bash
make run_app
```
You should be able to access the app at http://127.0.0.1:5001/ in your browser (Mac/Linux should also be able to access the app at http://127.0.0.1:5001/ or localhost:5001/) .

Note: If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5001` line in `dockerfiles/Dockerfile.app`)

### 4. Kill the container 

Once finished with the app, you will need to kill the container. If you named the container, you can execute the following: 

```bash
docker kill test-app 
```
where `test-app` is the name given in the `docker run` command.

If you did not name the container, you can look up its name by running the following:
```bash
docker container ls
```
The name will be provided in the right most column.


## Testing

Once you have built the image final-project-tests for testing by running `make test_image`. You can run the following to run uint tests:

```bash
make run_test
```

The following command will be executed within the container to run the provided unit tests under `tests/`:  

```bash
python -m pytest
```